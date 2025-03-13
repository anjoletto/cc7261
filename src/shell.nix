{ pkgs ? import <nixpkgs> {
  config.allowUnfree = true;
} }:
  pkgs.mkShell {
      nativeBuildInputs = with pkgs.buildPackages; [
        python312
        python312Packages.pip
        python312Packages.pyzmq
        python312Packages.msgpack
        zeromq
        czmq
        mpi
    ];
  }
