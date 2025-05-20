/* File: CompilerLogic/ir/runtime.c
   Extremely tiny software renderer that writes 800×600 RGB bytes
   into out/image.bin.  **Clipping** & **bounds check** inside helpers.
*/
#include "runtime.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <math.h>

#define W 800
#define H 600
#define BYTES (W*H*3)

static uint8_t *buf = NULL;
static uint32_t cur = 0x00FFFFFF;   /* default white */

/* ───────────────── helpers ───────────────── */
static inline int inside(int x,int y){ return x>=0 && x<W && y>=0 && y<H; }

static inline void putp(int x,int y){
    if(!inside(x,y)) return;
    size_t idx = (size_t)(y*W + x)*3;
    buf[idx+0] = (cur>>16)&0xFF;   /* R */
    buf[idx+1] = (cur>> 8)&0xFF;   /* G */
    buf[idx+2] =  cur     &0xFF;   /* B */
}

/* ───────────────── API ───────────────────── */
void vg_set_color(uint32_t rgb){ cur = rgb; }

void vg_draw_pixel(int x,int y){ putp(x,y); }

void vg_draw_circle(int cx,int cy,int r){
    for(int y=-r; y<=r; ++y)
        for(int x=-r; x<=r; ++x)
            if(x*x + y*y <= r*r) putp(cx+x, cy+y);
}

void vg_draw_line(int x1,int y1,int x2,int y2){
    /* Bresenham + 2-px thickness */
    int dx = abs(x2-x1), sx = x1<x2?1:-1;
    int dy =-abs(y2-y1), sy = y1<y2?1:-1;
    int err = dx+dy, e2;
    while(1){
        for(int ox=-1;ox<=0;++ox)for(int oy=-1;oy<=0;++oy) putp(x1+ox,y1+oy);
        if(x1==x2 && y1==y2) break;
        e2 = 2*err;
        if(e2>=dy){ err+=dy; x1+=sx; }
        if(e2<=dx){ err+=dx; y1+=sy; }
    }
}

void vg_draw_rect(int x1,int y1,int x2,int y2){
    if(x2<x1){ int t=x1; x1=x2; x2=t; }
    if(y2<y1){ int t=y1; y1=y2; y2=t; }
    for(int y=y1;y<=y2;++y)
        for(int x=x1;x<=x2;++x)
            putp(x,y);
}

void vg_clear(void){ memset(buf, 0xFF, BYTES); }

void vg_wait(int ms){ usleep(ms*1000); }

/* ───────────────── mmap buffer on load ───── */
__attribute__((constructor))
static void rt_init(void){
    int fd = open("out/image.bin", O_RDWR | O_CREAT, 0666);
    ftruncate(fd, BYTES);
    buf = mmap(NULL, BYTES, PROT_WRITE|PROT_READ, MAP_SHARED, fd, 0);
}