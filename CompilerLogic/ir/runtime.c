/* runtime.c – implementación mínima, *NO* optimizada. */
#include "runtime.h"
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#define WIDTH  800
#define HEIGHT 600

static uint8_t current_r = 0xFF, current_g = 0xFF, current_b = 0xFF; /* blanco */
static const char *BIN_PATH = "out/image.bin";

static FILE *open_bin(void) {
    FILE *f = fopen(BIN_PATH, "r+b");
    if (!f) {
        /* crea / limpia */
        f = fopen(BIN_PATH, "w+b");
        uint8_t white[WIDTH * HEIGHT * 3];
        memset(white, 0xFF, sizeof(white));
        fwrite(white, 1, sizeof(white), f);
    }
    return f;
}

static void plot(int x, int y) {
    if (x < 0 || x >= WIDTH || y < 0 || y >= HEIGHT) return;
    FILE *f = open_bin();
    if (!f) return;
    long pos = (y * WIDTH + x) * 3L;
    fseek(f, pos, SEEK_SET);
    fputc(current_r, f);
    fputc(current_g, f);
    fputc(current_b, f);
    fclose(f);
}

void vg_set_color(uint32_t rgb) {
    current_r = (rgb >> 16) & 0xFF;
    current_g = (rgb >> 8)  & 0xFF;
    current_b =  rgb        & 0xFF;
}

void vg_draw_pixel(int32_t x, int32_t y) {
    plot(x, y);
}

/*  Algoritmos triviales; optimízalos luego  */
void vg_draw_line(int32_t x1,int32_t y1,int32_t x2,int32_t y2) {
    int dx = abs(x2 - x1), dy = -abs(y2 - y1);
    int sx = x1 < x2 ? 1 : -1;
    int sy = y1 < y2 ? 1 : -1;
    int err = dx + dy;
    while (1) {
        plot(x1, y1);
        if (x1 == x2 && y1 == y2) break;
        int e2 = 2 * err;
        if (e2 >= dy) { err += dy; x1 += sx; }
        if (e2 <= dx) { err += dx; y1 += sy; }
    }
}

void vg_draw_circle(int32_t cx,int32_t cy,int32_t r) {
    int x = -r, y = 0, err = 2 - 2 * r;
    while (x <= 0) {
        for (int yi = y; yi >= -y; --yi) { /* círculo relleno */
            plot(cx - x, cy + yi);
            plot(cx + x, cy + yi);
        }
        int e2 = err;
        if (e2 <= y) err += ++y * 2 + 1;
        if (e2 >  x || err > y) err += ++x * 2 + 1;
    }
}

void vg_draw_rect(int32_t x1,int32_t y1,int32_t x2,int32_t y2) {
    if (x1 > x2) { int t = x1; x1 = x2; x2 = t; }
    if (y1 > y2) { int t = y1; y1 = y2; y2 = t; }
    for (int y = y1; y <= y2; ++y)
        for (int x = x1; x <= x2; ++x)
            plot(x, y);
}

void vg_clear(void) {
    FILE *f = fopen(BIN_PATH, "w+b");
    if (!f) return;
    uint8_t white[WIDTH * HEIGHT * 3];
    memset(white, 0xFF, sizeof(white));
    fwrite(white, 1, sizeof(white), f);
    fclose(f);
}

void vg_wait(int32_t ms) {
    struct timespec ts = { ms / 1000, (ms % 1000) * 1000000L };
    nanosleep(&ts, NULL);
}