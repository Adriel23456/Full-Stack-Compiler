; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@cx = local_unnamed_addr global double 0.000000e+00
@cy = local_unnamed_addr global double 0.000000e+00
@t = local_unnamed_addr global double 0.000000e+00
@seg = local_unnamed_addr global double 0.000000e+00
@ang = local_unnamed_addr global double 0.000000e+00
@x = local_unnamed_addr global double 0.000000e+00
@y = local_unnamed_addr global double 0.000000e+00
@ray = local_unnamed_addr global double 0.000000e+00
@x2 = local_unnamed_addr global double 0.000000e+00
@y2 = local_unnamed_addr global double 0.000000e+00
@blades = local_unnamed_addr global double 0.000000e+00
@col = local_unnamed_addr global i32 16777215
@switch.table.drawRing = private unnamed_addr constant [5 x i32] [i32 16711680, i32 16776960, i32 65280, i32 65535, i32 255], align 4

declare void @vg_set_color(i32) local_unnamed_addr

declare void @vg_draw_circle(i32, i32, i32) local_unnamed_addr

declare void @vg_draw_line(i32, i32, i32, i32) local_unnamed_addr

declare void @vg_draw_rect(i32, i32, i32, i32) local_unnamed_addr

declare void @vg_wait(i32) local_unnamed_addr

; Function Attrs: mustprogress nofree nounwind willreturn writeonly
declare double @cos(double) local_unnamed_addr #0

; Function Attrs: mustprogress nofree nounwind willreturn writeonly
declare double @sin(double) local_unnamed_addr #0

define i32 @main() local_unnamed_addr {
entry:
  store double 4.000000e+02, double* @cx, align 8
  store double 3.000000e+02, double* @cy, align 8
  store double 1.200000e+01, double* @blades, align 8
  store double 0.000000e+00, double* @t, align 8
  br label %for.body

for.body:                                         ; preds = %entry, %for.body
  tail call void @vg_set_color(i32 0)
  tail call void @vg_draw_rect(i32 0, i32 0, i32 799, i32 599)
  %.20 = load double, double* @t, align 8
  %.21 = load double, double* @blades, align 8
  tail call void @aperture(double %.20, double %.21, double 1.000000e+01, double 1.800000e+02)
  %.23 = load double, double* @t, align 8
  %.24 = fadd double %.23, 5.000000e-01
  %.25 = fptosi double %.24 to i32
  %.28 = srem i32 %.25, 20
  %addconv = add nsw i32 %.28, 60
  %.30 = sitofp i32 %addconv to double
  tail call void @drawRing(double %.30, double 2.400000e+01, double %.23, double 1.000000e+00)
  %.33 = load double, double* @t, align 8
  %.34 = fadd double %.33, 5.000000e-01
  %.35 = fptosi double %.34 to i32
  %.38 = srem i32 %.35, 20
  %.39 = sitofp i32 %.38 to double
  %.40 = fsub double 1.200000e+02, %.39
  %.42 = fmul double %.33, 1.500000e+00
  tail call void @drawRing(double %.40, double 3.000000e+01, double %.42, double -1.000000e+00)
  %.45 = load double, double* @t, align 8
  %.46 = fadd double %.45, 5.000000e-01
  %.47 = fptosi double %.46 to i32
  %.50 = srem i32 %.47, 15
  %addconv1 = add nsw i32 %.50, 180
  %.52 = sitofp i32 %addconv1 to double
  %.54 = fmul double %.45, 2.000000e+00
  tail call void @drawRing(double %.52, double 3.600000e+01, double %.54, double 1.000000e+00)
  %.56 = load double, double* @t, align 8
  %.57 = fadd double %.56, 5.000000e-01
  %.58 = fptosi double %.57 to i32
  %.61 = srem i32 %.58, 15
  %.62 = sitofp i32 %.61 to double
  %.63 = fsub double 2.400000e+02, %.62
  %.65 = fmul double %.56, 2.500000e+00
  tail call void @drawRing(double %.63, double 4.200000e+01, double %.65, double -1.000000e+00)
  tail call void @vg_wait(i32 100)
  %.72 = load double, double* @t, align 8
  %.73 = fadd double %.72, 3.000000e+00
  store double %.73, double* @t, align 8
  %.8 = fcmp olt double %.73, 3.600000e+05
  br i1 %.8, label %for.body, label %for.end

for.end:                                          ; preds = %for.body
  ret i32 0
}

define void @drawRing(double %.1, double %.2, double %.3, double %.4) local_unnamed_addr {
entry:
  store double 0.000000e+00, double* @seg, align 8
  %.141 = fcmp ogt double %.2, 0.000000e+00
  br i1 %.141, label %for.body.preheader, label %for.end

for.body.preheader:                               ; preds = %entry
  br label %for.body

for.body:                                         ; preds = %for.body.preheader, %endif
  %storemerge2 = phi double [ %.117, %endif ], [ 0.000000e+00, %for.body.preheader ]
  %.18 = fmul double %storemerge2, %.4
  %.19 = fmul double %.18, 3.600000e+02
  %.21 = fdiv double %.19, %.2
  %.23 = fadd double %.21, %.3
  store double %.23, double* @ang, align 8
  %.25 = load double, double* @cx, align 8
  %.28 = fmul double %.23, 3.141600e+00
  %.29 = fdiv double %.28, 1.800000e+02
  %.30 = tail call double @cos(double %.29)
  %.31 = fmul double %.30, %.1
  %.32 = fadd double %.25, %.31
  store double %.32, double* @x, align 8
  %.34 = load double, double* @cy, align 8
  %.36 = load double, double* @ang, align 8
  %.37 = fmul double %.36, 3.141600e+00
  %.38 = fdiv double %.37, 1.800000e+02
  %.39 = tail call double @sin(double %.38)
  %.40 = fmul double %.39, %.1
  %.41 = fadd double %.34, %.40
  store double %.41, double* @y, align 8
  %.43 = load double, double* @seg, align 8
  %.44 = fadd double %.43, 5.000000e-01
  %.45 = fptosi double %.44 to i32
  %.48 = srem i32 %.45, 6
  %0 = icmp ult i32 %.48, 5
  br i1 %0, label %switch.lookup, label %endif

for.end.loopexit:                                 ; preds = %endif
  br label %for.end

for.end:                                          ; preds = %for.end.loopexit, %entry
  ret void

switch.lookup:                                    ; preds = %for.body
  %1 = sext i32 %.48 to i64
  %switch.gep = getelementptr inbounds [5 x i32], [5 x i32]* @switch.table.drawRing, i64 0, i64 %1
  %switch.load = load i32, i32* %switch.gep, align 4
  br label %endif

endif:                                            ; preds = %for.body, %switch.lookup
  %.sink = phi i32 [ %switch.load, %switch.lookup ], [ 16711935, %for.body ]
  store i32 %.sink, i32* @col, align 4
  tail call void @vg_set_color(i32 %.sink)
  %.106 = load double, double* @x, align 8
  %.107 = fadd double %.106, 5.000000e-01
  %.108 = fptosi double %.107 to i32
  %.109 = load double, double* @y, align 8
  %.110 = fadd double %.109, 5.000000e-01
  %.111 = fptosi double %.110 to i32
  tail call void @vg_draw_circle(i32 %.108, i32 %.111, i32 5)
  %.116 = load double, double* @seg, align 8
  %.117 = fadd double %.116, 1.000000e+00
  store double %.117, double* @seg, align 8
  %.14 = fcmp olt double %.117, %.2
  br i1 %.14, label %for.body, label %for.end.loopexit
}

define void @aperture(double %.1, double %.2, double %.3, double %.4) local_unnamed_addr {
entry:
  store double 0.000000e+00, double* @ray, align 8
  %.142 = fcmp ogt double %.2, 0.000000e+00
  br i1 %.142, label %for.body.lr.ph, label %for.end

for.body.lr.ph:                                   ; preds = %entry
  %.21 = fmul double %.1, 2.000000e+00
  br label %for.body

for.body:                                         ; preds = %for.body.lr.ph, %for.body
  %storemerge3 = phi double [ 0.000000e+00, %for.body.lr.ph ], [ %.105, %for.body ]
  %.17 = fmul double %storemerge3, 3.600000e+02
  %.19 = fdiv double %.17, %.2
  %.22 = fadd double %.21, %.19
  store double %.22, double* @ang, align 8
  %.24 = load double, double* @cx, align 8
  %.27 = fmul double %.22, 3.141600e+00
  %.28 = fdiv double %.27, 1.800000e+02
  %.29 = tail call double @cos(double %.28)
  %.30 = fmul double %.29, %.3
  %.31 = fadd double %.24, %.30
  store double %.31, double* @x, align 8
  %.33 = load double, double* @cy, align 8
  %.35 = load double, double* @ang, align 8
  %.36 = fmul double %.35, 3.141600e+00
  %.37 = fdiv double %.36, 1.800000e+02
  %.38 = tail call double @sin(double %.37)
  %.39 = fmul double %.38, %.3
  %.40 = fadd double %.33, %.39
  store double %.40, double* @y, align 8
  %.42 = load double, double* @cx, align 8
  %.44 = load double, double* @ang, align 8
  %.45 = fmul double %.44, 3.141600e+00
  %.46 = fdiv double %.45, 1.800000e+02
  %.47 = tail call double @cos(double %.46)
  %.48 = fmul double %.47, %.4
  %.49 = fadd double %.42, %.48
  store double %.49, double* @x2, align 8
  %.51 = load double, double* @cy, align 8
  %.53 = load double, double* @ang, align 8
  %.54 = fmul double %.53, 3.141600e+00
  %.55 = fdiv double %.54, 1.800000e+02
  %.56 = tail call double @sin(double %.55)
  %.57 = fmul double %.56, %.4
  %.58 = fadd double %.51, %.57
  store double %.58, double* @y2, align 8
  %.60 = load double, double* @ray, align 8
  %.61 = fadd double %.60, 5.000000e-01
  %.62 = fptosi double %.61 to i32
  %0 = and i32 %.62, 1
  %.67 = icmp eq i32 %0, 0
  %. = select i1 %.67, i32 16777215, i32 65535
  store i32 %., i32* @col, align 4
  tail call void @vg_set_color(i32 %.)
  %.75 = load double, double* @x, align 8
  %.76 = fadd double %.75, 5.000000e-01
  %.77 = fptosi double %.76 to i32
  %.78 = load double, double* @y, align 8
  %.79 = fadd double %.78, 5.000000e-01
  %.80 = fptosi double %.79 to i32
  %.81 = load double, double* @x2, align 8
  %.82 = fadd double %.81, 5.000000e-01
  %.83 = fptosi double %.82 to i32
  %.84 = load double, double* @y2, align 8
  %.85 = fadd double %.84, 5.000000e-01
  %.86 = fptosi double %.85 to i32
  tail call void @vg_draw_line(i32 %.77, i32 %.80, i32 %.83, i32 %.86)
  %.88 = load double, double* @x, align 8
  %.89 = fadd double %.88, 1.000000e+00
  %.90 = fadd double %.89, 5.000000e-01
  %.91 = fptosi double %.90 to i32
  %.92 = load double, double* @y, align 8
  %.93 = fadd double %.92, 5.000000e-01
  %.94 = fptosi double %.93 to i32
  %.95 = load double, double* @x2, align 8
  %.96 = fadd double %.95, 1.000000e+00
  %.97 = fadd double %.96, 5.000000e-01
  %.98 = fptosi double %.97 to i32
  %.99 = load double, double* @y2, align 8
  %.100 = fadd double %.99, 5.000000e-01
  %.101 = fptosi double %.100 to i32
  tail call void @vg_draw_line(i32 %.91, i32 %.94, i32 %.98, i32 %.101)
  %.104 = load double, double* @ray, align 8
  %.105 = fadd double %.104, 1.000000e+00
  store double %.105, double* @ray, align 8
  %.14 = fcmp olt double %.105, %.2
  br i1 %.14, label %for.body, label %for.end.loopexit

for.end.loopexit:                                 ; preds = %for.body
  br label %for.end

for.end:                                          ; preds = %for.end.loopexit, %entry
  ret void
}

define i32 @_main() local_unnamed_addr {
entry:
  %.2 = tail call i32 @main()
  ret i32 0
}

attributes #0 = { mustprogress nofree nounwind willreturn writeonly }
