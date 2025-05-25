/* runtime.c – VGraph runtime portable
 *
 *  • Frame-buffer 800×600 RGB (24-bit) mapeado a image.bin
 *  • Busca image.bin en el mismo directorio que el ejecutable
 *  • Compatible con Linux, macOS, Windows (via MinGW/Cygwin)
 */

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>       /* sqrt, abs */

/* Detección de plataforma */
#ifdef _WIN32
    #include <windows.h>
    #define PATH_SEPARATOR "\\"
#else
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
static int      fdimg    = -1;          /* descriptor de image.bin */
static uint32_t CUR      = 0x00FFFFFF;  /* color actual */
static char     img_path[PATH_MAX];     /* ruta completa a image.bin */

#ifdef _WIN32
static HANDLE hMapFile = NULL;
static HANDLE hFile = INVALID_HANDLE_VALUE;
#endif

/* ───────── Funciones auxiliares ───────── */

/* Obtiene el directorio donde se encuentra el ejecutable (multi-plataforma) */
static void get_executable_dir(char *dir, size_t size)
{
    char path[PATH_MAX];
    
#ifdef _WIN32
    /* Windows */
    DWORD len = GetModuleFileNameA(NULL, path, sizeof(path));
    if (len > 0 && len < sizeof(path)) {
        /* Eliminar el nombre del ejecutable para obtener solo el directorio */
        char *last_sep = strrchr(path, '\\');
        if (last_sep) {
            *last_sep = '\0';
        }
        strncpy(dir, path, size - 1);
        dir[size - 1] = '\0';
        return;
    }
    
#elif defined(__APPLE__)
    /* macOS */
    uint32_t bufsize = sizeof(path);
    if (_NSGetExecutablePath(path, &bufsize) == 0) {
        char *dir_path = dirname(path);
        strncpy(dir, dir_path, size - 1);
        dir[size - 1] = '\0';
        return;
    }
    
#elif defined(__linux__)
    /* Linux */
    ssize_t len = readlink("/proc/self/exe", path, sizeof(path) - 1);
    if (len != -1) {
        path[len] = '\0';
        char *dir_path = dirname(path);
        strncpy(dir, dir_path, size - 1);
        dir[size - 1] = '\0';
        return;
    }
#endif
    
    /* Fallback: usar directorio actual */
    #ifdef _WIN32
        GetCurrentDirectoryA(size, dir);
    #else
        if (getcwd(dir, size) == NULL) {
            strncpy(dir, ".", size - 1);
            dir[size - 1] = '\0';
        }
    #endif
}

/* Función para dormir (multi-plataforma) */
static void sleep_ms(int ms)
{
#ifdef _WIN32
    Sleep(ms);
#else
    usleep(ms * 1000);
#endif
}

static void init_buf(void)
{
    if (img) return;  /* ya inicializado */
    
    char exe_dir[PATH_MAX];
    
    /* Obtener directorio del ejecutable */
    get_executable_dir(exe_dir, sizeof(exe_dir));
    
    /* Construir path completo a image.bin */
    snprintf(img_path, sizeof(img_path), "%s%simage.bin", exe_dir, PATH_SEPARATOR);
    
    printf("[VGraph] Ejecutable en: %s\n", exe_dir);
    printf("[VGraph] Usando image.bin en: %s\n", img_path);
    
#ifdef _WIN32
    /* Windows: usar CreateFile y CreateFileMapping */
    hFile = CreateFileA(img_path,
                        GENERIC_READ | GENERIC_WRITE,
                        FILE_SHARE_READ | FILE_SHARE_WRITE,
                        NULL,
                        OPEN_ALWAYS,
                        FILE_ATTRIBUTE_NORMAL,
                        NULL);
    
    if (hFile == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "[VGraph] Error: No se pudo abrir/crear %s\n", img_path);
        exit(1);
    }
    
    /* Establecer tamaño del archivo */
    LARGE_INTEGER size;
    size.QuadPart = BYTES;
    SetFilePointerEx(hFile, size, NULL, FILE_BEGIN);
    SetEndOfFile(hFile);
    
    /* Crear mapping */
    hMapFile = CreateFileMappingA(hFile,
                                  NULL,
                                  PAGE_READWRITE,
                                  0,
                                  BYTES,
                                  NULL);
    
    if (hMapFile == NULL) {
        fprintf(stderr, "[VGraph] Error: No se pudo crear file mapping\n");
        CloseHandle(hFile);
        exit(1);
    }
    
    /* Mapear vista del archivo */
    img = (uint8_t*)MapViewOfFile(hMapFile,
                                  FILE_MAP_ALL_ACCESS,
                                  0,
                                  0,
                                  BYTES);
    
    if (img == NULL) {
        fprintf(stderr, "[VGraph] Error: No se pudo mapear archivo\n");
        CloseHandle(hMapFile);
        CloseHandle(hFile);
        exit(1);
    }
    
#else
    /* Unix/Linux/macOS: usar mmap */
    fdimg = open(img_path, O_RDWR | O_CREAT, 0644);
    if (fdimg < 0) {
        fprintf(stderr, "[VGraph] Error: No se pudo abrir/crear %s\n", img_path);
        perror("open");
        exit(1);
    }
    
    /* Reservar tamaño fijo */
    if (ftruncate(fdimg, BYTES) != 0) {
        perror("ftruncate");
        exit(1);
    }
    
    /* Mapear a memoria */
    img = mmap(NULL, BYTES, PROT_READ | PROT_WRITE,
               MAP_SHARED, fdimg, 0);
    if (img == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }
#endif
    
    printf("[VGraph] image.bin mapeado correctamente (%d bytes)\n", BYTES);
}

static inline void put_px(int x, int y, uint32_t rgb)
{
    if (x < 0 || x >= W || y < 0 || y >= H) return;
    int idx = (y * W + x) * 3;
    img[idx + 0] = (rgb >> 16) & 0xFF;    /* R */
    img[idx + 1] = (rgb >>  8) & 0xFF;    /* G */
    img[idx + 2] =  rgb        & 0xFF;    /* B */
}

static inline void flush_buf(void)
{
#ifdef _WIN32
    /* Windows: forzar escritura */
    FlushViewOfFile(img, BYTES);
    FlushFileBuffers(hFile);
#else
    /* Unix: msync */
    msync(img, BYTES, MS_SYNC);
#endif
}

/* ───────── API invocada desde el IR ───────── */
void vg_clear(void)
{
    init_buf();
    memset(img, 0xFF, BYTES);  /* blanco */
    flush_buf();
}

void vg_set_color(uint32_t rgb) { CUR = rgb; }

void vg_draw_pixel(int x, int y)
{
    init_buf();
    put_px(x, y, CUR);
    flush_buf();
}

/* círculo relleno mediante scan-lines */
void vg_draw_circle(int cx, int cy, int r)
{
    init_buf();
    if (r <= 0) return;

    int r2 = r * r;
    for (int dy = -r; dy <= r; ++dy)
    {
        int y = cy + dy;
        if (y < 0 || y >= H) continue;

        int dx_max = (int)(sqrt((double)(r2 - dy * dy)) + 0.5);
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
    init_buf();

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
    init_buf();

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

void vg_wait(int ms) { sleep_ms(ms); }

/* ───────── limpieza al salir ───────── */
__attribute__((destructor))
static void close_buf(void)
{
    if (img) {
#ifdef _WIN32
        UnmapViewOfFile(img);
        if (hMapFile != NULL) CloseHandle(hMapFile);
        if (hFile != INVALID_HANDLE_VALUE) CloseHandle(hFile);
#else
        if (img != MAP_FAILED) {
            munmap(img, BYTES);
            printf("[VGraph] image.bin desmapeado\n");
        }
        if (fdimg >= 0) close(fdimg);
#endif
        img = NULL;
    }
}