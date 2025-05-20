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

@"x" = global double              0x0
@"y1" = global double              0x0
@"a1" = global i1 0
@"b1" = global i1 0
@"c1" = global i1 0
@"c" = global i32 16777215
define i32 @"main"()
{
entry:
  store i1 true, i1* @"a1"
  store i1 true, i1* @"b1"
  store i1 false, i1* @"c1"
  store i32 16711680, i32* @"c"
  %".6" = fdiv double 0x4000000000000000, 0x4000000000000000
  %".7" = fmul double %".6", 0x402e000000000000
  %".8" = fadd double 0x4014000000000000, %".7"
  store double %".8", double* @"x"
  ret i32 0
}

define i32 @"_main"()
{
entry:
  %".2" = call i32 @"main"()
  ret i32 %".2"
}
