; ModuleID = "vgraph"
target triple = "x86_64-pc-windows-msvc"
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
@"len100" = global double              0x0
@"ang" = global double              0x0
@"depth" = global double              0x0
@"axis" = global double              0x0
@"pos" = global double              0x0
@"col" = global i32 16777215
define i32 @"main"()
{
entry:
  call void @"vg_set_color"(i32 0)
  %".3" = fadd double              0x0, 0x3fe0000000000000
  %".4" = fptosi double %".3" to i32
  %".5" = fadd double              0x0, 0x3fe0000000000000
  %".6" = fptosi double %".5" to i32
  %".7" = fadd double 0x4088f80000000000, 0x3fe0000000000000
  %".8" = fptosi double %".7" to i32
  %".9" = fadd double 0x4082b80000000000, 0x3fe0000000000000
  %".10" = fptosi double %".9" to i32
  call void @"vg_draw_rect"(i32 %".4", i32 %".6", i32 %".8", i32 %".10")
  store double 0x4014000000000000, double* @"depth"
  store double 0x4099000000000000, double* @"len100"
  store double              0x0, double* @"pos"
  br label %"for.cond"
for.cond:
  %".16" = load double, double* @"pos"
  %".17" = fcmp olt double %".16", 0x4018000000000000
  br i1 %".17", label %"for.body", label %"for.end"
for.body:
  %".19" = load double, double* @"pos"
  %".20" = fcmp oeq double %".19",              0x0
  br i1 %".20", label %"then", label %"else"
for.incr:
  %".76" = load double, double* @"pos"
  %".77" = fadd double %".76", 0x3ff0000000000000
  store double %".77", double* @"pos"
  br label %"for.cond"
for.end:
  ret i32 0
then:
  store double 0x4062c00000000000, double* @"x1"
  store double 0x4062c00000000000, double* @"y1"
  br label %"endif"
endif:
  store double              0x0, double* @"axis"
  br label %"for.cond.1"
else:
  %".25" = load double, double* @"pos"
  %".26" = fcmp oeq double %".25", 0x3ff0000000000000
  br i1 %".26", label %"then.1", label %"else.1"
then.1:
  store double 0x4084500000000000, double* @"x1"
  store double 0x4062c00000000000, double* @"y1"
  br label %"endif.1"
endif.1:
  br label %"endif"
else.1:
  %".31" = load double, double* @"pos"
  %".32" = fcmp oeq double %".31", 0x4000000000000000
  br i1 %".32", label %"then.2", label %"else.2"
then.2:
  store double 0x4079000000000000, double* @"x1"
  store double 0x4059000000000000, double* @"y1"
  br label %"endif.2"
endif.2:
  br label %"endif.1"
else.2:
  %".37" = load double, double* @"pos"
  %".38" = fcmp oeq double %".37", 0x4008000000000000
  br i1 %".38", label %"then.3", label %"else.3"
then.3:
  store double 0x4062c00000000000, double* @"x1"
  store double 0x407c200000000000, double* @"y1"
  br label %"endif.3"
endif.3:
  br label %"endif.2"
else.3:
  %".43" = load double, double* @"pos"
  %".44" = fcmp oeq double %".43", 0x4010000000000000
  br i1 %".44", label %"then.4", label %"else.4"
then.4:
  store double 0x4084500000000000, double* @"x1"
  store double 0x407c200000000000, double* @"y1"
  br label %"endif.4"
endif.4:
  br label %"endif.3"
else.4:
  store double 0x4079000000000000, double* @"x1"
  store double 0x407f400000000000, double* @"y1"
  br label %"endif.4"
for.cond.1:
  %".58" = load double, double* @"axis"
  %".59" = fcmp olt double %".58", 0x4018000000000000
  br i1 %".59", label %"for.body.1", label %"for.end.1"
for.body.1:
  %".61" = load double, double* @"axis"
  %".62" = fmul double %".61", 0x404e000000000000
  store double %".62", double* @"ang"
  %".64" = load double, double* @"x1"
  %".65" = load double, double* @"y1"
  %".66" = load double, double* @"len100"
  %".67" = load double, double* @"ang"
  %".68" = load double, double* @"depth"
  call void @"triBranch"(double %".64", double %".65", double %".66", double %".67", double %".68")
  br label %"for.incr.1"
for.incr.1:
  %".71" = load double, double* @"axis"
  %".72" = fadd double %".71", 0x3ff0000000000000
  store double %".72", double* @"axis"
  br label %"for.cond.1"
for.end.1:
  br label %"for.incr"
}

define void @"triBranch"(double %".1", double %".2", double %".3", double %".4", double %".5")
{
entry:
  %"x1" = alloca double
  store double %".1", double* %"x1"
  %"y1" = alloca double
  store double %".2", double* %"y1"
  %"len100" = alloca double
  store double %".3", double* %"len100"
  %"ang" = alloca double
  store double %".4", double* %"ang"
  %"depth" = alloca double
  store double %".5", double* %"depth"
  %".12" = load double, double* %"depth"
  %".13" = fcmp oeq double %".12",              0x0
  br i1 %".13", label %"then", label %"endif"
then:
  call void @"vg_set_color"(i32 65280)
  %".16" = load double, double* %"x1"
  %".17" = fadd double %".16", 0x3fe0000000000000
  %".18" = fptosi double %".17" to i32
  %".19" = load double, double* %"y1"
  %".20" = fadd double %".19", 0x3fe0000000000000
  %".21" = fptosi double %".20" to i32
  %".22" = fadd double 0x4000000000000000, 0x3fe0000000000000
  %".23" = fptosi double %".22" to i32
  call void @"vg_draw_circle"(i32 %".18", i32 %".21", i32 %".23")
  ret void
endif:
  %".26" = load double, double* %"x1"
  %".27" = load double, double* %"len100"
  %".28" = load double, double* %"ang"
  %".29" = fmul double %".28", 0x400921ff2e48e8a7
  %".30" = fdiv double %".29", 0x4066800000000000
  %".31" = call double @"cos"(double %".30")
  %".32" = fmul double %".27", %".31"
  %".33" = fdiv double %".32", 0x4059000000000000
  %".34" = fadd double %".26", %".33"
  store double %".34", double* @"x2"
  %".36" = load double, double* %"y1"
  %".37" = load double, double* %"len100"
  %".38" = load double, double* %"ang"
  %".39" = fmul double %".38", 0x400921ff2e48e8a7
  %".40" = fdiv double %".39", 0x4066800000000000
  %".41" = call double @"sin"(double %".40")
  %".42" = fmul double %".37", %".41"
  %".43" = fdiv double %".42", 0x4059000000000000
  %".44" = fsub double %".36", %".43"
  store double %".44", double* @"y2"
  %".46" = load double, double* %"depth"
  %".47" = fadd double %".46", 0x3fe0000000000000
  %".48" = fptosi double %".47" to i32
  %".49" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".50" = fptosi double %".49" to i32
  %".51" = srem i32 %".48", %".50"
  %".52" = sitofp i32 %".51" to double
  %".53" = fcmp oeq double %".52",              0x0
  br i1 %".53", label %"then.1", label %"else"
then.1:
  store i32 16711680, i32* @"col"
  br label %"endif.1"
endif.1:
  %".107" = load i32, i32* @"col"
  call void @"vg_set_color"(i32 %".107")
  %".109" = load double, double* %"x1"
  %".110" = fadd double %".109", 0x3fe0000000000000
  %".111" = fptosi double %".110" to i32
  %".112" = load double, double* %"y1"
  %".113" = fadd double %".112", 0x3fe0000000000000
  %".114" = fptosi double %".113" to i32
  %".115" = load double, double* @"x2"
  %".116" = fadd double %".115", 0x3fe0000000000000
  %".117" = fptosi double %".116" to i32
  %".118" = load double, double* @"y2"
  %".119" = fadd double %".118", 0x3fe0000000000000
  %".120" = fptosi double %".119" to i32
  call void @"vg_draw_line"(i32 %".111", i32 %".114", i32 %".117", i32 %".120")
  %".122" = load double, double* %"x1"
  %".123" = fadd double %".122", 0x3ff0000000000000
  %".124" = fadd double %".123", 0x3fe0000000000000
  %".125" = fptosi double %".124" to i32
  %".126" = load double, double* %"y1"
  %".127" = fadd double %".126", 0x3fe0000000000000
  %".128" = fptosi double %".127" to i32
  %".129" = load double, double* @"x2"
  %".130" = fadd double %".129", 0x3ff0000000000000
  %".131" = fadd double %".130", 0x3fe0000000000000
  %".132" = fptosi double %".131" to i32
  %".133" = load double, double* @"y2"
  %".134" = fadd double %".133", 0x3fe0000000000000
  %".135" = fptosi double %".134" to i32
  call void @"vg_draw_line"(i32 %".125", i32 %".128", i32 %".132", i32 %".135")
  %".137" = load double, double* %"len100"
  %".138" = fmul double %".137", 0x4049000000000000
  %".139" = fdiv double %".138", 0x4059000000000000
  store double %".139", double* %"len100"
  %".141" = load double, double* @"x2"
  %".142" = load double, double* @"y2"
  %".143" = load double, double* %"len100"
  %".144" = load double, double* %"ang"
  %".145" = load double, double* %"depth"
  %".146" = fsub double %".145", 0x3ff0000000000000
  call void @"triBranch"(double %".141", double %".142", double %".143", double %".144", double %".146")
  %".148" = load double, double* @"x2"
  %".149" = load double, double* @"y2"
  %".150" = load double, double* %"len100"
  %".151" = load double, double* %"ang"
  %".152" = fsub double %".151", 0x404e000000000000
  %".153" = load double, double* %"depth"
  %".154" = fsub double %".153", 0x3ff0000000000000
  call void @"triBranch"(double %".148", double %".149", double %".150", double %".152", double %".154")
  %".156" = load double, double* @"x2"
  %".157" = load double, double* @"y2"
  %".158" = load double, double* %"len100"
  %".159" = load double, double* %"ang"
  %".160" = fadd double %".159", 0x404e000000000000
  %".161" = load double, double* %"depth"
  %".162" = fsub double %".161", 0x3ff0000000000000
  call void @"triBranch"(double %".156", double %".157", double %".158", double %".160", double %".162")
  ret void
else:
  %".57" = load double, double* %"depth"
  %".58" = fadd double %".57", 0x3fe0000000000000
  %".59" = fptosi double %".58" to i32
  %".60" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".61" = fptosi double %".60" to i32
  %".62" = srem i32 %".59", %".61"
  %".63" = sitofp i32 %".62" to double
  %".64" = fcmp oeq double %".63", 0x3ff0000000000000
  br i1 %".64", label %"then.2", label %"else.1"
then.2:
  store i32 16776960, i32* @"col"
  br label %"endif.2"
endif.2:
  br label %"endif.1"
else.1:
  %".68" = load double, double* %"depth"
  %".69" = fadd double %".68", 0x3fe0000000000000
  %".70" = fptosi double %".69" to i32
  %".71" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".72" = fptosi double %".71" to i32
  %".73" = srem i32 %".70", %".72"
  %".74" = sitofp i32 %".73" to double
  %".75" = fcmp oeq double %".74", 0x4000000000000000
  br i1 %".75", label %"then.3", label %"else.2"
then.3:
  store i32 65280, i32* @"col"
  br label %"endif.3"
endif.3:
  br label %"endif.2"
else.2:
  %".79" = load double, double* %"depth"
  %".80" = fadd double %".79", 0x3fe0000000000000
  %".81" = fptosi double %".80" to i32
  %".82" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".83" = fptosi double %".82" to i32
  %".84" = srem i32 %".81", %".83"
  %".85" = sitofp i32 %".84" to double
  %".86" = fcmp oeq double %".85", 0x4008000000000000
  br i1 %".86", label %"then.4", label %"else.3"
then.4:
  store i32 65535, i32* @"col"
  br label %"endif.4"
endif.4:
  br label %"endif.3"
else.3:
  %".90" = load double, double* %"depth"
  %".91" = fadd double %".90", 0x3fe0000000000000
  %".92" = fptosi double %".91" to i32
  %".93" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".94" = fptosi double %".93" to i32
  %".95" = srem i32 %".92", %".94"
  %".96" = sitofp i32 %".95" to double
  %".97" = fcmp oeq double %".96", 0x4010000000000000
  br i1 %".97", label %"then.5", label %"else.4"
then.5:
  store i32 255, i32* @"col"
  br label %"endif.5"
endif.5:
  br label %"endif.4"
else.4:
  store i32 16711935, i32* @"col"
  br label %"endif.5"
}

define i32 @"_main"()
{
entry:
  %".2" = call i32 @"main"()
  ret i32 %".2"
}
