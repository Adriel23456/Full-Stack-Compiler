# File: CompilerLogic/ir/build_runtime.sh
#!/usr/bin/env bash
# Build the tiny VGraph runtime and create a static archive.
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
clang -O2 -c "$SCRIPT_DIR/runtime.c" -o "$SCRIPT_DIR/runtime.o"
ar rcs "$SCRIPT_DIR/libvgraphrt.a" "$SCRIPT_DIR/runtime.o"
echo "libvgraphrt.a created."