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
@"arm" = global double              0x0
@"ang" = global double              0x0
@"rad" = global double              0x0
@"x" = global double              0x0
@"y" = global double              0x0
@"star" = global double              0x0
@"sx" = global double              0x0
@"sy" = global double              0x0
@"sparkleT" = global double              0x0
@"col" = global i32 16777215
define i32 @"main"()
{
entry:
  store double 0x4079000000000000, double* @"cx"
  store double 0x4072c00000000000, double* @"cy"
  call void @"vg_clear"()
  call void @"vg_set_color"(i32 0)
  %".6" = fadd double              0x0, 0x3fe0000000000000
  %".7" = fptosi double %".6" to i32
  %".8" = fadd double              0x0, 0x3fe0000000000000
  %".9" = fptosi double %".8" to i32
  %".10" = fadd double 0x4088f80000000000, 0x3fe0000000000000
  %".11" = fptosi double %".10" to i32
  %".12" = fadd double 0x4082b80000000000, 0x3fe0000000000000
  %".13" = fptosi double %".12" to i32
  call void @"vg_draw_rect"(i32 %".7", i32 %".9", i32 %".11", i32 %".13")
  store double              0x0, double* @"t"
  br label %"for.cond"
for.cond:
  %".17" = load double, double* @"t"
  %".18" = fcmp olt double %".17", 0x40e1940000000000
  br i1 %".18", label %"for.body", label %"for.end"
for.body:
  %".20" = load double, double* @"t"
  %".21" = fdiv double %".20", 0x4034000000000000
  %".22" = fadd double %".21", 0x3fe0000000000000
  %".23" = fptosi double %".22" to i32
  %".24" = fadd double 0x4000000000000000, 0x3fe0000000000000
  %".25" = fptosi double %".24" to i32
  %".26" = srem i32 %".23", %".25"
  %".27" = sitofp i32 %".26" to double
  %".28" = fcmp oeq double %".27",              0x0
  br i1 %".28", label %"then", label %"else"
for.incr:
  %".315" = load double, double* @"t"
  %".316" = fadd double %".315", 0x4000000000000000
  store double %".316", double* @"t"
  br label %"for.cond"
for.end:
  ret i32 0
then:
  store i32 16777215, i32* @"col"
  br label %"endif"
endif:
  %".34" = load i32, i32* @"col"
  call void @"vg_set_color"(i32 %".34")
  %".36" = load double, double* @"cx"
  %".37" = fadd double %".36", 0x3fe0000000000000
  %".38" = fptosi double %".37" to i32
  %".39" = load double, double* @"cy"
  %".40" = fadd double %".39", 0x3fe0000000000000
  %".41" = fptosi double %".40" to i32
  %".42" = load double, double* @"t"
  %".43" = fadd double %".42", 0x3fe0000000000000
  %".44" = fptosi double %".43" to i32
  %".45" = fadd double 0x4034000000000000, 0x3fe0000000000000
  %".46" = fptosi double %".45" to i32
  %".47" = srem i32 %".44", %".46"
  %".48" = sitofp i32 %".47" to double
  %".49" = fdiv double %".48", 0x4000000000000000
  %".50" = fadd double 0x4028000000000000, %".49"
  %".51" = fadd double %".50", 0x3fe0000000000000
  %".52" = fptosi double %".51" to i32
  call void @"vg_draw_circle"(i32 %".38", i32 %".41", i32 %".52")
  store double              0x0, double* @"arm"
  br label %"for.cond.1"
else:
  store i32 65535, i32* @"col"
  br label %"endif"
for.cond.1:
  %".56" = load double, double* @"arm"
  %".57" = fcmp olt double %".56", 0x4018000000000000
  br i1 %".57", label %"for.body.1", label %"for.end.1"
for.body.1:
  store double              0x0, double* @"rad"
  store double 0x4018000000000000, double* @"rad"
  br label %"for.cond.2"
for.incr.1:
  %".216" = load double, double* @"arm"
  %".217" = fadd double %".216", 0x3ff0000000000000
  store double %".217", double* @"arm"
  br label %"for.cond.1"
for.end.1:
  store double              0x0, double* @"star"
  br label %"for.cond.3"
for.cond.2:
  %".62" = load double, double* @"rad"
  %".63" = fcmp olt double %".62", 0x4070400000000000
  br i1 %".63", label %"for.body.2", label %"for.end.2"
for.body.2:
  %".65" = load double, double* @"t"
  %".66" = load double, double* @"arm"
  %".67" = fmul double %".66", 0x404e000000000000
  %".68" = fadd double %".65", %".67"
  %".69" = load double, double* @"rad"
  %".70" = fadd double %".68", %".69"
  store double %".70", double* @"ang"
  %".72" = load double, double* @"cx"
  %".73" = load double, double* @"rad"
  %".74" = load double, double* @"ang"
  %".75" = fmul double %".74", 0x400921ff2e48e8a7
  %".76" = fdiv double %".75", 0x4066800000000000
  %".77" = call double @"cos"(double %".76")
  %".78" = fmul double %".73", %".77"
  %".79" = fadd double %".72", %".78"
  store double %".79", double* @"x"
  %".81" = load double, double* @"cy"
  %".82" = load double, double* @"rad"
  %".83" = load double, double* @"ang"
  %".84" = fmul double %".83", 0x400921ff2e48e8a7
  %".85" = fdiv double %".84", 0x4066800000000000
  %".86" = call double @"sin"(double %".85")
  %".87" = fmul double %".82", %".86"
  %".88" = fadd double %".81", %".87"
  store double %".88", double* @"y"
  %".90" = load double, double* @"rad"
  %".91" = fdiv double %".90", 0x4038000000000000
  %".92" = load double, double* @"arm"
  %".93" = fadd double %".91", %".92"
  %".94" = fadd double %".93", 0x3fe0000000000000
  %".95" = fptosi double %".94" to i32
  %".96" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".97" = fptosi double %".96" to i32
  %".98" = srem i32 %".95", %".97"
  %".99" = sitofp i32 %".98" to double
  %".100" = fcmp oeq double %".99",              0x0
  br i1 %".100", label %"then.1", label %"else.1"
for.incr.2:
  %".211" = load double, double* @"rad"
  %".212" = fadd double %".211", 0x4018000000000000
  store double %".212", double* @"rad"
  br label %"for.cond.2"
for.end.2:
  br label %"for.incr.1"
then.1:
  store i32 16711680, i32* @"col"
  br label %"endif.1"
endif.1:
  %".166" = load i32, i32* @"col"
  call void @"vg_set_color"(i32 %".166")
  %".168" = load double, double* @"x"
  %".169" = fadd double %".168", 0x3fe0000000000000
  %".170" = fptosi double %".169" to i32
  %".171" = load double, double* @"y"
  %".172" = fadd double %".171", 0x3fe0000000000000
  %".173" = fptosi double %".172" to i32
  %".174" = fadd double 0x4010000000000000, 0x3fe0000000000000
  %".175" = fptosi double %".174" to i32
  call void @"vg_draw_circle"(i32 %".170", i32 %".173", i32 %".175")
  call void @"vg_set_color"(i32 16777215)
  %".178" = load double, double* @"x"
  %".179" = fadd double %".178", 0x4000000000000000
  %".180" = fadd double %".179", 0x3fe0000000000000
  %".181" = fptosi double %".180" to i32
  %".182" = load double, double* @"y"
  %".183" = fadd double %".182", 0x3fe0000000000000
  %".184" = fptosi double %".183" to i32
  call void @"vg_draw_pixel"(i32 %".181", i32 %".184")
  %".186" = load double, double* @"x"
  %".187" = fsub double %".186", 0x4000000000000000
  %".188" = fadd double %".187", 0x3fe0000000000000
  %".189" = fptosi double %".188" to i32
  %".190" = load double, double* @"y"
  %".191" = fadd double %".190", 0x3fe0000000000000
  %".192" = fptosi double %".191" to i32
  call void @"vg_draw_pixel"(i32 %".189", i32 %".192")
  %".194" = load double, double* @"x"
  %".195" = fadd double %".194", 0x3fe0000000000000
  %".196" = fptosi double %".195" to i32
  %".197" = load double, double* @"y"
  %".198" = fadd double %".197", 0x4000000000000000
  %".199" = fadd double %".198", 0x3fe0000000000000
  %".200" = fptosi double %".199" to i32
  call void @"vg_draw_pixel"(i32 %".196", i32 %".200")
  %".202" = load double, double* @"x"
  %".203" = fadd double %".202", 0x3fe0000000000000
  %".204" = fptosi double %".203" to i32
  %".205" = load double, double* @"y"
  %".206" = fsub double %".205", 0x4000000000000000
  %".207" = fadd double %".206", 0x3fe0000000000000
  %".208" = fptosi double %".207" to i32
  call void @"vg_draw_pixel"(i32 %".204", i32 %".208")
  br label %"for.incr.2"
else.1:
  %".104" = load double, double* @"rad"
  %".105" = fdiv double %".104", 0x4038000000000000
  %".106" = load double, double* @"arm"
  %".107" = fadd double %".105", %".106"
  %".108" = fadd double %".107", 0x3fe0000000000000
  %".109" = fptosi double %".108" to i32
  %".110" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".111" = fptosi double %".110" to i32
  %".112" = srem i32 %".109", %".111"
  %".113" = sitofp i32 %".112" to double
  %".114" = fcmp oeq double %".113", 0x3ff0000000000000
  br i1 %".114", label %"then.2", label %"else.2"
then.2:
  store i32 16776960, i32* @"col"
  br label %"endif.2"
endif.2:
  br label %"endif.1"
else.2:
  %".118" = load double, double* @"rad"
  %".119" = fdiv double %".118", 0x4038000000000000
  %".120" = load double, double* @"arm"
  %".121" = fadd double %".119", %".120"
  %".122" = fadd double %".121", 0x3fe0000000000000
  %".123" = fptosi double %".122" to i32
  %".124" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".125" = fptosi double %".124" to i32
  %".126" = srem i32 %".123", %".125"
  %".127" = sitofp i32 %".126" to double
  %".128" = fcmp oeq double %".127", 0x4000000000000000
  br i1 %".128", label %"then.3", label %"else.3"
then.3:
  store i32 65280, i32* @"col"
  br label %"endif.3"
endif.3:
  br label %"endif.2"
else.3:
  %".132" = load double, double* @"rad"
  %".133" = fdiv double %".132", 0x4038000000000000
  %".134" = load double, double* @"arm"
  %".135" = fadd double %".133", %".134"
  %".136" = fadd double %".135", 0x3fe0000000000000
  %".137" = fptosi double %".136" to i32
  %".138" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".139" = fptosi double %".138" to i32
  %".140" = srem i32 %".137", %".139"
  %".141" = sitofp i32 %".140" to double
  %".142" = fcmp oeq double %".141", 0x4008000000000000
  br i1 %".142", label %"then.4", label %"else.4"
then.4:
  store i32 65535, i32* @"col"
  br label %"endif.4"
endif.4:
  br label %"endif.3"
else.4:
  %".146" = load double, double* @"rad"
  %".147" = fdiv double %".146", 0x4038000000000000
  %".148" = load double, double* @"arm"
  %".149" = fadd double %".147", %".148"
  %".150" = fadd double %".149", 0x3fe0000000000000
  %".151" = fptosi double %".150" to i32
  %".152" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".153" = fptosi double %".152" to i32
  %".154" = srem i32 %".151", %".153"
  %".155" = sitofp i32 %".154" to double
  %".156" = fcmp oeq double %".155", 0x4010000000000000
  br i1 %".156", label %"then.5", label %"else.5"
then.5:
  store i32 255, i32* @"col"
  br label %"endif.5"
endif.5:
  br label %"endif.4"
else.5:
  store i32 16711935, i32* @"col"
  br label %"endif.5"
for.cond.3:
  %".222" = load double, double* @"star"
  %".223" = fcmp olt double %".222", 0x4049000000000000
  br i1 %".223", label %"for.body.3", label %"for.end.3"
for.body.3:
  %".225" = load double, double* @"t"
  %".226" = fmul double %".225", 0x402a000000000000
  %".227" = load double, double* @"star"
  %".228" = fmul double %".227", 0x4058400000000000
  %".229" = fadd double %".226", %".228"
  %".230" = fadd double %".229", 0x3fe0000000000000
  %".231" = fptosi double %".230" to i32
  %".232" = fadd double 0x4089000000000000, 0x3fe0000000000000
  %".233" = fptosi double %".232" to i32
  %".234" = srem i32 %".231", %".233"
  %".235" = sitofp i32 %".234" to double
  store double %".235", double* @"sx"
  %".237" = load double, double* @"t"
  %".238" = fmul double %".237", 0x403d000000000000
  %".239" = load double, double* @"star"
  %".240" = fmul double %".239", 0x404a800000000000
  %".241" = fadd double %".238", %".240"
  %".242" = fadd double %".241", 0x3fe0000000000000
  %".243" = fptosi double %".242" to i32
  %".244" = fadd double 0x4082c00000000000, 0x3fe0000000000000
  %".245" = fptosi double %".244" to i32
  %".246" = srem i32 %".243", %".245"
  %".247" = sitofp i32 %".246" to double
  store double %".247", double* @"sy"
  %".249" = load double, double* @"t"
  %".250" = load double, double* @"star"
  %".251" = fmul double %".250", 0x401c000000000000
  %".252" = fadd double %".249", %".251"
  %".253" = fdiv double %".252", 0x4024000000000000
  %".254" = fadd double %".253", 0x3fe0000000000000
  %".255" = fptosi double %".254" to i32
  %".256" = fadd double 0x4000000000000000, 0x3fe0000000000000
  %".257" = fptosi double %".256" to i32
  %".258" = srem i32 %".255", %".257"
  %".259" = sitofp i32 %".258" to double
  %".260" = fcmp oeq double %".259",              0x0
  br i1 %".260", label %"then.6", label %"else.6"
for.incr.3:
  %".276" = load double, double* @"star"
  %".277" = fadd double %".276", 0x3ff0000000000000
  store double %".277", double* @"star"
  br label %"for.cond.3"
for.end.3:
  %".280" = load double, double* @"t"
  %".281" = fadd double %".280", 0x3fe0000000000000
  %".282" = fptosi double %".281" to i32
  %".283" = fadd double 0x4066800000000000, 0x3fe0000000000000
  %".284" = fptosi double %".283" to i32
  %".285" = srem i32 %".282", %".284"
  %".286" = sitofp i32 %".285" to double
  %".287" = fcmp oeq double %".286",              0x0
  br i1 %".287", label %"then.7", label %"endif.7"
then.6:
  store i32 16777215, i32* @"col"
  br label %"endif.6"
endif.6:
  %".266" = load i32, i32* @"col"
  call void @"vg_set_color"(i32 %".266")
  %".268" = load double, double* @"sx"
  %".269" = fadd double %".268", 0x3fe0000000000000
  %".270" = fptosi double %".269" to i32
  %".271" = load double, double* @"sy"
  %".272" = fadd double %".271", 0x3fe0000000000000
  %".273" = fptosi double %".272" to i32
  call void @"vg_draw_pixel"(i32 %".270", i32 %".273")
  br label %"for.incr.3"
else.6:
  store i32 65535, i32* @"col"
  br label %"endif.6"
then.7:
  %".289" = load double, double* @"cx"
  %".290" = load double, double* @"t"
  %".291" = fadd double %".290", 0x405ec00000000000
  %".292" = fmul double %".291", 0x400921ff2e48e8a7
  %".293" = fdiv double %".292", 0x4066800000000000
  %".294" = call double @"cos"(double %".293")
  %".295" = fmul double 0x4070400000000000, %".294"
  %".296" = fadd double %".289", %".295"
  store double %".296", double* @"sx"
  %".298" = load double, double* @"cy"
  %".299" = load double, double* @"t"
  %".300" = fadd double %".299", 0x405ec00000000000
  %".301" = fmul double %".300", 0x400921ff2e48e8a7
  %".302" = fdiv double %".301", 0x4066800000000000
  %".303" = call double @"sin"(double %".302")
  %".304" = fmul double 0x4070400000000000, %".303"
  %".305" = fadd double %".298", %".304"
  store double %".305", double* @"sy"
  %".307" = load double, double* @"sx"
  %".308" = load double, double* @"sy"
  call void @"sparkle"(double %".307", double %".308")
  br label %"endif.7"
endif.7:
  %".311" = fadd double 0x4000000000000000, 0x3fe0000000000000
  %".312" = fptosi double %".311" to i32
  call void @"vg_wait"(i32 %".312")
  br label %"for.incr"
}

define void @"sparkle"(double %".1", double %".2")
{
entry:
  %"px" = alloca double
  store double %".1", double* %"px"
  %"py" = alloca double
  store double %".2", double* %"py"
  store double              0x0, double* @"sparkleT"
  br label %"for.cond"
for.cond:
  %".8" = load double, double* @"sparkleT"
  %".9" = fcmp olt double %".8", 0x4018000000000000
  br i1 %".9", label %"for.body", label %"for.end"
for.body:
  %".11" = load double, double* @"sparkleT"
  %".12" = fadd double %".11", 0x3fe0000000000000
  %".13" = fptosi double %".12" to i32
  %".14" = fadd double 0x4000000000000000, 0x3fe0000000000000
  %".15" = fptosi double %".14" to i32
  %".16" = srem i32 %".13", %".15"
  %".17" = sitofp i32 %".16" to double
  %".18" = fcmp oeq double %".17",              0x0
  br i1 %".18", label %"then", label %"else"
for.incr:
  %".39" = load double, double* @"sparkleT"
  %".40" = fadd double %".39", 0x3ff0000000000000
  store double %".40", double* @"sparkleT"
  br label %"for.cond"
for.end:
  ret void
then:
  store i32 16711935, i32* @"col"
  br label %"endif"
endif:
  %".24" = load i32, i32* @"col"
  call void @"vg_set_color"(i32 %".24")
  %".26" = load double, double* %"px"
  %".27" = fadd double %".26", 0x3fe0000000000000
  %".28" = fptosi double %".27" to i32
  %".29" = load double, double* %"py"
  %".30" = fadd double %".29", 0x3fe0000000000000
  %".31" = fptosi double %".30" to i32
  %".32" = load double, double* @"sparkleT"
  %".33" = fdiv double %".32", 0x4000000000000000
  %".34" = fsub double 0x4010000000000000, %".33"
  %".35" = fadd double %".34", 0x3fe0000000000000
  %".36" = fptosi double %".35" to i32
  call void @"vg_draw_circle"(i32 %".28", i32 %".31", i32 %".36")
  br label %"for.incr"
else:
  store i32 16776960, i32* @"col"
  br label %"endif"
}

define i32 @"_main"()
{
entry:
  %".2" = call i32 @"main"()
  ret i32 %".2"
}
