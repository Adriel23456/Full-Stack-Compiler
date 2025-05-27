; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc"

@x1 = local_unnamed_addr global double 0.000000e+00
@y1 = local_unnamed_addr global double 0.000000e+00
@x2 = local_unnamed_addr global double 0.000000e+00
@y2 = local_unnamed_addr global double 0.000000e+00
@len100 = local_unnamed_addr global double 0.000000e+00
@ang = local_unnamed_addr global double 0.000000e+00
@depth = local_unnamed_addr global double 0.000000e+00
@axis = local_unnamed_addr global double 0.000000e+00
@pos = local_unnamed_addr global double 0.000000e+00
@col = local_unnamed_addr global i32 16777215
@switch.table.triBranch = private unnamed_addr constant [5 x i32] [i32 16711680, i32 16776960, i32 65280, i32 65535, i32 255], align 4

declare void @vg_set_color(i32) local_unnamed_addr

declare void @vg_draw_circle(i32, i32, i32) local_unnamed_addr

declare void @vg_draw_line(i32, i32, i32, i32) local_unnamed_addr

declare void @vg_draw_rect(i32, i32, i32, i32) local_unnamed_addr

; Function Attrs: mustprogress nofree nounwind willreturn writeonly
declare double @cos(double) local_unnamed_addr #0

; Function Attrs: mustprogress nofree nounwind willreturn writeonly
declare double @sin(double) local_unnamed_addr #0

define i32 @main() local_unnamed_addr {
entry:
  tail call void @vg_set_color(i32 0)
  tail call void @vg_draw_rect(i32 0, i32 0, i32 799, i32 599)
  store double 5.000000e+00, double* @depth, align 8
  store double 1.600000e+03, double* @len100, align 8
  store double 0.000000e+00, double* @pos, align 8
  br label %for.body

for.body:                                         ; preds = %entry, %for.end.1
  %storemerge3 = phi double [ 0.000000e+00, %entry ], [ %.77, %for.end.1 ]
  %.20 = fcmp oeq double %storemerge3, 0.000000e+00
  br i1 %.20, label %endif, label %else

for.end:                                          ; preds = %for.end.1
  ret i32 0

endif:                                            ; preds = %for.body, %else.3, %else.2, %else.1, %else
  %.sink4 = phi double [ 6.500000e+02, %else ], [ 4.000000e+02, %else.1 ], [ 1.500000e+02, %else.2 ], [ %., %else.3 ], [ 1.500000e+02, %for.body ]
  %.sink = phi double [ 1.500000e+02, %else ], [ 1.000000e+02, %else.1 ], [ 4.500000e+02, %else.2 ], [ %.5, %else.3 ], [ 1.500000e+02, %for.body ]
  store double %.sink4, double* @x1, align 8
  store double %.sink, double* @y1, align 8
  store double 0.000000e+00, double* @axis, align 8
  br label %for.body.1

else:                                             ; preds = %for.body
  %.26 = fcmp oeq double %storemerge3, 1.000000e+00
  br i1 %.26, label %endif, label %else.1

else.1:                                           ; preds = %else
  %.32 = fcmp oeq double %storemerge3, 2.000000e+00
  br i1 %.32, label %endif, label %else.2

else.2:                                           ; preds = %else.1
  %.38 = fcmp oeq double %storemerge3, 3.000000e+00
  br i1 %.38, label %endif, label %else.3

else.3:                                           ; preds = %else.2
  %.44 = fcmp oeq double %storemerge3, 4.000000e+00
  %. = select i1 %.44, double 6.500000e+02, double 4.000000e+02
  %.5 = select i1 %.44, double 4.500000e+02, double 5.000000e+02
  br label %endif

for.body.1:                                       ; preds = %endif, %for.body.1
  %storemerge12 = phi double [ 0.000000e+00, %endif ], [ %.72, %for.body.1 ]
  %.62 = fmul double %storemerge12, 6.000000e+01
  store double %.62, double* @ang, align 8
  %.64 = load double, double* @x1, align 8
  %.65 = load double, double* @y1, align 8
  %.66 = load double, double* @len100, align 8
  %.68 = load double, double* @depth, align 8
  tail call void @triBranch(double %.64, double %.65, double %.66, double %.62, double %.68)
  %.71 = load double, double* @axis, align 8
  %.72 = fadd double %.71, 1.000000e+00
  store double %.72, double* @axis, align 8
  %.59 = fcmp olt double %.72, 6.000000e+00
  br i1 %.59, label %for.body.1, label %for.end.1

for.end.1:                                        ; preds = %for.body.1
  %.76 = load double, double* @pos, align 8
  %.77 = fadd double %.76, 1.000000e+00
  store double %.77, double* @pos, align 8
  %.17 = fcmp olt double %.77, 6.000000e+00
  br i1 %.17, label %for.body, label %for.end
}

define void @triBranch(double %.1, double %.2, double %.3, double %.4, double %.5) local_unnamed_addr {
entry:
  %.136 = fcmp oeq double %.5, 0.000000e+00
  br i1 %.136, label %then, label %endif.preheader

endif.preheader:                                  ; preds = %entry
  br label %endif

then.loopexit:                                    ; preds = %endif.1
  %.156.lcssa = phi double [ %.156, %endif.1 ]
  %.157.lcssa = phi double [ %.157, %endif.1 ]
  br label %then

then:                                             ; preds = %then.loopexit, %entry
  %.1.tr.lcssa = phi double [ %.1, %entry ], [ %.156.lcssa, %then.loopexit ]
  %.2.tr.lcssa = phi double [ %.2, %entry ], [ %.157.lcssa, %then.loopexit ]
  tail call void @vg_set_color(i32 65280)
  %.17 = fadd double %.1.tr.lcssa, 5.000000e-01
  %.18 = fptosi double %.17 to i32
  %.20 = fadd double %.2.tr.lcssa, 5.000000e-01
  %.21 = fptosi double %.20 to i32
  tail call void @vg_draw_circle(i32 %.18, i32 %.21, i32 2)
  ret void

endif:                                            ; preds = %endif.preheader, %endif.1
  %.5.tr11 = phi double [ %.146, %endif.1 ], [ %.5, %endif.preheader ]
  %.4.tr10 = phi double [ %.160, %endif.1 ], [ %.4, %endif.preheader ]
  %.3.tr9 = phi double [ %.139, %endif.1 ], [ %.3, %endif.preheader ]
  %.2.tr8 = phi double [ %.157, %endif.1 ], [ %.2, %endif.preheader ]
  %.1.tr7 = phi double [ %.156, %endif.1 ], [ %.1, %endif.preheader ]
  %.29 = fmul double %.4.tr10, 3.141600e+00
  %.30 = fdiv double %.29, 1.800000e+02
  %.31 = tail call double @cos(double %.30)
  %.32 = fmul double %.3.tr9, %.31
  %.33 = fdiv double %.32, 1.000000e+02
  %.34 = fadd double %.1.tr7, %.33
  store double %.34, double* @x2, align 8
  %.41 = tail call double @sin(double %.30)
  %.42 = fmul double %.3.tr9, %.41
  %.43 = fdiv double %.42, 1.000000e+02
  %.44 = fsub double %.2.tr8, %.43
  store double %.44, double* @y2, align 8
  %.47 = fadd double %.5.tr11, 5.000000e-01
  %.48 = fptosi double %.47 to i32
  %.51 = srem i32 %.48, 6
  %0 = icmp ult i32 %.51, 5
  br i1 %0, label %switch.lookup, label %endif.1

switch.lookup:                                    ; preds = %endif
  %1 = sext i32 %.51 to i64
  %switch.gep = getelementptr inbounds [5 x i32], [5 x i32]* @switch.table.triBranch, i64 0, i64 %1
  %switch.load = load i32, i32* %switch.gep, align 4
  br label %endif.1

endif.1:                                          ; preds = %endif, %switch.lookup
  %.sink = phi i32 [ %switch.load, %switch.lookup ], [ 16711935, %endif ]
  store i32 %.sink, i32* @col, align 4
  tail call void @vg_set_color(i32 %.sink)
  %.110 = fadd double %.1.tr7, 5.000000e-01
  %.111 = fptosi double %.110 to i32
  %.113 = fadd double %.2.tr8, 5.000000e-01
  %.114 = fptosi double %.113 to i32
  %.115 = load double, double* @x2, align 8
  %.116 = fadd double %.115, 5.000000e-01
  %.117 = fptosi double %.116 to i32
  %.118 = load double, double* @y2, align 8
  %.119 = fadd double %.118, 5.000000e-01
  %.120 = fptosi double %.119 to i32
  tail call void @vg_draw_line(i32 %.111, i32 %.114, i32 %.117, i32 %.120)
  %.123 = fadd double %.1.tr7, 1.000000e+00
  %.124 = fadd double %.123, 5.000000e-01
  %.125 = fptosi double %.124 to i32
  %.129 = load double, double* @x2, align 8
  %.130 = fadd double %.129, 1.000000e+00
  %.131 = fadd double %.130, 5.000000e-01
  %.132 = fptosi double %.131 to i32
  %.133 = load double, double* @y2, align 8
  %.134 = fadd double %.133, 5.000000e-01
  %.135 = fptosi double %.134 to i32
  tail call void @vg_draw_line(i32 %.125, i32 %.114, i32 %.132, i32 %.135)
  %.138 = fmul double %.3.tr9, 5.000000e+01
  %.139 = fdiv double %.138, 1.000000e+02
  %.141 = load double, double* @x2, align 8
  %.142 = load double, double* @y2, align 8
  %.146 = fadd double %.5.tr11, -1.000000e+00
  tail call void @triBranch(double %.141, double %.142, double %.139, double %.4.tr10, double %.146)
  %.148 = load double, double* @x2, align 8
  %.149 = load double, double* @y2, align 8
  %.152 = fadd double %.4.tr10, -6.000000e+01
  tail call void @triBranch(double %.148, double %.149, double %.139, double %.152, double %.146)
  %.156 = load double, double* @x2, align 8
  %.157 = load double, double* @y2, align 8
  %.160 = fadd double %.4.tr10, 6.000000e+01
  %.13 = fcmp oeq double %.146, 0.000000e+00
  br i1 %.13, label %then.loopexit, label %endif
}

define i32 @_main() local_unnamed_addr {
entry:
  %.2 = tail call i32 @main()
  ret i32 0
}

attributes #0 = { mustprogress nofree nounwind willreturn writeonly }
