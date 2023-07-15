{ pkgs ? import <nixpkgs> {} }:

let
  myWheel = "${/run/user/1000/pdm-build-mma56jx0/urllib3-1.26.16-py2.py3-none-any.whl}";
in
pkgs.mkShell rec {
  buildInputs = [
    pkgs.python3
  ];

  shellHook = ''
    ${pkgs.python3.interpreter}/bin/pip install --no-index --find-links=file://${myWheel} $(basename ${myWheel})
  '';
}
