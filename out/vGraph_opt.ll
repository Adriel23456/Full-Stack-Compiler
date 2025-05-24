; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@x1 = local_unnamed_addr global double 0.000000e+00
@y1 = local_unnamed_addr global double 0.000000e+00
@x2 = local_unnamed_addr global double 0.000000e+00
@y2 = local_unnamed_addr global double 0.000000e+00
@a1 = local_unnamed_addr global i1 false
@b1 = local_unnamed_addr global i1 false
@c1 = local_unnamed_addr global i1 false
@c = local_unnamed_addr global i32 16777215

declare void @vg_set_color(i32) local_unnamed_addr

declare void @vg_draw_pixel(i32, i32) local_unnamed_addr

declare void @vg_clear() local_unnamed_addr

define i32 @main() local_unnamed_addr {
entry:
  store i32 16711680, i32* @c, align 4
  store double 1.000000e+00, double* @x1, align 8
  store double 1.000000e+00, double* @y1, align 8
  store double 1.000000e+01, double* @x2, align 8
  store double 2.500000e+01, double* @y2, align 8
  tail call void @vg_clear()
  %.8 = load i32, i32* @c, align 4
  tail call void @vg_set_color(i32 %.8)
  %.10 = load double, double* @x1, align 8
  %.11 = fadd double %.10, 5.000000e-01
  %.12 = fptosi double %.11 to i32
  %.13 = load double, double* @y1, align 8
  %.14 = fadd double %.13, 5.000000e-01
  %.15 = fptosi double %.14 to i32
  tail call void @vg_draw_pixel(i32 %.12, i32 %.15)
  %.17 = load double, double* @x1, align 8
  %.18 = fadd double %.17, 1.000000e+00
  %.19 = fmul double %.18, 2.000000e+01
  %.20 = fadd double %.19, 5.000000e-01
  %.21 = fptosi double %.20 to i32
  %.22 = load double, double* @y1, align 8
  %.23 = fadd double %.22, 2.000000e+00
  %.24 = fmul double %.23, 2.000000e+01
  %.25 = fadd double %.24, 5.000000e-01
  %.26 = fptosi double %.25 to i32
  tail call void @vg_draw_pixel(i32 %.21, i32 %.26)
  ret i32 0
}

define i32 @_main() local_unnamed_addr {
entry:
  store i32 16711680, i32* @c, align 4
  store double 1.000000e+00, double* @x1, align 8
  store double 1.000000e+00, double* @y1, align 8
  store double 1.000000e+01, double* @x2, align 8
  store double 2.500000e+01, double* @y2, align 8
  tail call void @vg_clear()
  %.8.i = load i32, i32* @c, align 4
  tail call void @vg_set_color(i32 %.8.i)
  %.10.i = load double, double* @x1, align 8
  %.11.i = fadd double %.10.i, 5.000000e-01
  %.12.i = fptosi double %.11.i to i32
  %.13.i = load double, double* @y1, align 8
  %.14.i = fadd double %.13.i, 5.000000e-01
  %.15.i = fptosi double %.14.i to i32
  tail call void @vg_draw_pixel(i32 %.12.i, i32 %.15.i)
  %.17.i = load double, double* @x1, align 8
  %.18.i = fadd double %.17.i, 1.000000e+00
  %.19.i = fmul double %.18.i, 2.000000e+01
  %.20.i = fadd double %.19.i, 5.000000e-01
  %.21.i = fptosi double %.20.i to i32
  %.22.i = load double, double* @y1, align 8
  %.23.i = fadd double %.22.i, 2.000000e+00
  %.24.i = fmul double %.23.i, 2.000000e+01
  %.25.i = fadd double %.24.i, 5.000000e-01
  %.26.i = fptosi double %.25.i to i32
  tail call void @vg_draw_pixel(i32 %.21.i, i32 %.26.i)
  ret i32 0
}
