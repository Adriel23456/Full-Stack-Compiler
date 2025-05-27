; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@x = local_unnamed_addr global double 0.000000e+00
@y = local_unnamed_addr global double 0.000000e+00
@t = local_unnamed_addr global double 0.000000e+00
@c = local_unnamed_addr global i32 16777215

declare void @vg_set_color(i32) local_unnamed_addr

declare void @vg_draw_pixel(i32, i32) local_unnamed_addr

declare void @vg_clear() local_unnamed_addr

declare void @vg_wait(i32) local_unnamed_addr

; Function Attrs: mustprogress nofree nounwind willreturn writeonly
declare double @cos(double) local_unnamed_addr #0

; Function Attrs: mustprogress nofree nounwind willreturn writeonly
declare double @sin(double) local_unnamed_addr #0

define i32 @main() local_unnamed_addr {
entry:
  tail call void @vg_clear()
  store double 0.000000e+00, double* @t, align 8
  br label %for.body

for.body:                                         ; preds = %entry, %for.body
  %storemerge1 = phi double [ 0.000000e+00, %entry ], [ %.113, %for.body ]
  %.10 = fmul double %storemerge1, 3.141600e+00
  %.11 = fdiv double %.10, 1.800000e+02
  %.12 = tail call double @cos(double %.11)
  %.13 = fmul double %storemerge1, %.12
  %.14 = fadd double %.13, 3.200000e+02
  store double %.14, double* @x, align 8
  %.16 = load double, double* @t, align 8
  %.18 = fmul double %.16, 3.141600e+00
  %.19 = fdiv double %.18, 1.800000e+02
  %.20 = tail call double @sin(double %.19)
  %.21 = fmul double %.16, %.20
  %.22 = fadd double %.21, 2.400000e+02
  store double %.22, double* @y, align 8
  %.24 = load double, double* @t, align 8
  %.25 = fadd double %.24, 5.000000e-01
  %.26 = fptosi double %.25 to i32
  %.29 = srem i32 %.26, 3
  %switch.selectcmp = icmp eq i32 %.29, 1
  %switch.select = select i1 %switch.selectcmp, i32 255, i32 65280
  %switch.selectcmp3 = icmp eq i32 %.29, 0
  %switch.select4 = select i1 %switch.selectcmp3, i32 16711680, i32 %switch.select
  store i32 %switch.select4, i32* @c, align 4
  tail call void @vg_set_color(i32 %switch.select4)
  %.51 = load double, double* @x, align 8
  %.52 = fadd double %.51, 5.000000e-01
  %.53 = fptosi double %.52 to i32
  %.54 = load double, double* @y, align 8
  %.55 = fadd double %.54, 5.000000e-01
  %.56 = fptosi double %.55 to i32
  tail call void @vg_draw_pixel(i32 %.53, i32 %.56)
  %.58 = load double, double* @x, align 8
  %.59 = fadd double %.58, 1.000000e+00
  %.60 = fadd double %.59, 5.000000e-01
  %.61 = fptosi double %.60 to i32
  %.62 = load double, double* @y, align 8
  %.63 = fadd double %.62, 1.000000e+00
  %.64 = fadd double %.63, 5.000000e-01
  %.65 = fptosi double %.64 to i32
  tail call void @vg_draw_pixel(i32 %.61, i32 %.65)
  %.67 = load double, double* @x, align 8
  %.68 = fadd double %.67, 1.000000e+00
  %.69 = fadd double %.68, 5.000000e-01
  %.70 = fptosi double %.69 to i32
  %.71 = load double, double* @y, align 8
  %.72 = fadd double %.71, 5.000000e-01
  %.73 = fptosi double %.72 to i32
  tail call void @vg_draw_pixel(i32 %.70, i32 %.73)
  %.75 = load double, double* @x, align 8
  %.76 = fadd double %.75, 5.000000e-01
  %.77 = fptosi double %.76 to i32
  %.78 = load double, double* @y, align 8
  %.79 = fadd double %.78, 1.000000e+00
  %.80 = fadd double %.79, 5.000000e-01
  %.81 = fptosi double %.80 to i32
  tail call void @vg_draw_pixel(i32 %.77, i32 %.81)
  %.83 = load double, double* @x, align 8
  %.84 = fadd double %.83, -1.000000e+00
  %.85 = fadd double %.84, 5.000000e-01
  %.86 = fptosi double %.85 to i32
  %.87 = load double, double* @y, align 8
  %.88 = fadd double %.87, -1.000000e+00
  %.89 = fadd double %.88, 5.000000e-01
  %.90 = fptosi double %.89 to i32
  tail call void @vg_draw_pixel(i32 %.86, i32 %.90)
  %.92 = load double, double* @x, align 8
  %.93 = fadd double %.92, -1.000000e+00
  %.94 = fadd double %.93, 5.000000e-01
  %.95 = fptosi double %.94 to i32
  %.96 = load double, double* @y, align 8
  %.97 = fadd double %.96, 5.000000e-01
  %.98 = fptosi double %.97 to i32
  tail call void @vg_draw_pixel(i32 %.95, i32 %.98)
  %.100 = load double, double* @x, align 8
  %.101 = fadd double %.100, 5.000000e-01
  %.102 = fptosi double %.101 to i32
  %.103 = load double, double* @y, align 8
  %.104 = fadd double %.103, -1.000000e+00
  %.105 = fadd double %.104, 5.000000e-01
  %.106 = fptosi double %.105 to i32
  tail call void @vg_draw_pixel(i32 %.102, i32 %.106)
  tail call void @vg_wait(i32 100)
  %.112 = load double, double* @t, align 8
  %.113 = fadd double %.112, 5.000000e+00
  store double %.113, double* @t, align 8
  %.6 = fcmp olt double %.113, 3.600000e+02
  br i1 %.6, label %for.body, label %for.end

for.end:                                          ; preds = %for.body
  ret i32 0
}

define i32 @_main() local_unnamed_addr {
entry:
  %.2 = tail call i32 @main()
  ret i32 0
}

attributes #0 = { mustprogress nofree nounwind willreturn writeonly }
