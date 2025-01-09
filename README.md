# tiff2pdf
Convert TIFF files to PDFs.

## Usage
```
usage: tiff2pdf [-h] [-d] [-r ROTATE] [-x WIDTH] [-y HEIGHT] path

Convert TIFF files to PDFs.

positional arguments:
  path        Path to TIFF file (or directory containing TIFFs: see option `-d`).

options:
  -h, --help  show this help message and exit
  -d          The specified path is a directory containing files with the `.tiff` or `.tif`
              extension.
  -r ROTATE   Rotate the orientation of the TIFF by ROTATE degrees when scaling the PDF.
  -x WIDTH    Resize the PDF to WIDTH (in points). Height option must also be specified.
  -y HEIGHT   Resize the PDF to HEIGHT (in points). Width option must also be specified.
```

If you are using `nix`, you can run the script with `nix run`:

```bash
nix run github:tdback/tiff2pdf -- -h
```

### Example
Bulk convert a directory containing TIFF file drawings to PDFs, but rotate the
images by 90 degrees and scale the resulting PDFs up to 11 x 17 sized sheets
for printing.

```bash
tiff2pdf -r 90 -x 892 -y 1191 -d ./drawings
```

## Requirements
The script relies on the following libraries, which can be installed via `pip`:

```bash
pip install pillow PyPDF2
```

Or if you are using `nix`, you can build a self-contained binary with the
following command:

```bash
nix build
```

The generated executable can be found in `./result/bin/`.
