; ModuleID = "vgraph"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare void @"vg_set_color"(i32 %".1")

declare void @"vg_draw_pixel"(i32 %".1", i32 %".2")

declare void @"vg_draw_circle"(i32 %".1", i32 %".2", i32 %".3")

declare void @"vg_draw_line"(i32 %".1", i32 %".2", i32 %".3", i32 %".4")

declare void @"vg_draw_rect"(i32 %".1", i32 %".2", i32 %".3", i32 %".4")

declare void @"vg_clear"()

declare void @"vg_wait"(i32 %".1")

declare double @"cos"(double %".1")

declare double @"sin"(double %".1")

@"x1" = global double              0x0
@"y1" = global double              0x0
@"x2" = global double              0x0
@"y2" = global double              0x0
@"a1" = global i1 0
@"b1" = global i1 0
@"c1" = global i1 0
@"c" = global i32 16777215
define i32 @"main"()
{
entry:
  store i32 16711680, i32* @"c"
  store double 0x3ff0000000000000, double* @"x1"
  store double 0x3ff0000000000000, double* @"y1"
  store double 0x4024000000000000, double* @"x2"
  store double 0x4039000000000000, double* @"y2"
  call void @"vg_clear"()
  %".8" = load i32, i32* @"c"
  call void @"vg_set_color"(i32 %".8")
  %".10" = load double, double* @"x1"
  %".11" = fadd double %".10", 0x3fe0000000000000
  %".12" = fptosi double %".11" to i32
  %".13" = load double, double* @"y1"
  %".14" = fadd double %".13", 0x3fe0000000000000
  %".15" = fptosi double %".14" to i32
  call void @"vg_draw_pixel"(i32 %".12", i32 %".15")
  %".17" = load double, double* @"x1"
  %".18" = fadd double %".17", 0x3ff0000000000000
  %".19" = fmul double %".18", 0x4034000000000000
  %".20" = fadd double %".19", 0x3fe0000000000000
  %".21" = fptosi double %".20" to i32
  %".22" = load double, double* @"y1"
  %".23" = fadd double %".22", 0x4000000000000000
  %".24" = fmul double %".23", 0x4034000000000000
  %".25" = fadd double %".24", 0x3fe0000000000000
  %".26" = fptosi double %".25" to i32
  call void @"vg_draw_pixel"(i32 %".21", i32 %".26")
  ret i32 0
}

define i32 @"_main"()
{
entry:
  %".2" = call i32 @"main"()
  ret i32 %".2"
}
