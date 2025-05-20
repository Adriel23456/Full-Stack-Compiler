#ifndef VGRAPH_RUNTIME_H
#define VGRAPH_RUNTIME_H
#include <stdint.h>

/* Color actual (RGB – 0x00RRGGBB) */
void vg_set_color(uint32_t rgb);

/* Plot primitives – todas validan rango 0 ≤ x < 800, 0 ≤ y < 600 */
void vg_draw_pixel (int32_t x, int32_t y);
void vg_draw_line  (int32_t x1,int32_t y1,int32_t x2,int32_t y2);
void vg_draw_circle(int32_t cx,int32_t cy,int32_t r);
void vg_draw_rect  (int32_t x1,int32_t y1,int32_t x2,int32_t y2);

/* Miscelánea */
void vg_clear(void);               /* Rellena de blanco */
void vg_wait (int32_t ms);         /* Busy‑wait simple */

#endif /* VGRAPH_RUNTIME_H */