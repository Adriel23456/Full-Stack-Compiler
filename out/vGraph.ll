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

@"cx" = global double              0x0
@"cy" = global double              0x0
@"t" = global double              0x0
@"seg" = global double              0x0
@"ang" = global double              0x0
@"x" = global double              0x0
@"y" = global double              0x0
@"ray" = global double              0x0
@"x2" = global double              0x0
@"y2" = global double              0x0
@"blades" = global double              0x0
@"col" = global i32 16777215
define i32 @"main"()
{
entry:
  store double 0x4079000000000000, double* @"cx"
  store double 0x4072c00000000000, double* @"cy"
  store double 0x4028000000000000, double* @"blades"
  store double              0x0, double* @"t"
  br label %"for.cond"
for.cond:
  %".7" = load double, double* @"t"
  %".8" = fcmp olt double %".7", 0x4115f90000000000
  br i1 %".8", label %"for.body", label %"for.end"
for.body:
  call void @"vg_set_color"(i32 0)
  %".11" = fadd double              0x0, 0x3fe0000000000000
  %".12" = fptosi double %".11" to i32
  %".13" = fadd double              0x0, 0x3fe0000000000000
  %".14" = fptosi double %".13" to i32
  %".15" = fadd double 0x4088f80000000000, 0x3fe0000000000000
  %".16" = fptosi double %".15" to i32
  %".17" = fadd double 0x4082b80000000000, 0x3fe0000000000000
  %".18" = fptosi double %".17" to i32
  call void @"vg_draw_rect"(i32 %".12", i32 %".14", i32 %".16", i32 %".18")
  %".20" = load double, double* @"t"
  %".21" = load double, double* @"blades"
  call void @"aperture"(double %".20", double %".21", double 0x4024000000000000, double 0x4066800000000000)
  %".23" = load double, double* @"t"
  %".24" = fadd double %".23", 0x3fe0000000000000
  %".25" = fptosi double %".24" to i32
  %".26" = fadd double 0x4034000000000000, 0x3fe0000000000000
  %".27" = fptosi double %".26" to i32
  %".28" = srem i32 %".25", %".27"
  %".29" = sitofp i32 %".28" to double
  %".30" = fadd double 0x404e000000000000, %".29"
  %".31" = load double, double* @"t"
  call void @"drawRing"(double %".30", double 0x4038000000000000, double %".31", double 0x3ff0000000000000)
  %".33" = load double, double* @"t"
  %".34" = fadd double %".33", 0x3fe0000000000000
  %".35" = fptosi double %".34" to i32
  %".36" = fadd double 0x4034000000000000, 0x3fe0000000000000
  %".37" = fptosi double %".36" to i32
  %".38" = srem i32 %".35", %".37"
  %".39" = sitofp i32 %".38" to double
  %".40" = fsub double 0x405e000000000000, %".39"
  %".41" = load double, double* @"t"
  %".42" = fmul double %".41", 0x3ff8000000000000
  %".43" = fsub double              0x0, 0x3ff0000000000000
  call void @"drawRing"(double %".40", double 0x403e000000000000, double %".42", double %".43")
  %".45" = load double, double* @"t"
  %".46" = fadd double %".45", 0x3fe0000000000000
  %".47" = fptosi double %".46" to i32
  %".48" = fadd double 0x402e000000000000, 0x3fe0000000000000
  %".49" = fptosi double %".48" to i32
  %".50" = srem i32 %".47", %".49"
  %".51" = sitofp i32 %".50" to double
  %".52" = fadd double 0x4066800000000000, %".51"
  %".53" = load double, double* @"t"
  %".54" = fmul double %".53", 0x4000000000000000
  call void @"drawRing"(double %".52", double 0x4042000000000000, double %".54", double 0x3ff0000000000000)
  %".56" = load double, double* @"t"
  %".57" = fadd double %".56", 0x3fe0000000000000
  %".58" = fptosi double %".57" to i32
  %".59" = fadd double 0x402e000000000000, 0x3fe0000000000000
  %".60" = fptosi double %".59" to i32
  %".61" = srem i32 %".58", %".60"
  %".62" = sitofp i32 %".61" to double
  %".63" = fsub double 0x406e000000000000, %".62"
  %".64" = load double, double* @"t"
  %".65" = fmul double %".64", 0x4004000000000000
  %".66" = fsub double              0x0, 0x3ff0000000000000
  call void @"drawRing"(double %".63", double 0x4045000000000000, double %".65", double %".66")
  %".68" = fadd double 0x4059000000000000, 0x3fe0000000000000
  %".69" = fptosi double %".68" to i32
  call void @"vg_wait"(i32 %".69")
  br label %"for.incr"
for.incr:
  %".72" = load double, double* @"t"
  %".73" = fadd double %".72", 0x4008000000000000
  store double %".73", double* @"t"
  br label %"for.cond"
for.end:
  ret i32 0
}

define void @"drawRing"(double %".1", double %".2", double %".3", double %".4")
{
entry:
  %"radius" = alloca double
  store double %".1", double* %"radius"
  %"segments" = alloca double
  store double %".2", double* %"segments"
  %"phase" = alloca double
  store double %".3", double* %"phase"
  %"dir" = alloca double
  store double %".4", double* %"dir"
  store double              0x0, double* @"seg"
  br label %"for.cond"
for.cond:
  %".12" = load double, double* @"seg"
  %".13" = load double, double* %"segments"
  %".14" = fcmp olt double %".12", %".13"
  br i1 %".14", label %"for.body", label %"for.end"
for.body:
  %".16" = load double, double* %"dir"
  %".17" = load double, double* @"seg"
  %".18" = fmul double %".16", %".17"
  %".19" = fmul double %".18", 0x4076800000000000
  %".20" = load double, double* %"segments"
  %".21" = fdiv double %".19", %".20"
  %".22" = load double, double* %"phase"
  %".23" = fadd double %".21", %".22"
  store double %".23", double* @"ang"
  %".25" = load double, double* @"cx"
  %".26" = load double, double* %"radius"
  %".27" = load double, double* @"ang"
  %".28" = fmul double %".27", 0x400921ff2e48e8a7
  %".29" = fdiv double %".28", 0x4066800000000000
  %".30" = call double @"cos"(double %".29")
  %".31" = fmul double %".26", %".30"
  %".32" = fadd double %".25", %".31"
  store double %".32", double* @"x"
  %".34" = load double, double* @"cy"
  %".35" = load double, double* %"radius"
  %".36" = load double, double* @"ang"
  %".37" = fmul double %".36", 0x400921ff2e48e8a7
  %".38" = fdiv double %".37", 0x4066800000000000
  %".39" = call double @"sin"(double %".38")
  %".40" = fmul double %".35", %".39"
  %".41" = fadd double %".34", %".40"
  store double %".41", double* @"y"
  %".43" = load double, double* @"seg"
  %".44" = fadd double %".43", 0x3fe0000000000000
  %".45" = fptosi double %".44" to i32
  %".46" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".47" = fptosi double %".46" to i32
  %".48" = srem i32 %".45", %".47"
  %".49" = sitofp i32 %".48" to double
  %".50" = fcmp oeq double %".49",              0x0
  br i1 %".50", label %"then", label %"else"
for.incr:
  %".116" = load double, double* @"seg"
  %".117" = fadd double %".116", 0x3ff0000000000000
  store double %".117", double* @"seg"
  br label %"for.cond"
for.end:
  ret void
then:
  store i32 16711680, i32* @"col"
  br label %"endif"
endif:
  %".104" = load i32, i32* @"col"
  call void @"vg_set_color"(i32 %".104")
  %".106" = load double, double* @"x"
  %".107" = fadd double %".106", 0x3fe0000000000000
  %".108" = fptosi double %".107" to i32
  %".109" = load double, double* @"y"
  %".110" = fadd double %".109", 0x3fe0000000000000
  %".111" = fptosi double %".110" to i32
  %".112" = fadd double 0x4014000000000000, 0x3fe0000000000000
  %".113" = fptosi double %".112" to i32
  call void @"vg_draw_circle"(i32 %".108", i32 %".111", i32 %".113")
  br label %"for.incr"
else:
  %".54" = load double, double* @"seg"
  %".55" = fadd double %".54", 0x3fe0000000000000
  %".56" = fptosi double %".55" to i32
  %".57" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".58" = fptosi double %".57" to i32
  %".59" = srem i32 %".56", %".58"
  %".60" = sitofp i32 %".59" to double
  %".61" = fcmp oeq double %".60", 0x3ff0000000000000
  br i1 %".61", label %"then.1", label %"else.1"
then.1:
  store i32 16776960, i32* @"col"
  br label %"endif.1"
endif.1:
  br label %"endif"
else.1:
  %".65" = load double, double* @"seg"
  %".66" = fadd double %".65", 0x3fe0000000000000
  %".67" = fptosi double %".66" to i32
  %".68" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".69" = fptosi double %".68" to i32
  %".70" = srem i32 %".67", %".69"
  %".71" = sitofp i32 %".70" to double
  %".72" = fcmp oeq double %".71", 0x4000000000000000
  br i1 %".72", label %"then.2", label %"else.2"
then.2:
  store i32 65280, i32* @"col"
  br label %"endif.2"
endif.2:
  br label %"endif.1"
else.2:
  %".76" = load double, double* @"seg"
  %".77" = fadd double %".76", 0x3fe0000000000000
  %".78" = fptosi double %".77" to i32
  %".79" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".80" = fptosi double %".79" to i32
  %".81" = srem i32 %".78", %".80"
  %".82" = sitofp i32 %".81" to double
  %".83" = fcmp oeq double %".82", 0x4008000000000000
  br i1 %".83", label %"then.3", label %"else.3"
then.3:
  store i32 65535, i32* @"col"
  br label %"endif.3"
endif.3:
  br label %"endif.2"
else.3:
  %".87" = load double, double* @"seg"
  %".88" = fadd double %".87", 0x3fe0000000000000
  %".89" = fptosi double %".88" to i32
  %".90" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".91" = fptosi double %".90" to i32
  %".92" = srem i32 %".89", %".91"
  %".93" = sitofp i32 %".92" to double
  %".94" = fcmp oeq double %".93", 0x4010000000000000
  br i1 %".94", label %"then.4", label %"else.4"
then.4:
  store i32 255, i32* @"col"
  br label %"endif.4"
endif.4:
  br label %"endif.3"
else.4:
  store i32 16711935, i32* @"col"
  br label %"endif.4"
}

define void @"aperture"(double %".1", double %".2", double %".3", double %".4")
{
entry:
  %"step" = alloca double
  store double %".1", double* %"step"
  %"blades" = alloca double
  store double %".2", double* %"blades"
  %"innerR" = alloca double
  store double %".3", double* %"innerR"
  %"outerR" = alloca double
  store double %".4", double* %"outerR"
  store double              0x0, double* @"ray"
  br label %"for.cond"
for.cond:
  %".12" = load double, double* @"ray"
  %".13" = load double, double* %"blades"
  %".14" = fcmp olt double %".12", %".13"
  br i1 %".14", label %"for.body", label %"for.end"
for.body:
  %".16" = load double, double* @"ray"
  %".17" = fmul double %".16", 0x4076800000000000
  %".18" = load double, double* %"blades"
  %".19" = fdiv double %".17", %".18"
  %".20" = load double, double* %"step"
  %".21" = fmul double %".20", 0x4000000000000000
  %".22" = fadd double %".19", %".21"
  store double %".22", double* @"ang"
  %".24" = load double, double* @"cx"
  %".25" = load double, double* %"innerR"
  %".26" = load double, double* @"ang"
  %".27" = fmul double %".26", 0x400921ff2e48e8a7
  %".28" = fdiv double %".27", 0x4066800000000000
  %".29" = call double @"cos"(double %".28")
  %".30" = fmul double %".25", %".29"
  %".31" = fadd double %".24", %".30"
  store double %".31", double* @"x"
  %".33" = load double, double* @"cy"
  %".34" = load double, double* %"innerR"
  %".35" = load double, double* @"ang"
  %".36" = fmul double %".35", 0x400921ff2e48e8a7
  %".37" = fdiv double %".36", 0x4066800000000000
  %".38" = call double @"sin"(double %".37")
  %".39" = fmul double %".34", %".38"
  %".40" = fadd double %".33", %".39"
  store double %".40", double* @"y"
  %".42" = load double, double* @"cx"
  %".43" = load double, double* %"outerR"
  %".44" = load double, double* @"ang"
  %".45" = fmul double %".44", 0x400921ff2e48e8a7
  %".46" = fdiv double %".45", 0x4066800000000000
  %".47" = call double @"cos"(double %".46")
  %".48" = fmul double %".43", %".47"
  %".49" = fadd double %".42", %".48"
  store double %".49", double* @"x2"
  %".51" = load double, double* @"cy"
  %".52" = load double, double* %"outerR"
  %".53" = load double, double* @"ang"
  %".54" = fmul double %".53", 0x400921ff2e48e8a7
  %".55" = fdiv double %".54", 0x4066800000000000
  %".56" = call double @"sin"(double %".55")
  %".57" = fmul double %".52", %".56"
  %".58" = fadd double %".51", %".57"
  store double %".58", double* @"y2"
  %".60" = load double, double* @"ray"
  %".61" = fadd double %".60", 0x3fe0000000000000
  %".62" = fptosi double %".61" to i32
  %".63" = fadd double 0x4000000000000000, 0x3fe0000000000000
  %".64" = fptosi double %".63" to i32
  %".65" = srem i32 %".62", %".64"
  %".66" = sitofp i32 %".65" to double
  %".67" = fcmp oeq double %".66",              0x0
  br i1 %".67", label %"then", label %"else"
for.incr:
  %".104" = load double, double* @"ray"
  %".105" = fadd double %".104", 0x3ff0000000000000
  store double %".105", double* @"ray"
  br label %"for.cond"
for.end:
  ret void
then:
  store i32 16777215, i32* @"col"
  br label %"endif"
endif:
  %".73" = load i32, i32* @"col"
  call void @"vg_set_color"(i32 %".73")
  %".75" = load double, double* @"x"
  %".76" = fadd double %".75", 0x3fe0000000000000
  %".77" = fptosi double %".76" to i32
  %".78" = load double, double* @"y"
  %".79" = fadd double %".78", 0x3fe0000000000000
  %".80" = fptosi double %".79" to i32
  %".81" = load double, double* @"x2"
  %".82" = fadd double %".81", 0x3fe0000000000000
  %".83" = fptosi double %".82" to i32
  %".84" = load double, double* @"y2"
  %".85" = fadd double %".84", 0x3fe0000000000000
  %".86" = fptosi double %".85" to i32
  call void @"vg_draw_line"(i32 %".77", i32 %".80", i32 %".83", i32 %".86")
  %".88" = load double, double* @"x"
  %".89" = fadd double %".88", 0x3ff0000000000000
  %".90" = fadd double %".89", 0x3fe0000000000000
  %".91" = fptosi double %".90" to i32
  %".92" = load double, double* @"y"
  %".93" = fadd double %".92", 0x3fe0000000000000
  %".94" = fptosi double %".93" to i32
  %".95" = load double, double* @"x2"
  %".96" = fadd double %".95", 0x3ff0000000000000
  %".97" = fadd double %".96", 0x3fe0000000000000
  %".98" = fptosi double %".97" to i32
  %".99" = load double, double* @"y2"
  %".100" = fadd double %".99", 0x3fe0000000000000
  %".101" = fptosi double %".100" to i32
  call void @"vg_draw_line"(i32 %".91", i32 %".94", i32 %".98", i32 %".101")
  br label %"for.incr"
else:
  store i32 65535, i32* @"col"
  br label %"endif"
}

define i32 @"_main"()
{
entry:
  %".2" = call i32 @"main"()
  ret i32 %".2"
}
