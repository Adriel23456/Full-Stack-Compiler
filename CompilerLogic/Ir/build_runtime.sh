#!/usr/bin/env bash
# Build the VGraph runtime for current platform
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[Build] Compilando runtime VGraph..."

# Detectar el sistema operativo
OS="$(uname -s)"
case "${OS}" in
    Linux*)     
        echo "[Build] Plataforma: Linux"
        CFLAGS="-O2 -fPIC"
        ;;
    Darwin*)    
        echo "[Build] Plataforma: macOS"
        CFLAGS="-O2 -fPIC"
        ;;
    MINGW*|MSYS*|CYGWIN*)
        echo "[Build] Plataforma: Windows (MinGW/MSYS/Cygwin)"
        CFLAGS="-O2"
        ;;
    *)
        echo "[Build] Plataforma no reconocida: ${OS}"
        CFLAGS="-O2"
        ;;
esac

# Compilar runtime
if command -v clang &> /dev/null; then
    CC="clang"
elif command -v gcc &> /dev/null; then
    CC="gcc"
else
    echo "[Error] No se encontró compilador C (clang o gcc)"
    exit 1
fi

echo "[Build] Usando compilador: ${CC}"
echo "[Build] Flags: ${CFLAGS}"

${CC} ${CFLAGS} -c "$SCRIPT_DIR/runtime.c" -o "$SCRIPT_DIR/runtime.o" -lm

# Crear archivo estático
ar rcs "$SCRIPT_DIR/libvgraphrt.a" "$SCRIPT_DIR/runtime.o"

echo "[Build] runtime.o creado"
echo "[Build] libvgraphrt.a creado"
echo "[Build] Runtime compilado correctamente"