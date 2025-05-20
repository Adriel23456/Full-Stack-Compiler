/* runtime.c – VGraph stub runtime
 *
 *  • Framebuffer 800×600 RGB (24-bit) mapeado a out/image.bin
 *  • Todas las funciones escriben sobre ese mapeo
 */

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>     /* write, usleep   */
#include <fcntl.h>      /* open, O_* flags */
#include <sys/mman.h>   /* mmap, munmap    */
#include <sys/stat.h>   /* ftruncate       */

#define W 800
#define H 600
#define BYTES (W*H*3)

static uint8_t *img   = NULL;   /* framebuffer                     */
static int      fdimg = -1;     /* descriptor de out/image.bin     */
static uint32_t CUR   = 0x00FFFFFF;

/* ───────── helpers ───────── */
static void init_buf(void)
{
    if (img) return;                        /* ya inicializado */

    /* 1- abrir/crear archivo */
    if (access("out", F_OK) != 0)           /* asegurar dir ./out */
        mkdir("out", 0755);
    fdimg = open("out/image.bin",
                 O_RDWR | O_CREAT,
                 0644);
    if (fdimg < 0){ perror("open image.bin"); exit(1); }

    /* 2- reservar tamaño (si era nuevo) */
    if (ftruncate(fdimg, BYTES) != 0){
        perror("ftruncate"); exit(1);
    }

    /* 3- mapear a memoria */
    img = mmap(NULL, BYTES, PROT_READ | PROT_WRITE,
               MAP_SHARED, fdimg, 0);
    if (img == MAP_FAILED){
        perror("mmap"); exit(1);
    }
}

static inline void put_px(int x,int y,uint32_t rgb)
{
    if (x<0||x>=W||y<0||y>=H) return;
    int idx = (y*W + x)*3;
    img[idx+0] = (rgb>>16)&0xFF;   /* R */
    img[idx+1] = (rgb>>8 )&0xFF;   /* G */
    img[idx+2] =  rgb      &0xFF;  /* B */
}

static void flush_buf(void)
{
    /* msync fuerza la escritura en disco */
    msync(img, BYTES, MS_SYNC);
}

/* ───────── API que invoca el IR ───────── */
void vg_clear(void)
{
    init_buf();
    memset(img, 0xFF, BYTES);      /* blanco */
    flush_buf();
}

void vg_set_color(uint32_t rgb)
{
    CUR = rgb;
}

void vg_draw_pixel(int x,int y)
{
    init_buf();
    put_px(x,y,CUR);
    flush_buf();
}

/* stubs pendientes */
void vg_draw_circle(int cx,int cy,int r){ /* TODO */ }
void vg_draw_line  (int x1,int y1,int x2,int y2){ /* TODO */ }
void vg_draw_rect  (int x1,int y1,int x2,int y2){ /* TODO */ }

void vg_wait(int ms){ usleep(ms*1000); }

/* ───────── limpieza al salir ───────── */
__attribute__((destructor))
static void close_buf(void)
{
    if (img  && img != MAP_FAILED) munmap(img, BYTES);
    if (fdimg>=0) close(fdimg);
}