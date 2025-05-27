#!/usr/bin/env bash
# Build the VGraph runtime for current platform
# Cross-platform compatible bash script
# For better Windows support, use build_runtime.py instead

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[Build] Compilando runtime VGraph..."
echo "[Build] Script directory: $SCRIPT_DIR"

# Detectar el sistema operativo con mejor detección
OS="$(uname -s)"
ARCH="$(uname -m)"

case "${OS}" in
    Linux*)     
        echo "[Build] Plataforma: Linux ($ARCH)"
        PLATFORM="linux"
        CFLAGS="-O2 -fPIC"
        ;;
    Darwin*)    
        echo "[Build] Plataforma: macOS ($ARCH)"
        PLATFORM="macos"
        CFLAGS="-O2 -fPIC"
        ;;
    MINGW*|MSYS*|CYGWIN*)
        echo "[Build] Plataforma: Windows (${OS})"
        PLATFORM="windows"
        CFLAGS="-O2"
        ;;
    FreeBSD*)
        echo "[Build] Plataforma: FreeBSD"
        PLATFORM="freebsd"
        CFLAGS="-O2 -fPIC"
        ;;
    *)
        echo "[Build] Plataforma no reconocida: ${OS}"
        echo "[Build] Usando configuración por defecto"
        PLATFORM="unknown"
        CFLAGS="-O2"
        ;;
esac

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detectar compilador C disponible
if command_exists clang; then
    CC="clang"
    echo "[Build] Usando compilador: clang"
elif command_exists gcc; then
    CC="gcc"
    echo "[Build] Usando compilador: gcc"
elif command_exists cc; then
    CC="cc"
    echo "[Build] Usando compilador: cc"
else
    echo "[Build] ERROR: No se encontró compilador C (clang, gcc, o cc)"
    echo "[Build] Por favor instala uno de los siguientes:"
    case "$PLATFORM" in
        "linux")
            echo "[Build]   Ubuntu/Debian: sudo apt install build-essential"
            echo "[Build]   CentOS/RHEL: sudo yum groupinstall 'Development Tools'"
            echo "[Build]   Fedora: sudo dnf groupinstall 'Development Tools'"
            ;;
        "macos")
            echo "[Build]   macOS: xcode-select --install"
            echo "[Build]   o instala Homebrew y ejecuta: brew install gcc"
            ;;
        "windows")
            echo "[Build]   Windows: Instala MinGW-w64 o Visual Studio Build Tools"
            ;;
    esac
    exit 1
fi

# Detectar archivador
if command_exists ar; then
    AR="ar"
    echo "[Build] Usando archivador: ar"
elif command_exists llvm-ar; then
    AR="llvm-ar"
    echo "[Build] Usando archivador: llvm-ar"
else
    echo "[Build] WARNING: No se encontró archivador (ar o llvm-ar)"
    echo "[Build] No se creará archivo .a"
    AR=""
fi

# Verificar archivos fuente
RUNTIME_C="$SCRIPT_DIR/runtime.c"
RUNTIME_H="$SCRIPT_DIR/runtime.h"

if [[ ! -f "$RUNTIME_C" ]]; then
    echo "[Build] ERROR: No se encontró $RUNTIME_C"
    exit 1
fi

if [[ ! -f "$RUNTIME_H" ]]; then
    echo "[Build] WARNING: No se encontró $RUNTIME_H"
fi

echo "[Build] Archivos fuente verificados"
echo "[Build] Flags de compilación: ${CFLAGS}"

# Compilar runtime.c
echo "[Build] Compilando runtime.c..."
RUNTIME_O="$SCRIPT_DIR/runtime.o"

if ! ${CC} ${CFLAGS} -c "$RUNTIME_C" -o "$RUNTIME_O"; then
    echo "[Build] ERROR: Falló la compilación"
    exit 1
fi

if [[ ! -f "$RUNTIME_O" ]]; then
    echo "[Build] ERROR: No se generó runtime.o"
    exit 1
fi

echo "[Build] SUCCESS: runtime.o creado"

# Crear archivo estático si tenemos archivador
if [[ -n "$AR" ]]; then
    echo "[Build] Creando biblioteca estática..."
    RUNTIME_LIB="$SCRIPT_DIR/libvgraphrt.a"
    
    if ! ${AR} rcs "$RUNTIME_LIB" "$RUNTIME_O"; then
        echo "[Build] WARNING: Falló la creación de libvgraphrt.a"
    else
        if [[ -f "$RUNTIME_LIB" ]]; then
            echo "[Build] SUCCESS: libvgraphrt.a creado"
        else
            echo "[Build] WARNING: libvgraphrt.a no fue creado"
        fi
    fi
fi

# Verificar resultado final
echo "[Build] Verificando archivos generados..."
if [[ -f "$RUNTIME_O" ]]; then
    SIZE=$(du -h "$RUNTIME_O" | cut -f1)
    echo "[Build]   ✓ runtime.o ($SIZE)"
else
    echo "[Build]   ✗ runtime.o"
fi

if [[ -f "$SCRIPT_DIR/libvgraphrt.a" ]]; then
    SIZE=$(du -h "$SCRIPT_DIR/libvgraphrt.a" | cut -f1)
    echo "[Build]   ✓ libvgraphrt.a ($SIZE)"
fi

# Información del compilador
echo "[Build] Información del compilador:"
if ${CC} --version >/dev/null 2>&1; then
    ${CC} --version | head -n 1 | sed 's/^/[Build]   /'
fi

echo "[Build] Runtime compilado correctamente"
echo "[Build] Plataforma: $PLATFORM"
echo "[Build] Compilador: $CC"
if [[ -n "$AR" ]]; then
    echo "[Build] Archivador: $AR"
fi

# Función de limpieza
cleanup() {
    echo "[Build] Limpiando archivos temporales..."
    rm -f "$SCRIPT_DIR"/*.tmp
}

# Registrar función de limpieza
trap cleanup EXIT