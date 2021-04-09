{ pkgs ? import <nixpkgs> {} }:
let
  mach-nix = import (
    builtins.fetchGit {
      url = "https://github.com/DavHau/mach-nix/";
      ref = "refs/tags/3.2.0";
      rev = "ac62255e8112e547432ca0f09bfe8f4d1920fbb8";
    }
  ) {};

  pips = mach-nix.mkPython {
    requirements = builtins.readFile ./requirements.txt;
  };
in
pkgs.mkShell {
  buildInputs = [
    pips
    pkgs.python39
  ];

}
