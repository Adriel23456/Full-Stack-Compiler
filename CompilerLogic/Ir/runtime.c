/* runtime.c – VGraph stub runtime
 *
 *  • Frame-buffer 800×600 RGB (24-bit) mapeado a out/image.bin
 *  • Todas las funciones escriben sobre ese mapeo y lo sincronizan
 *    con disco mediante msync().
 */

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>     /* write, usleep         */
#include <fcntl.h>      /* open, O_* flags       */
#include <sys/mman.h>   /* mmap, munmap, msync   */
#include <sys/stat.h>   /* ftruncate             */
#include <math.h>       /* sqrt, abs             */

#define W 800
#define H 600
#define BYTES (W * H * 3)

static uint8_t *img   = NULL;      /* frame-buffer                   */
static int      fdimg = -1;        /* descriptor de out/image.bin    */
static uint32_t CUR   = 0x00FFFFFF;

/* ───────── helpers ───────── */
static void init_buf(void)
{
    if (img) return;                          /* ya inicializado */

    /* 1- asegúrate de que exista ./out                       */
    if (access("out", F_OK) != 0)
        mkdir("out", 0755);

    /* 2- abre/crea archivo binario de imagen                 */
    fdimg = open("out/image.bin", O_RDWR | O_CREAT, 0644);
    if (fdimg < 0) { perror("open image.bin"); exit(1); }

    /* 3- reserva tamaño fijo                                 */
    if (ftruncate(fdimg, BYTES) != 0) {
        perror("ftruncate"); exit(1);
    }

    /* 4- mapea a memoria                                     */
    img = mmap(NULL, BYTES, PROT_READ | PROT_WRITE,
               MAP_SHARED, fdimg, 0);
    if (img == MAP_FAILED) {
        perror("mmap"); exit(1);
    }
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
    /* fuerza escritura en disco (modo síncrono) */
    msync(img, BYTES, MS_SYNC);
}

/* ───────── API invocada desde el IR ───────── */
void vg_clear(void)
{
    init_buf();
    memset(img, 0xFF, BYTES);               /* blanco */
    flush_buf();
}

void vg_set_color(uint32_t rgb) { CUR = rgb; }

void vg_draw_pixel(int x, int y)
{
    init_buf();
    put_px(x, y, CUR);
    flush_buf();
}

/* ───────── nuevas primitivas ───────── */

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

void vg_wait(int ms) { usleep(ms * 1000); }

/* ───────── limpieza al salir ───────── */
__attribute__((destructor))
static void close_buf(void)
{
    if (img  && img != MAP_FAILED) munmap(img, BYTES);
    if (fdimg >= 0) close(fdimg);
}