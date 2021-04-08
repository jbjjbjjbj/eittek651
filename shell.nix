{ pkgs ? import <nixpkgs> {} }:
let
  mach-nix = import (
    builtins.fetchGit {
      url = "https://github.com/DavHau/mach-nix/";
      ref = "refs/tags/3.1.1";
      rev = "1ec92303acd142aa1a3b60bb97745544cf049312";
    }
  ) {};

  pips = mach-nix.mkPython {
    requirements = builtins.readFile ./requirements.txt;
  };
in
pkgs.mkShell {
  buildInputs = [
    pips
  ];

}
