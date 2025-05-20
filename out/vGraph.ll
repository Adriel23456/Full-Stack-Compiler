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
  call void @"vg_clear"()
  store double              0x0, double* @"t"
  br label %"for.cond"
for.cond:
  %".5" = load double, double* @"t"
  %".6" = fmul double 0x4076800000000000, 0x4000000000000000
  %".7" = fcmp olt double %".5", %".6"
  br i1 %".7", label %"for.body", label %"for.end"
for.body:
  %".9" = load double, double* @"t"
  %".10" = load double, double* @"t"
  %".11" = fmul double %".10", 0x400921ff2e48e8a7
  %".12" = fdiv double %".11", 0x4066800000000000
  %".13" = call double @"cos"(double %".12")
  %".14" = fmul double %".9", %".13"
  %".15" = fadd double 0x4074000000000000, %".14"
  store double %".15", double* @"x"
  %".17" = load double, double* @"t"
  %".18" = load double, double* @"t"
  %".19" = fmul double %".18", 0x400921ff2e48e8a7
  %".20" = fdiv double %".19", 0x4066800000000000
  %".21" = call double @"sin"(double %".20")
  %".22" = fmul double %".17", %".21"
  %".23" = fadd double 0x406e000000000000, %".22"
  store double %".23", double* @"y"
  %".25" = load double, double* @"t"
  %".26" = fadd double %".25", 0x3fe0000000000000
  %".27" = fptosi double %".26" to i32
  %".28" = fadd double 0x4008000000000000, 0x3fe0000000000000
  %".29" = fptosi double %".28" to i32
  %".30" = srem i32 %".27", %".29"
  %".31" = sitofp i32 %".30" to double
  %".32" = fcmp oeq double %".31",              0x0
  br i1 %".32", label %"then", label %"else"
for.incr:
  %".113" = load double, double* @"t"
  %".114" = fadd double %".113", 0x4014000000000000
  store double %".114", double* @"t"
  br label %"for.cond"
for.end:
  ret i32 0
then:
  store i32 16711680, i32* @"c"
  br label %"endif"
endif:
  %".50" = load i32, i32* @"c"
  call void @"vg_set_color"(i32 %".50")
  %".52" = load double, double* @"x"
  %".53" = fadd double %".52", 0x3fe0000000000000
  %".54" = fptosi double %".53" to i32
  %".55" = load double, double* @"y"
  %".56" = fadd double %".55", 0x3fe0000000000000
  %".57" = fptosi double %".56" to i32
  call void @"vg_draw_pixel"(i32 %".54", i32 %".57")
  %".59" = load double, double* @"x"
  %".60" = fadd double %".59", 0x3ff0000000000000
  %".61" = fadd double %".60", 0x3fe0000000000000
  %".62" = fptosi double %".61" to i32
  %".63" = load double, double* @"y"
  %".64" = fadd double %".63", 0x3ff0000000000000
  %".65" = fadd double %".64", 0x3fe0000000000000
  %".66" = fptosi double %".65" to i32
  call void @"vg_draw_pixel"(i32 %".62", i32 %".66")
  %".68" = load double, double* @"x"
  %".69" = fadd double %".68", 0x3ff0000000000000
  %".70" = fadd double %".69", 0x3fe0000000000000
  %".71" = fptosi double %".70" to i32
  %".72" = load double, double* @"y"
  %".73" = fadd double %".72", 0x3fe0000000000000
  %".74" = fptosi double %".73" to i32
  call void @"vg_draw_pixel"(i32 %".71", i32 %".74")
  %".76" = load double, double* @"x"
  %".77" = fadd double %".76", 0x3fe0000000000000
  %".78" = fptosi double %".77" to i32
  %".79" = load double, double* @"y"
  %".80" = fadd double %".79", 0x3ff0000000000000
  %".81" = fadd double %".80", 0x3fe0000000000000
  %".82" = fptosi double %".81" to i32
  call void @"vg_draw_pixel"(i32 %".78", i32 %".82")
  %".84" = load double, double* @"x"
  %".85" = fsub double %".84", 0x3ff0000000000000
  %".86" = fadd double %".85", 0x3fe0000000000000
  %".87" = fptosi double %".86" to i32
  %".88" = load double, double* @"y"
  %".89" = fsub double %".88", 0x3ff0000000000000
  %".90" = fadd double %".89", 0x3fe0000000000000
  %".91" = fptosi double %".90" to i32
  call void @"vg_draw_pixel"(i32 %".87", i32 %".91")
  %".93" = load double, double* @"x"
  %".94" = fsub double %".93", 0x3ff0000000000000
  %".95" = fadd double %".94", 0x3fe0000000000000
  %".96" = fptosi double %".95" to i32
  %".97" = load double, double* @"y"
  %".98" = fadd double %".97", 0x3fe0000000000000
  %".99" = fptosi double %".98" to i32
  call void @"vg_draw_pixel"(i32 %".96", i32 %".99")
  %".101" = load double, double* @"x"
  %".102" = fadd double %".101", 0x3fe0000000000000
  %".103" = fptosi double %".102" to i32
  %".104" = load double, double* @"y"
  %".105" = fsub double %".104", 0x3ff0000000000000
  %".106" = fadd double %".105", 0x3fe0000000000000
  %".107" = fptosi double %".106" to i32
  call void @"vg_draw_pixel"(i32 %".103", i32 %".107")
  %".109" = fadd double 0x4059000000000000, 0x3fe0000000000000
  %".110" = fptosi double %".109" to i32
  call void @"vg_wait"(i32 %".110")
  br label %"for.incr"
else:
  %".36" = load double, double* @"t"
  %".37" = fadd double %".36", 0x3fe0000000000000
  %".38" = fptosi double %".37" to i32
  %".39" = fadd double 0x4008000000000000, 0x3fe0000000000000
  %".40" = fptosi double %".39" to i32
  %".41" = srem i32 %".38", %".40"
  %".42" = sitofp i32 %".41" to double
  %".43" = fcmp oeq double %".42", 0x3ff0000000000000
  br i1 %".43", label %"then.1", label %"else.1"
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
