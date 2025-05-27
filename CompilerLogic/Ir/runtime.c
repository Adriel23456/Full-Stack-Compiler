/* runtime.c – VGraph runtime portable
 *
 *  • Frame-buffer 800×600 RGB (24-bit) mapeado a image.bin
 *  • Busca image.bin en el mismo directorio que el ejecutable
 *  • Compatible con Linux, macOS, Windows (via MinGW/MSVC/Cygwin)
 *  • Mejorado para máxima compatibilidad cross-platform
 */

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>       /* sqrt, abs */

#if defined(__linux__)
    #include <stdarg.h>
    #include <errno.h>
#endif

/* Detección de plataforma mejorada */
#if defined(_WIN32) || defined(_WIN64) || defined(__CYGWIN__) || defined(__MINGW32__) || defined(__MINGW64__)
    #define PLATFORM_WINDOWS
    #include <windows.h>
    #include <io.h>
    #define PATH_SEPARATOR "\\"
    #ifndef PATH_MAX
        #define PATH_MAX MAX_PATH
    #endif
#else
    #define PLATFORM_UNIX
    #include <unistd.h>     /* usleep, readlink */
    #include <fcntl.h>      /* open, O_* flags */
    #include <sys/mman.h>   /* mmap, munmap, msync */
    #include <sys/stat.h>   /* ftruncate */
    #include <libgen.h>     /* dirname */
    #include <limits.h>     /* PATH_MAX */
    #define PATH_SEPARATOR "/"
    
    #ifdef __APPLE__
        #include <mach-o/dyld.h>  /* _NSGetExecutablePath */
    #endif
#endif

#ifndef PATH_MAX
    #define PATH_MAX 4096
#endif

#define W 800
#define H 600
#define BYTES (W * H * 3)

static uint8_t *img      = NULL;        /* frame-buffer */
static uint32_t CUR      = 0x00FFFFFF;  /* color actual */
static char     img_path[PATH_MAX];     /* ruta completa a image.bin */
static int      initialized = 0;        /* flag de inicialización */

#ifdef PLATFORM_WINDOWS
static HANDLE hMapFile = NULL;
static HANDLE hFile = INVALID_HANDLE_VALUE;
#else
static int      fdimg    = -1;          /* descriptor de image.bin */
#endif

/* ───────── Funciones auxiliares mejoradas ───────── */

/* Función de logging thread-safe */
static void vg_log(const char *level, const char *format, ...)
{
    va_list args;
    va_start(args, format);
    fprintf(stdout, "[VGraph-%s] ", level);
    vfprintf(stdout, format, args);
    fprintf(stdout, "\n");
    fflush(stdout);
    va_end(args);
}

/* Obtiene el directorio donde se encuentra el ejecutable (multi-plataforma mejorado) */
static int get_executable_dir(char *dir, size_t size)
{
    char path[PATH_MAX];
    
#ifdef PLATFORM_WINDOWS
    /* Windows - funciona con MSVC, MinGW, Cygwin */
    DWORD len = GetModuleFileNameA(NULL, path, sizeof(path));
    if (len > 0 && len < sizeof(path)) {
        /* Convertir separadores a formato Windows */
        for (char *p = path; *p; p++) {
            if (*p == '/') *p = '\\';
        }
        
        /* Eliminar el nombre del ejecutable para obtener solo el directorio */
        char *last_sep = strrchr(path, '\\');
        if (last_sep) {
            *last_sep = '\0';
        }
        
        /* Copiar resultado */
        if (strlen(path) < size) {
            strcpy(dir, path);
            return 1;
        }
    }
    
#elif defined(__APPLE__)
    /* macOS */
    uint32_t bufsize = sizeof(path);
    if (_NSGetExecutablePath(path, &bufsize) == 0) {
        /* Usar dirname de forma segura */
        char temp_path[PATH_MAX];
        strcpy(temp_path, path);
        char *dir_path = dirname(temp_path);
        if (strlen(dir_path) < size) {
            strcpy(dir, dir_path);
            return 1;
        }
    }
    
#elif defined(__linux__)
    /* Linux */
    ssize_t len = readlink("/proc/self/exe", path, sizeof(path) - 1);
    if (len != -1) {
        path[len] = '\0';
        /* Usar dirname de forma segura */
        char temp_path[PATH_MAX];
        strcpy(temp_path, path);
        char *dir_path = dirname(temp_path);
        if (strlen(dir_path) < size) {
            strcpy(dir, dir_path);
            return 1;
        }
    }
#endif
    
    /* Fallback: usar directorio actual */
#ifdef PLATFORM_WINDOWS
    if (GetCurrentDirectoryA(size, dir) > 0) {
        return 1;
    }
#else
    if (getcwd(dir, size) != NULL) {
        return 1;
    }
#endif
    
    /* Último recurso */
    if (size > 1) {
        strcpy(dir, ".");
        return 1;
    }
    
    return 0;
}

/* Función para dormir (multi-plataforma) */
static void sleep_ms(int ms)
{
    if (ms <= 0) return;
    
#ifdef PLATFORM_WINDOWS
    Sleep(ms);
#else
    /* Usar nanosleep en sistemas Unix para mayor precisión */
    struct timespec ts;
    ts.tv_sec = ms / 1000;
    ts.tv_nsec = (ms % 1000) * 1000000;
    nanosleep(&ts, NULL);
#endif
}

/* Verificar si un archivo existe */
static int file_exists(const char *path)
{
#ifdef PLATFORM_WINDOWS
    DWORD attrs = GetFileAttributesA(path);
    return (attrs != INVALID_FILE_ATTRIBUTES && !(attrs & FILE_ATTRIBUTE_DIRECTORY));
#else
    return access(path, F_OK) == 0;
#endif
}

/* Crear directorio si no existe */
static int ensure_directory(const char *path)
{
#ifdef PLATFORM_WINDOWS
    return CreateDirectoryA(path, NULL) || GetLastError() == ERROR_ALREADY_EXISTS;
#else
    return mkdir(path, 0755) == 0 || errno == EEXIST;
#endif
}

static int init_buf(void)
{
    if (initialized) return 1;  /* ya inicializado */
    
    char exe_dir[PATH_MAX];
    
    /* Obtener directorio del ejecutable */
    if (!get_executable_dir(exe_dir, sizeof(exe_dir))) {
        vg_log("ERROR", "No se pudo obtener directorio del ejecutable");
        return 0;
    }
    
    /* Construir path completo a image.bin */
    int ret = snprintf(img_path, sizeof(img_path), "%s%simage.bin", exe_dir, PATH_SEPARATOR);
    if (ret >= sizeof(img_path) || ret < 0) {
        vg_log("ERROR", "Path demasiado largo para image.bin");
        return 0;
    }
    
    vg_log("INFO", "Ejecutable en: %s", exe_dir);
    vg_log("INFO", "Usando image.bin en: %s", img_path);
    
#ifdef PLATFORM_WINDOWS
    /* Windows: usar CreateFile y CreateFileMapping */
    hFile = CreateFileA(img_path,
                        GENERIC_READ | GENERIC_WRITE,
                        FILE_SHARE_READ | FILE_SHARE_WRITE,
                        NULL,
                        OPEN_ALWAYS,
                        FILE_ATTRIBUTE_NORMAL,
                        NULL);
    
    if (hFile == INVALID_HANDLE_VALUE) {
        DWORD error = GetLastError();
        vg_log("ERROR", "No se pudo abrir/crear %s (Error: %lu)", img_path, error);
        return 0;
    }
    
    /* Establecer tamaño del archivo */
    LARGE_INTEGER size;
    size.QuadPart = BYTES;
    if (!SetFilePointerEx(hFile, size, NULL, FILE_BEGIN) || !SetEndOfFile(hFile)) {
        vg_log("ERROR", "No se pudo establecer tamaño del archivo");
        CloseHandle(hFile);
        hFile = INVALID_HANDLE_VALUE;
        return 0;
    }
    
    /* Crear mapping */
    hMapFile = CreateFileMappingA(hFile,
                                  NULL,
                                  PAGE_READWRITE,
                                  0,
                                  BYTES,
                                  NULL);
    
    if (hMapFile == NULL) {
        vg_log("ERROR", "No se pudo crear file mapping");
        CloseHandle(hFile);
        hFile = INVALID_HANDLE_VALUE;
        return 0;
    }
    
    /* Mapear vista del archivo */
    img = (uint8_t*)MapViewOfFile(hMapFile,
                                  FILE_MAP_ALL_ACCESS,
                                  0,
                                  0,
                                  BYTES);
    
    if (img == NULL) {
        vg_log("ERROR", "No se pudo mapear archivo");
        CloseHandle(hMapFile);
        CloseHandle(hFile);
        hMapFile = NULL;
        hFile = INVALID_HANDLE_VALUE;
        return 0;
    }
    
#else
    /* Unix/Linux/macOS: usar mmap */
    fdimg = open(img_path, O_RDWR | O_CREAT, 0644);
    if (fdimg < 0) {
        vg_log("ERROR", "No se pudo abrir/crear %s", img_path);
        perror("open");
        return 0;
    }
    
    /* Reservar tamaño fijo */
    if (ftruncate(fdimg, BYTES) != 0) {
        vg_log("ERROR", "No se pudo establecer tamaño del archivo");
        perror("ftruncate");
        close(fdimg);
        fdimg = -1;
        return 0;
    }
    
    /* Mapear a memoria */
    img = mmap(NULL, BYTES, PROT_READ | PROT_WRITE,
               MAP_SHARED, fdimg, 0);
    if (img == MAP_FAILED) {
        vg_log("ERROR", "No se pudo mapear archivo a memoria");
        perror("mmap");
        close(fdimg);
        fdimg = -1;
        img = NULL;
        return 0;
    }
#endif
    
    initialized = 1;
    vg_log("INFO", "image.bin mapeado correctamente (%d bytes)", BYTES);
    return 1;
}

static inline void put_px(int x, int y, uint32_t rgb)
{
    if (!img || x < 0 || x >= W || y < 0 || y >= H) return;
    int idx = (y * W + x) * 3;
    img[idx + 0] = (rgb >> 16) & 0xFF;    /* R */
    img[idx + 1] = (rgb >>  8) & 0xFF;    /* G */
    img[idx + 2] =  rgb        & 0xFF;    /* B */
}

static inline void flush_buf(void)
{
    if (!img) return;
    
#ifdef PLATFORM_WINDOWS
    /* Windows: forzar escritura */
    if (!FlushViewOfFile(img, BYTES)) {
        vg_log("WARN", "FlushViewOfFile falló");
    }
    if (hFile != INVALID_HANDLE_VALUE && !FlushFileBuffers(hFile)) {
        vg_log("WARN", "FlushFileBuffers falló");
    }
#else
    /* Unix: msync */
    if (msync(img, BYTES, MS_SYNC) != 0) {
        vg_log("WARN", "msync falló");
    }
#endif
}

/* ───────── API invocada desde el IR ───────── */
void vg_clear(void)
{
    if (!init_buf()) {
        vg_log("ERROR", "No se pudo inicializar buffer en vg_clear");
        return;
    }
    memset(img, 0xFF, BYTES);  /* blanco */
    flush_buf();
}

void vg_set_color(uint32_t rgb) 
{ 
    CUR = rgb & 0x00FFFFFF;  /* Asegurar que solo usamos 24 bits */
}

void vg_draw_pixel(int x, int y)
{
    if (!init_buf()) {
        vg_log("ERROR", "No se pudo inicializar buffer en vg_draw_pixel");
        return;
    }
    put_px(x, y, CUR);
    flush_buf();
}

/* círculo relleno mediante scan-lines */
void vg_draw_circle(int cx, int cy, int r)
{
    if (!init_buf()) {
        vg_log("ERROR", "No se pudo inicializar buffer en vg_draw_circle");
        return;
    }
    
    if (r <= 0) return;

    int r2 = r * r;
    for (int dy = -r; dy <= r; ++dy)
    {
        int y = cy + dy;
        if (y < 0 || y >= H) continue;

        double dx_max_d = sqrt((double)(r2 - dy * dy));
        int dx_max = (int)(dx_max_d + 0.5);
        int x0 = cx - dx_max;
        int x1 = cx + dx_max;

        if (x0 < 0) x0 = 0;
        if (x1 >= W) x1 = W - 1;

        for (int x = x0; x <= x1; ++x)
            put_px(x, y, CUR);
    }
    flush_buf();
}

/* línea Bresenham */
void vg_draw_line(int x1, int y1, int x2, int y2)
{
    if (!init_buf()) {
        vg_log("ERROR", "No se pudo inicializar buffer en vg_draw_line");
        return;
    }

    int dx =  abs(x2 - x1), sx = x1 < x2 ?  1 : -1;
    int dy = -abs(y2 - y1), sy = y1 < y2 ?  1 : -1;
    int err = dx + dy;

    while (1)
    {
        put_px(x1, y1, CUR);
        if (x1 == x2 && y1 == y2) break;

        int e2 = 2 * err;
        if (e2 >= dy) { err += dy; x1 += sx; }
        if (e2 <= dx) { err += dx; y1 += sy; }
    }
    flush_buf();
}

/* rectángulo relleno */
void vg_draw_rect(int x1, int y1, int x2, int y2)
{
    if (!init_buf()) {
        vg_log("ERROR", "No se pudo inicializar buffer en vg_draw_rect");
        return;
    }

    if (x1 > x2) { int t = x1; x1 = x2; x2 = t; }
    if (y1 > y2) { int t = y1; y1 = y2; y2 = t; }

    if (x2 < 0 || x1 >= W || y2 < 0 || y1 >= H) return;

    if (x1 < 0) x1 = 0; if (x2 >= W) x2 = W - 1;
    if (y1 < 0) y1 = 0; if (y2 >= H) y2 = H - 1;

    for (int y = y1; y <= y2; ++y)
        for (int x = x1; x <= x2; ++x)
            put_px(x, y, CUR);

    flush_buf();
}

void vg_wait(int ms) 
{ 
    sleep_ms(ms); 
}

/* ───────── Funciones de información y debug ───────── */
void vg_get_info(void)
{
    vg_log("INFO", "VGraph Runtime Information");
    vg_log("INFO", "=========================");
#ifdef PLATFORM_WINDOWS
    vg_log("INFO", "Platform: Windows");
#elif defined(__APPLE__)
    vg_log("INFO", "Platform: macOS");
#else
    vg_log("INFO", "Platform: Linux/Unix");
#endif
    vg_log("INFO", "Frame buffer: %dx%d (%d bytes)", W, H, BYTES);
    vg_log("INFO", "Initialized: %s", initialized ? "Yes" : "No");
    if (initialized) {
        vg_log("INFO", "Image file: %s", img_path);
        vg_log("INFO", "Current color: 0x%06X", CUR);
    }
}

/* ───────── limpieza al salir ───────── */
static void close_buf(void)
{
    if (!initialized) return;
    
    if (img) {
#ifdef PLATFORM_WINDOWS
        if (!UnmapViewOfFile(img)) {
            vg_log("WARN", "UnmapViewOfFile falló");
        }
        if (hMapFile != NULL) {
            CloseHandle(hMapFile);
            hMapFile = NULL;
        }
        if (hFile != INVALID_HANDLE_VALUE) {
            CloseHandle(hFile);
            hFile = INVALID_HANDLE_VALUE;
        }
#else
        if (img != MAP_FAILED) {
            if (munmap(img, BYTES) != 0) {
                vg_log("WARN", "munmap falló");
            } else {
                vg_log("INFO", "image.bin desmapeado");
            }
        }
        if (fdimg >= 0) {
            close(fdimg);
            fdimg = -1;
        }
#endif
        img = NULL;
    }
    
    initialized = 0;
}

/* Funciones de inicialización y limpieza explícitas */
void vg_init(void)
{
    if (!initialized) {
        init_buf();
    }
}

void vg_cleanup(void)
{
    close_buf();
}

/* Constructor/Destructor automático */
#ifdef PLATFORM_WINDOWS
/* Windows DLL entry point para auto-inicialización */
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
    switch (fdwReason) {
        case DLL_PROCESS_DETACH:
            close_buf();
            break;
    }
    return TRUE;
}
#else
/* Unix constructor/destructor */
__attribute__((constructor))
static void vg_constructor(void)
{
    /* Inicialización automática opcional */
}

__attribute__((destructor))
static void vg_destructor(void)
{
    close_buf();
}
#endif