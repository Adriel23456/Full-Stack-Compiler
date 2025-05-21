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

@"activo" = global i1 0
@"visible" = global i1 0
@"parpadeo" = global i1 0
@"contador" = global double              0x0
@"colorLed" = global i32 16777215
define i32 @"main"()
{
entry:
  call void @"vg_clear"()
  store i1 true, i1* @"activo"
  store i1 false, i1* @"visible"
  store double              0x0, double* @"contador"
  store double              0x0, double* @"contador"
  br label %"for.cond"
for.cond:
  %".8" = load double, double* @"contador"
  %".9" = fcmp olt double %".8", 0x4024000000000000
  br i1 %".9", label %"for.body", label %"for.end"
for.body:
  %".11" = load double, double* @"contador"
  %".12" = fadd double %".11", 0x3fe0000000000000
  %".13" = fptosi double %".12" to i32
  %".14" = fadd double 0x4000000000000000, 0x3fe0000000000000
  %".15" = fptosi double %".14" to i32
  %".16" = srem i32 %".13", %".15"
  %".17" = sitofp i32 %".16" to double
  %".18" = fcmp oeq double %".17",              0x0
  store i1 %".18", i1* @"parpadeo"
  %".20" = load i1, i1* @"activo"
  %".21" = load i1, i1* @"parpadeo"
  %".22" = and i1 %".20", %".21"
  store i1 %".22", i1* @"visible"
  %".24" = load i1, i1* @"visible"
  br i1 %".24", label %"then", label %"else"
for.incr:
  %".49" = load double, double* @"contador"
  %".50" = fadd double %".49", 0x3ff0000000000000
  store double %".50", double* @"contador"
  br label %"for.cond"
for.end:
  ret i32 0
then:
  %".26" = load double, double* @"contador"
  %".27" = fcmp olt double %".26", 0x4014000000000000
  br i1 %".27", label %"then.1", label %"else.1"
endif:
  %".36" = load i32, i32* @"colorLed"
  call void @"vg_set_color"(i32 %".36")
  %".38" = fadd double 0x4072c00000000000, 0x3fe0000000000000
  %".39" = fptosi double %".38" to i32
  %".40" = fadd double 0x4072c00000000000, 0x3fe0000000000000
  %".41" = fptosi double %".40" to i32
  %".42" = fadd double 0x4049000000000000, 0x3fe0000000000000
  %".43" = fptosi double %".42" to i32
  call void @"vg_draw_circle"(i32 %".39", i32 %".41", i32 %".43")
  %".45" = fadd double 0x408f400000000000, 0x3fe0000000000000
  %".46" = fptosi double %".45" to i32
  call void @"vg_wait"(i32 %".46")
  br label %"for.incr"
else:
  store i32 0, i32* @"colorLed"
  br label %"endif"
then.1:
  store i32 255, i32* @"colorLed"
  br label %"endif.1"
endif.1:
  br label %"endif"
else.1:
  store i32 16776960, i32* @"colorLed"
  br label %"endif.1"
}

define i32 @"_main"()
{
entry:
  %".2" = call i32 @"main"()
  ret i32 %".2"
}
