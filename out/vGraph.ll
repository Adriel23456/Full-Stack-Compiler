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
@"angle" = global double              0x0
@"depth" = global double              0x0
@"c" = global i32 16777215
define i32 @"main"()
{
entry:
  call void @"vg_clear"()
  store double 0x3ff0000000000000, double* @"depth"
  br label %"for.cond"
for.cond:
  %".5" = load double, double* @"depth"
  %".6" = fcmp ole double %".5", 0x4024000000000000
  br i1 %".6", label %"for.body", label %"for.end"
for.body:
  call void @"vg_clear"()
  %".9" = load double, double* @"depth"
  call void @"tree"(double 0x4074000000000000, double 0x4079000000000000, double 0x4059000000000000, double 0x4056800000000000, double %".9")
  %".11" = fadd double 0x407f400000000000, 0x3fe0000000000000
  %".12" = fptosi double %".11" to i32
  call void @"vg_wait"(i32 %".12")
  br label %"for.incr"
for.incr:
  %".15" = load double, double* @"depth"
  %".16" = fadd double %".15", 0x3ff0000000000000
  store double %".16", double* @"depth"
  br label %"for.cond"
for.end:
  ret i32 0
}

define void @"tree"(double %".1", double %".2", double %".3", double %".4", double %".5")
{
entry:
  %"x1" = alloca double
  store double %".1", double* %"x1"
  %"y1" = alloca double
  store double %".2", double* %"y1"
  %"length" = alloca double
  store double %".3", double* %"length"
  %"angle" = alloca double
  store double %".4", double* %"angle"
  %"depth" = alloca double
  store double %".5", double* %"depth"
  %".12" = load double, double* %"depth"
  %".13" = fcmp oeq double %".12",              0x0
  br i1 %".13", label %"then", label %"endif"
then:
  ret void
endif:
  %".16" = load double, double* %"x1"
  %".17" = load double, double* %"length"
  %".18" = load double, double* %"angle"
  %".19" = fmul double %".18", 0x400921ff2e48e8a7
  %".20" = fdiv double %".19", 0x4066800000000000
  %".21" = call double @"cos"(double %".20")
  %".22" = fmul double %".17", %".21"
  %".23" = fadd double %".16", %".22"
  store double %".23", double* @"x2"
  %".25" = load double, double* %"y1"
  %".26" = load double, double* %"length"
  %".27" = load double, double* %"angle"
  %".28" = fmul double %".27", 0x400921ff2e48e8a7
  %".29" = fdiv double %".28", 0x4066800000000000
  %".30" = call double @"sin"(double %".29")
  %".31" = fmul double %".26", %".30"
  %".32" = fsub double %".25", %".31"
  store double %".32", double* @"y2"
  %".34" = load double, double* %"depth"
  %".35" = fadd double %".34", 0x3fe0000000000000
  %".36" = fptosi double %".35" to i32
  %".37" = fadd double 0x4008000000000000, 0x3fe0000000000000
  %".38" = fptosi double %".37" to i32
  %".39" = srem i32 %".36", %".38"
  %".40" = sitofp i32 %".39" to double
  %".41" = fcmp oeq double %".40",              0x0
  br i1 %".41", label %"then.1", label %"else"
then.1:
  store i32 65280, i32* @"c"
  br label %"endif.1"
endif.1:
  %".59" = load i32, i32* @"c"
  call void @"vg_set_color"(i32 %".59")
  %".61" = load double, double* %"x1"
  %".62" = fadd double %".61", 0x3fe0000000000000
  %".63" = fptosi double %".62" to i32
  %".64" = load double, double* %"y1"
  %".65" = fadd double %".64", 0x3fe0000000000000
  %".66" = fptosi double %".65" to i32
  %".67" = load double, double* @"x2"
  %".68" = fadd double %".67", 0x3fe0000000000000
  %".69" = fptosi double %".68" to i32
  %".70" = load double, double* @"y2"
  %".71" = fadd double %".70", 0x3fe0000000000000
  %".72" = fptosi double %".71" to i32
  call void @"vg_draw_line"(i32 %".63", i32 %".66", i32 %".69", i32 %".72")
  %".74" = load double, double* %"x1"
  %".75" = fadd double %".74", 0x3ff0000000000000
  %".76" = fadd double %".75", 0x3fe0000000000000
  %".77" = fptosi double %".76" to i32
  %".78" = load double, double* %"y1"
  %".79" = fadd double %".78", 0x3fe0000000000000
  %".80" = fptosi double %".79" to i32
  %".81" = load double, double* @"x2"
  %".82" = fadd double %".81", 0x3ff0000000000000
  %".83" = fadd double %".82", 0x3fe0000000000000
  %".84" = fptosi double %".83" to i32
  %".85" = load double, double* @"y2"
  %".86" = fadd double %".85", 0x3fe0000000000000
  %".87" = fptosi double %".86" to i32
  call void @"vg_draw_line"(i32 %".77", i32 %".80", i32 %".84", i32 %".87")
  %".89" = load double, double* %"x1"
  %".90" = fadd double %".89", 0x3fe0000000000000
  %".91" = fptosi double %".90" to i32
  %".92" = load double, double* %"y1"
  %".93" = fadd double %".92", 0x3ff0000000000000
  %".94" = fadd double %".93", 0x3fe0000000000000
  %".95" = fptosi double %".94" to i32
  %".96" = load double, double* @"x2"
  %".97" = fadd double %".96", 0x3fe0000000000000
  %".98" = fptosi double %".97" to i32
  %".99" = load double, double* @"y2"
  %".100" = fadd double %".99", 0x3ff0000000000000
  %".101" = fadd double %".100", 0x3fe0000000000000
  %".102" = fptosi double %".101" to i32
  call void @"vg_draw_line"(i32 %".91", i32 %".95", i32 %".98", i32 %".102")
  %".104" = load double, double* %"x1"
  %".105" = fadd double %".104", 0x3ff0000000000000
  %".106" = fadd double %".105", 0x3fe0000000000000
  %".107" = fptosi double %".106" to i32
  %".108" = load double, double* %"y1"
  %".109" = fadd double %".108", 0x3ff0000000000000
  %".110" = fadd double %".109", 0x3fe0000000000000
  %".111" = fptosi double %".110" to i32
  %".112" = load double, double* @"x2"
  %".113" = fadd double %".112", 0x3ff0000000000000
  %".114" = fadd double %".113", 0x3fe0000000000000
  %".115" = fptosi double %".114" to i32
  %".116" = load double, double* @"y2"
  %".117" = fadd double %".116", 0x3ff0000000000000
  %".118" = fadd double %".117", 0x3fe0000000000000
  %".119" = fptosi double %".118" to i32
  call void @"vg_draw_line"(i32 %".107", i32 %".111", i32 %".115", i32 %".119")
  %".121" = load double, double* @"x2"
  %".122" = load double, double* @"y2"
  %".123" = load double, double* %"length"
  %".124" = fmul double %".123", 0x3fe6666666666666
  %".125" = load double, double* %"angle"
  %".126" = fsub double %".125", 0x4039000000000000
  %".127" = load double, double* %"depth"
  %".128" = fsub double %".127", 0x3ff0000000000000
  call void @"tree"(double %".121", double %".122", double %".124", double %".126", double %".128")
  %".130" = load double, double* @"x2"
  %".131" = load double, double* @"y2"
  %".132" = load double, double* %"length"
  %".133" = fmul double %".132", 0x3fe6666666666666
  %".134" = load double, double* %"angle"
  %".135" = fadd double %".134", 0x4039000000000000
  %".136" = load double, double* %"depth"
  %".137" = fsub double %".136", 0x3ff0000000000000
  call void @"tree"(double %".130", double %".131", double %".133", double %".135", double %".137")
  ret void
else:
  %".45" = load double, double* %"depth"
  %".46" = fadd double %".45", 0x3fe0000000000000
  %".47" = fptosi double %".46" to i32
  %".48" = fadd double 0x4008000000000000, 0x3fe0000000000000
  %".49" = fptosi double %".48" to i32
  %".50" = srem i32 %".47", %".49"
  %".51" = sitofp i32 %".50" to double
  %".52" = fcmp oeq double %".51", 0x3ff0000000000000
  br i1 %".52", label %"then.2", label %"else.1"
then.2:
  store i32 8388608, i32* @"c"
  br label %"endif.2"
endif.2:
  br label %"endif.1"
else.1:
  store i32 16776960, i32* @"c"
  br label %"endif.2"
}

define i32 @"_main"()
{
entry:
  %".2" = call i32 @"main"()
  ret i32 %".2"
}
