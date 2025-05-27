/* File: CompilerLogic/ir/runtime.h
 * VGraph Runtime Library Header
 * Cross-platform compatible (Windows/Linux/MacOS)
 */

#ifndef VGRAPH_RUNTIME_H
#define VGRAPH_RUNTIME_H

#include <stdint.h>

/* Platform detection for proper calling conventions */
#if defined(_WIN32) || defined(_WIN64) || defined(__CYGWIN__) || defined(__MINGW32__) || defined(__MINGW64__)
    #define VGRAPH_PLATFORM_WINDOWS
    
    /* Windows calling convention */
    #ifdef VGRAPH_BUILD_DLL
        #define VGRAPH_API __declspec(dllexport)
    #elif defined(VGRAPH_USE_DLL)
        #define VGRAPH_API __declspec(dllimport)
    #else
        #define VGRAPH_API
    #endif
    
    /* Windows calling convention */
    #define VGRAPH_CALL __cdecl
    
#else
    #define VGRAPH_PLATFORM_UNIX
    
    /* Unix calling convention */
    #define VGRAPH_API __attribute__((visibility("default")))
    #define VGRAPH_CALL
    
#endif

/* C++ compatibility */
#ifdef __cplusplus
extern "C" {
#endif

/* VGraph Runtime API */

/**
 * Set the current drawing color
 * @param rgb Color in RGB format (24-bit, 0x00RRGGBB)
 */
VGRAPH_API void VGRAPH_CALL vg_set_color(uint32_t rgb);

/**
 * Draw a single pixel at the specified coordinates
 * @param x X coordinate (0-799)
 * @param y Y coordinate (0-599)
 */
VGRAPH_API void VGRAPH_CALL vg_draw_pixel(int x, int y);

/**
 * Draw a filled circle
 * @param cx Center X coordinate
 * @param cy Center Y coordinate
 * @param r Radius in pixels
 */
VGRAPH_API void VGRAPH_CALL vg_draw_circle(int cx, int cy, int r);

/**
 * Draw a line between two points
 * @param x1 Start X coordinate
 * @param y1 Start Y coordinate
 * @param x2 End X coordinate
 * @param y2 End Y coordinate
 */
VGRAPH_API void VGRAPH_CALL vg_draw_line(int x1, int y1, int x2, int y2);

/**
 * Draw a filled rectangle
 * @param x1 Top-left X coordinate
 * @param y1 Top-left Y coordinate
 * @param x2 Bottom-right X coordinate
 * @param y2 Bottom-right Y coordinate
 */
VGRAPH_API void VGRAPH_CALL vg_draw_rect(int x1, int y1, int x2, int y2);

/**
 * Clear the entire frame buffer to white
 */
VGRAPH_API void VGRAPH_CALL vg_clear(void);

/**
 * Wait/pause execution for the specified number of milliseconds
 * @param ms Number of milliseconds to wait
 */
VGRAPH_API void VGRAPH_CALL vg_wait(int ms);

/**
 * Initialize the VGraph runtime (optional, called automatically)
 */
VGRAPH_API void VGRAPH_CALL vg_init(void);

/**
 * Clean up VGraph runtime resources (optional, called automatically)
 */
VGRAPH_API void VGRAPH_CALL vg_cleanup(void);

/**
 * Print runtime information to console (debug function)
 */
VGRAPH_API void VGRAPH_CALL vg_get_info(void);

/* Constants */
#define VGRAPH_WIDTH  800
#define VGRAPH_HEIGHT 600
#define VGRAPH_BYTES  (VGRAPH_WIDTH * VGRAPH_HEIGHT * 3)

/* Predefined colors (24-bit RGB) */
#define VGRAPH_COLOR_BLACK   0x000000
#define VGRAPH_COLOR_WHITE   0xFFFFFF
#define VGRAPH_COLOR_RED     0xFF0000
#define VGRAPH_COLOR_GREEN   0x00FF00
#define VGRAPH_COLOR_BLUE    0x0000FF
#define VGRAPH_COLOR_YELLOW  0xFFFF00
#define VGRAPH_COLOR_CYAN    0x00FFFF
#define VGRAPH_COLOR_MAGENTA 0xFF00FF
#define VGRAPH_COLOR_BROWN   0x800000

/* Utility macros */
#define VGRAPH_RGB(r,g,b) (((r) << 16) | ((g) << 8) | (b))
#define VGRAPH_GET_RED(rgb)   (((rgb) >> 16) & 0xFF)
#define VGRAPH_GET_GREEN(rgb) (((rgb) >> 8) & 0xFF)
#define VGRAPH_GET_BLUE(rgb)  ((rgb) & 0xFF)

/* Version information */
#define VGRAPH_VERSION_MAJOR 1
#define VGRAPH_VERSION_MINOR 0
#define VGRAPH_VERSION_PATCH 0
#define VGRAPH_VERSION_STRING "1.0.0"

#ifdef __cplusplus
}
#endif

#endif /* VGRAPH_RUNTIME_H */