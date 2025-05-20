/* File: CompilerLogic/ir/runtime.h */
#ifndef VGRAPH_RUNTIME_H
#define VGRAPH_RUNTIME_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

void vg_set_color(uint32_t rgb);

void vg_draw_pixel(int x, int y);
void vg_draw_circle(int cx, int cy, int r);
void vg_draw_line(int x1, int y1, int x2, int y2);
void vg_draw_rect(int x1, int y1, int x2, int y2);

void vg_clear(void);
void vg_wait(int ms);

#ifdef __cplusplus
}
#endif

#endif /* VGRAPH_RUNTIME_H */