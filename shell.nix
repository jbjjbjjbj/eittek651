{ pkgs ? import <nixpkgs> {} }:
let
  mach-nix = import (
    builtins.fetchGit {
      url = "https://github.com/DavHau/mach-nix/";
      ref = "refs/tags/3.2.0";
      rev = "ac62255e8112e547432ca0f09bfe8f4d1920fbb8";
    }
    ) {
      pypiDataRev = "c67aa64b8cfb625a4ebf197d3e3edd9a6e3fccb3";
      pypiDataSha256 = "0ma6naxawngbd4m2c35dywqa1vlw6ckfgp8q803j8kragy2ybbyl";

    };

    pips = mach-nix.mkPython {
      requirements = builtins.replaceStrings
        [ "PyQt5" ]
        [ "" ]
        (builtins.readFile ./requirements.txt);
    };
in
  pkgs.mkShell {
    buildInputs = [
      pips
    ];

    shellHook = ''
        export MPLBACKEND="webagg"
        '';

  }
