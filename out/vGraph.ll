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
@"y" = global double              0x0
@"t" = global double              0x0
@"c" = global i32 16777215
define i32 @"main"()
{
entry:
  call void @"vg_clear"()
  store double              0x0, double* @"t"
  br label %"for.cond"
for.cond:
  %".5" = load double, double* @"t"
  %".6" = fcmp olt double %".5", 0x4076800000000000
  br i1 %".6", label %"for.body", label %"for.end"
for.body:
  %".8" = load double, double* @"t"
  %".9" = load double, double* @"t"
  %".10" = fmul double %".9", 0x400921ff2e48e8a7
  %".11" = fdiv double %".10", 0x4066800000000000
  %".12" = call double @"cos"(double %".11")
  %".13" = fmul double %".8", %".12"
  %".14" = fadd double 0x4074000000000000, %".13"
  store double %".14", double* @"x"
  %".16" = load double, double* @"t"
  %".17" = load double, double* @"t"
  %".18" = fmul double %".17", 0x400921ff2e48e8a7
  %".19" = fdiv double %".18", 0x4066800000000000
  %".20" = call double @"sin"(double %".19")
  %".21" = fmul double %".16", %".20"
  %".22" = fadd double 0x406e000000000000, %".21"
  store double %".22", double* @"y"
  %".24" = load double, double* @"t"
  %".25" = fadd double %".24", 0x3fe0000000000000
  %".26" = fptosi double %".25" to i32
  %".27" = fadd double 0x4008000000000000, 0x3fe0000000000000
  %".28" = fptosi double %".27" to i32
  %".29" = srem i32 %".26", %".28"
  %".30" = sitofp i32 %".29" to double
  %".31" = fcmp oeq double %".30",              0x0
  br i1 %".31", label %"then", label %"else"
for.incr:
  %".112" = load double, double* @"t"
  %".113" = fadd double %".112", 0x4014000000000000
  store double %".113", double* @"t"
  br label %"for.cond"
for.end:
  ret i32 0
then:
  store i32 16711680, i32* @"c"
  br label %"endif"
endif:
  %".49" = load i32, i32* @"c"
  call void @"vg_set_color"(i32 %".49")
  %".51" = load double, double* @"x"
  %".52" = fadd double %".51", 0x3fe0000000000000
  %".53" = fptosi double %".52" to i32
  %".54" = load double, double* @"y"
  %".55" = fadd double %".54", 0x3fe0000000000000
  %".56" = fptosi double %".55" to i32
  call void @"vg_draw_pixel"(i32 %".53", i32 %".56")
  %".58" = load double, double* @"x"
  %".59" = fadd double %".58", 0x3ff0000000000000
  %".60" = fadd double %".59", 0x3fe0000000000000
  %".61" = fptosi double %".60" to i32
  %".62" = load double, double* @"y"
  %".63" = fadd double %".62", 0x3ff0000000000000
  %".64" = fadd double %".63", 0x3fe0000000000000
  %".65" = fptosi double %".64" to i32
  call void @"vg_draw_pixel"(i32 %".61", i32 %".65")
  %".67" = load double, double* @"x"
  %".68" = fadd double %".67", 0x3ff0000000000000
  %".69" = fadd double %".68", 0x3fe0000000000000
  %".70" = fptosi double %".69" to i32
  %".71" = load double, double* @"y"
  %".72" = fadd double %".71", 0x3fe0000000000000
  %".73" = fptosi double %".72" to i32
  call void @"vg_draw_pixel"(i32 %".70", i32 %".73")
  %".75" = load double, double* @"x"
  %".76" = fadd double %".75", 0x3fe0000000000000
  %".77" = fptosi double %".76" to i32
  %".78" = load double, double* @"y"
  %".79" = fadd double %".78", 0x3ff0000000000000
  %".80" = fadd double %".79", 0x3fe0000000000000
  %".81" = fptosi double %".80" to i32
  call void @"vg_draw_pixel"(i32 %".77", i32 %".81")
  %".83" = load double, double* @"x"
  %".84" = fsub double %".83", 0x3ff0000000000000
  %".85" = fadd double %".84", 0x3fe0000000000000
  %".86" = fptosi double %".85" to i32
  %".87" = load double, double* @"y"
  %".88" = fsub double %".87", 0x3ff0000000000000
  %".89" = fadd double %".88", 0x3fe0000000000000
  %".90" = fptosi double %".89" to i32
  call void @"vg_draw_pixel"(i32 %".86", i32 %".90")
  %".92" = load double, double* @"x"
  %".93" = fsub double %".92", 0x3ff0000000000000
  %".94" = fadd double %".93", 0x3fe0000000000000
  %".95" = fptosi double %".94" to i32
  %".96" = load double, double* @"y"
  %".97" = fadd double %".96", 0x3fe0000000000000
  %".98" = fptosi double %".97" to i32
  call void @"vg_draw_pixel"(i32 %".95", i32 %".98")
  %".100" = load double, double* @"x"
  %".101" = fadd double %".100", 0x3fe0000000000000
  %".102" = fptosi double %".101" to i32
  %".103" = load double, double* @"y"
  %".104" = fsub double %".103", 0x3ff0000000000000
  %".105" = fadd double %".104", 0x3fe0000000000000
  %".106" = fptosi double %".105" to i32
  call void @"vg_draw_pixel"(i32 %".102", i32 %".106")
  %".108" = fadd double 0x4059000000000000, 0x3fe0000000000000
  %".109" = fptosi double %".108" to i32
  call void @"vg_wait"(i32 %".109")
  br label %"for.incr"
else:
  %".35" = load double, double* @"t"
  %".36" = fadd double %".35", 0x3fe0000000000000
  %".37" = fptosi double %".36" to i32
  %".38" = fadd double 0x4008000000000000, 0x3fe0000000000000
  %".39" = fptosi double %".38" to i32
  %".40" = srem i32 %".37", %".39"
  %".41" = sitofp i32 %".40" to double
  %".42" = fcmp oeq double %".41", 0x3ff0000000000000
  br i1 %".42", label %"then.1", label %"else.1"
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
