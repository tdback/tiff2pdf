{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  outputs = { nixpkgs, ... }: let
    supportedSystems = [
      "x86_64-linux"
      "aarch64-linux"
      "x86_64-darwin"
      "aarch64-darwin"
    ];

    eachSystem = nixpkgs.lib.genAttrs supportedSystems;
    pkgsBySystem = nixpkgs.lib.getAttrs supportedSystems nixpkgs.legacyPackages;

    forAllPkgs = fn:
      nixpkgs.lib.mapAttrs (system: pkgs: (fn pkgs)) pkgsBySystem;

    tiff2PdfFor = pkgs: let
      bin = "tiff2pdf";
      version = "1.0.0";
    in
      pkgs.python3Packages.buildPythonApplication {
        pname = bin;
        version = version;
        src = ./.;

        propagatedBuildInputs = with pkgs.python3Packages; [
          pillow
          pypdf2
        ];

        preBuild = ''
          cat > setup.py << EOF
          from setuptools import setup
          setup(
              name='${bin}',
              verion='${version}',
              install_requires=['pillow','pypdf2'],
              scripts=['${bin}.py']
          )
          EOF
        '';

        postInstall = "mv -v $out/bin/${bin}.py $out/bin/${bin}";
      };
  in {
    packages = forAllPkgs (pkgs: {
      default = tiff2PdfFor pkgs;
    });

    devShells = eachSystem (system: let
      pkgs = import nixpkgs { inherit system; };
    in {
      default = pkgs.mkShell {
        buildInputs = with pkgs; [
          (python3.withPackages (p: with p; [
            ipython
            pillow
            pypdf2
            python-lsp-server
          ]))
        ];
      };
    });
  };
}
