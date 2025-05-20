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

@"c" = global i32 16777215
@"x" = global double              0x0
@"y" = global double              0x0
@"t" = global double              0x0
define i32 @"main"()
{
entry:
  br label %"for.cond"
for.cond:
  %".3" = load double, double* @"t"
  %".4" = fcmp olt double %".3", 0x4076800000000000
  br i1 %".4", label %"for.body", label %"for.end"
for.body:
  %".6" = load double, double* @"t"
  %".7" = load double, double* @"t"
  %".8" = fmul double %".7", 0x400921ff2e48e8a7
  %".9" = fdiv double %".8", 0x4066800000000000
  %".10" = call double @"cos"(double %".9")
  %".11" = fmul double %".6", %".10"
  %".12" = fadd double 0x4074000000000000, %".11"
  store double %".12", double* @"x"
  %".14" = load double, double* @"t"
  %".15" = load double, double* @"t"
  %".16" = fmul double %".15", 0x400921ff2e48e8a7
  %".17" = fdiv double %".16", 0x4066800000000000
  %".18" = call double @"sin"(double %".17")
  %".19" = fmul double %".14", %".18"
  %".20" = fadd double 0x406e000000000000, %".19"
  store double %".20", double* @"y"
  %".22" = load double, double* @"t"
  %".23" = fmul double %".22", 0x4008000000000000
  %".24" = fcmp oeq double %".23",              0x0
  br i1 %".24", label %"then", label %"else"
for.incr:
  %".50" = load double, double* @"t"
  %".51" = fadd double %".50", 0x4014000000000000
  br label %"for.cond"
for.end:
  ret i32 0
then:
  store i32 16711680, i32* @"c"
  br label %"endif"
endif:
  %".37" = load i32, i32* @"c"
  call void @"vg_set_color"(i32 %".37")
  %".39" = load double, double* @"x"
  %".40" = fadd double %".39", 0x3fe0000000000000
  %".41" = fptosi double %".40" to i32
  %".42" = load double, double* @"y"
  %".43" = fadd double %".42", 0x3fe0000000000000
  %".44" = fptosi double %".43" to i32
  call void @"vg_draw_pixel"(i32 %".41", i32 %".44")
  %".46" = fadd double 0x3ff0000000000000, 0x3fe0000000000000
  %".47" = fptosi double %".46" to i32
  call void @"vg_wait"(i32 %".47")
  br label %"for.incr"
else:
  %".28" = load double, double* @"t"
  %".29" = fmul double %".28", 0x4008000000000000
  %".30" = fcmp oeq double %".29", 0x3ff0000000000000
  br i1 %".30", label %"then.1", label %"else.1"
then.1:
  store i32 255, i32* @"c"
  br label %"endif.1"
endif.1:
  br label %"endif"
else.1:
  store i32 65280, i32* @"c"
  br label %"endif.1"
}

define i32 @"_main"()
{
entry:
  %".2" = call i32 @"main"()
  ret i32 %".2"
}
