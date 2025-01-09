#!/usr/bin/env python3

# tiff2pdf: Convert TIFF files to PDF. Depends on pillow and PyPDF2.

import argparse
import os
import sys

from PIL import Image
from PyPDF2 import PageObject, PdfReader, PdfWriter, Transformation
from PyPDF2.generic import RectangleObject


def generate_pdf(path, rotate, width, height):
    images = []

    # Convert each "page" (frame) in the TIFF to an image format used by PDFs.
    img = Image.open(path)
    for n in range(img.n_frames):
        try:
            img.seek(n)
            img = img.rotate(rotate, expand=True) if rotate else img
            images.append(img.convert("RGB"))
        except EOFError:
            break

    # Save - and optionally scale - the PDF.
    if images:
        ext = ".tiff" if path.endswith(".tiff") else ".tif"
        pdf_path = f"{path.rstrip(ext)}.pdf"

        images[0].save(
            pdf_path,
            save_all=True,
            append_images=images[1:],
            quality=100,
        )

        if width and height:
            scale_pdf(pdf_path, width, height)


def scale_pdf(path, width, height):
    reader = PdfReader(path)
    writer = PdfWriter()

    for page in reader.pages:
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)

        # Calculate and scale the page while preserving the aspect ratio.
        scale_factor = min(width/w, height/h)

        # Resize page to fit *inside* new dimensions.
        transform = Transformation().scale(scale_factor, scale_factor)
        page.add_transformation(transform)

        # Set the page to the desired size.
        page.cropbox = RectangleObject((0, 0, width, height))

        # Prepare the new page.
        new_page = PageObject.create_blank_page(width=width, height=height)
        page.mediabox = new_page.mediabox
        new_page.merge_page(page)

        writer.add_page(new_page)

    # Overwrite the original PDF with the scaled version.
    with open(path, "wb") as f:
        writer.write(f)


def main():
    parser = argparse.ArgumentParser(
        prog="tiff2pdf",
        description="Convert TIFF files to PDFs.",
    )

    parser.add_argument(
        dest="path",
        help="Path to TIFF file (or directory containing TIFFs: see option `-d`).",
    )

    parser.add_argument(
        "-d",
        dest="is_dir",
        action="store_true",
        help="The specified path is a directory containing files with the `.tiff` or `.tif` extension.",
    )

    parser.add_argument(
        "-r",
        dest="rotate",
        type=float,
        help="Rotate the orientation of the TIFF by ROTATE degrees when scaling the PDF.",
    )

    parser.add_argument(
        "-x",
        dest="width",
        type=float,
        help="Resize the PDF to WIDTH (in points). Height option must also be specified.",
    )

    parser.add_argument(
        "-y",
        dest="height",
        type=float,
        help="Resize the PDF to HEIGHT (in points). Width option must also be specified.",
    )

    args = parser.parse_args()

    if not args.width or not args.height:
        print(
            "width and height require that both or neither be specified",
            file=sys.stderr,
        )
        exit(1)

    if not os.path.exists(args.path):
        print(f"path '{args.path}' does not exist.", file=sys.stderr)
        exit(1)

    if args.is_dir:
        for root, dirs, files in os.walk(args.path):
            for file in files:
                if file.endswith(".tiff") or file.endswith(".tif"):
                    path = f"{root}{os.sep}{file}"
                    generate_pdf(path, args.rotate, args.width, args.height)
    else:
        generate_pdf(args.path, args.rotate, args.width, args.height)


if __name__ == "__main__":
    main()
