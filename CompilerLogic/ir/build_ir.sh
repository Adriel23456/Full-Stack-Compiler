#!/usr/bin/env bash
set -e
clang -c runtime.c -o runtime.o
clang -O2 ../../out/vGraph.ll runtime.o -o ../../out/vGraph.exe