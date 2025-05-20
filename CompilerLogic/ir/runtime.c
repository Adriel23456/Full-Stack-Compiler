/* runtime.c – runtime mínimo para VGraph
 *
 *  framebuffer RGB 24-bit de 800×600:
 *     – Se mapea sobre ./out/image.bin (se crea/trunca si no existe).
 *     – vg_clear() pone el buffer en blanco (0xFFFFFF).
 *     – vg_set_color() guarda el color actual.
 *     – vg_draw_pixel() escribe con clipping.
 *
 *  draw_circle / draw_line / draw_rect quedan todavía como TODO.
 */

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>

#include "runtime.h"
#include <newlib/sys/types.h>

#define W 800
#define H 600
#define IMG_SIZE (W * H * 3)
#define IMG_PATH "out/image.bin"

static uint8_t  *img   = NULL;       /* framebuffer mapeado        */
static uint32_t  CUR   = 0x00FFFFFF; /* color actual (RGB-888)      */

/*──────────────────── helpers ────────────────────*/
static void map_file(void)
{
    if (img) return;                     /* ya asignado */

    /* 1) asegurar directorio out/ */
    (void)mkdir("out", 0755);

    /* 2) abrir/crear archivo de imagen */
    int fd = open(IMG_PATH, O_RDWR | O_CREAT, 0644);
    if (fd < 0) { perror("open image.bin"); exit(EXIT_FAILURE); }

    /* 3) garantizar tamaño correcto */
    if (ftruncate(fd, IMG_SIZE) != 0) {
        perror("ftruncate image.bin");
        exit(EXIT_FAILURE);
    }

    /* 4) mapear con escritura compartida (cambios → disco) */
    img = mmap(NULL, IMG_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (img == MAP_FAILED) { perror("mmap image.bin"); exit(EXIT_FAILURE); }

    /* 5) cerrar fd (mapa sigue vivo) */
    close(fd);
}

static void put_px(int x, int y, uint32_t rgb)
{
    if (x < 0 || x >= W || y < 0 || y >= H) return;   /* clipping */
    size_t idx = (size_t)(y * W + x) * 3;
    img[idx + 0] = (rgb >> 16) & 0xFF;   /* R */
    img[idx + 1] = (rgb >>  8) & 0xFF;   /* G */
    img[idx + 2] =  rgb        & 0xFF;   /* B */
}

/*──────────────────── API ────────────────────────*/
void vg_clear(void)
{
    map_file();
    memset(img, 0xFF, IMG_SIZE);         /* blanco */
}

void vg_set_color(uint32_t rgb)
{
    map_file();
    CUR = rgb;
}

void vg_draw_pixel(int x, int y)
{
    map_file();
    put_px(x, y, CUR);
}

/*─── place-holders ───────────────────────────────*/
void vg_draw_circle(int cx, int cy, int r)  { (void)cx;(void)cy;(void)r; }
void vg_draw_line  (int x1,int y1,int x2,int y2){ (void)x1;(void)y1;(void)x2;(void)y2; }
void vg_draw_rect  (int x1,int y1,int x2,int y2){ (void)x1;(void)y1;(void)x2;(void)y2; }
void vg_wait(int ms){ usleep((useconds_t)ms * 1000); }