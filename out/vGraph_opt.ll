; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@cx = local_unnamed_addr global double 0.000000e+00
@cy = local_unnamed_addr global double 0.000000e+00
@t = local_unnamed_addr global double 0.000000e+00
@arm = local_unnamed_addr global double 0.000000e+00
@ang = local_unnamed_addr global double 0.000000e+00
@rad = local_unnamed_addr global double 0.000000e+00
@x = local_unnamed_addr global double 0.000000e+00
@y = local_unnamed_addr global double 0.000000e+00
@star = local_unnamed_addr global double 0.000000e+00
@sx = local_unnamed_addr global double 0.000000e+00
@sy = local_unnamed_addr global double 0.000000e+00
@sparkleT = local_unnamed_addr global double 0.000000e+00
@col = local_unnamed_addr global i32 16777215
@switch.table.main = private unnamed_addr constant [5 x i32] [i32 16711680, i32 16776960, i32 65280, i32 65535, i32 255], align 4

declare void @vg_set_color(i32) local_unnamed_addr

declare void @vg_draw_pixel(i32, i32) local_unnamed_addr

declare void @vg_draw_circle(i32, i32, i32) local_unnamed_addr

declare void @vg_draw_rect(i32, i32, i32, i32) local_unnamed_addr

declare void @vg_clear() local_unnamed_addr

declare void @vg_wait(i32) local_unnamed_addr

; Function Attrs: mustprogress nofree nounwind willreturn writeonly
declare double @cos(double) local_unnamed_addr #0

; Function Attrs: mustprogress nofree nounwind willreturn writeonly
declare double @sin(double) local_unnamed_addr #0

define i32 @main() local_unnamed_addr {
entry:
  store double 4.000000e+02, double* @cx, align 8
  store double 3.000000e+02, double* @cy, align 8
  tail call void @vg_clear()
  tail call void @vg_set_color(i32 0)
  tail call void @vg_draw_rect(i32 0, i32 0, i32 799, i32 599)
  store double 0.000000e+00, double* @t, align 8
  br label %for.body

for.body:                                         ; preds = %entry, %endif.7
  %storemerge9 = phi double [ 0.000000e+00, %entry ], [ %.316, %endif.7 ]
  %.21 = fdiv double %storemerge9, 2.000000e+01
  %.22 = fadd double %.21, 5.000000e-01
  %.23 = fptosi double %.22 to i32
  %0 = and i32 %.23, 1
  %.28 = icmp eq i32 %0, 0
  %. = select i1 %.28, i32 16777215, i32 65535
  store i32 %., i32* @col, align 4
  tail call void @vg_set_color(i32 %.)
  %.36 = load double, double* @cx, align 8
  %.37 = fadd double %.36, 5.000000e-01
  %.38 = fptosi double %.37 to i32
  %.39 = load double, double* @cy, align 8
  %.40 = fadd double %.39, 5.000000e-01
  %.41 = fptosi double %.40 to i32
  %.42 = load double, double* @t, align 8
  %.43 = fadd double %.42, 5.000000e-01
  %.44 = fptosi double %.43 to i32
  %.47 = srem i32 %.44, 20
  %.48 = sitofp i32 %.47 to double
  %.49 = fmul double %.48, 5.000000e-01
  %.50 = fadd double %.49, 1.200000e+01
  %.51 = fadd double %.50, 5.000000e-01
  %.52 = fptosi double %.51 to i32
  tail call void @vg_draw_circle(i32 %.38, i32 %.41, i32 %.52)
  store double 0.000000e+00, double* @arm, align 8
  br label %for.cond.2.preheader

for.end:                                          ; preds = %endif.7
  ret i32 0

for.cond.3.preheader:                             ; preds = %for.end.2
  store double 0.000000e+00, double* @star, align 8
  br label %for.body.3

for.cond.2.preheader:                             ; preds = %for.body, %for.end.2
  store double 6.000000e+00, double* @rad, align 8
  br label %for.body.2

for.body.2:                                       ; preds = %for.cond.2.preheader, %endif.1
  %storemerge57 = phi double [ 6.000000e+00, %for.cond.2.preheader ], [ %.212, %endif.1 ]
  %.65 = load double, double* @t, align 8
  %.66 = load double, double* @arm, align 8
  %.67 = fmul double %.66, 6.000000e+01
  %.68 = fadd double %.65, %.67
  %.70 = fadd double %storemerge57, %.68
  store double %.70, double* @ang, align 8
  %.72 = load double, double* @cx, align 8
  %.75 = fmul double %.70, 3.141600e+00
  %.76 = fdiv double %.75, 1.800000e+02
  %.77 = tail call double @cos(double %.76)
  %.78 = fmul double %storemerge57, %.77
  %.79 = fadd double %.72, %.78
  store double %.79, double* @x, align 8
  %.81 = load double, double* @cy, align 8
  %.82 = load double, double* @rad, align 8
  %.83 = load double, double* @ang, align 8
  %.84 = fmul double %.83, 3.141600e+00
  %.85 = fdiv double %.84, 1.800000e+02
  %.86 = tail call double @sin(double %.85)
  %.87 = fmul double %.82, %.86
  %.88 = fadd double %.81, %.87
  store double %.88, double* @y, align 8
  %.90 = load double, double* @rad, align 8
  %.91 = fdiv double %.90, 2.400000e+01
  %.92 = load double, double* @arm, align 8
  %.93 = fadd double %.91, %.92
  %.94 = fadd double %.93, 5.000000e-01
  %.95 = fptosi double %.94 to i32
  %.98 = srem i32 %.95, 6
  %1 = icmp ult i32 %.98, 5
  br i1 %1, label %switch.lookup, label %endif.1

for.end.2:                                        ; preds = %endif.1
  %.216 = load double, double* @arm, align 8
  %.217 = fadd double %.216, 1.000000e+00
  store double %.217, double* @arm, align 8
  %.57 = fcmp olt double %.217, 6.000000e+00
  br i1 %.57, label %for.cond.2.preheader, label %for.cond.3.preheader

switch.lookup:                                    ; preds = %for.body.2
  %2 = sext i32 %.98 to i64
  %switch.gep = getelementptr inbounds [5 x i32], [5 x i32]* @switch.table.main, i64 0, i64 %2
  %switch.load = load i32, i32* %switch.gep, align 4
  br label %endif.1

endif.1:                                          ; preds = %for.body.2, %switch.lookup
  %.sink = phi i32 [ %switch.load, %switch.lookup ], [ 16711935, %for.body.2 ]
  store i32 %.sink, i32* @col, align 4
  tail call void @vg_set_color(i32 %.sink)
  %.168 = load double, double* @x, align 8
  %.169 = fadd double %.168, 5.000000e-01
  %.170 = fptosi double %.169 to i32
  %.171 = load double, double* @y, align 8
  %.172 = fadd double %.171, 5.000000e-01
  %.173 = fptosi double %.172 to i32
  tail call void @vg_draw_circle(i32 %.170, i32 %.173, i32 4)
  tail call void @vg_set_color(i32 16777215)
  %.178 = load double, double* @x, align 8
  %.179 = fadd double %.178, 2.000000e+00
  %.180 = fadd double %.179, 5.000000e-01
  %.181 = fptosi double %.180 to i32
  %.182 = load double, double* @y, align 8
  %.183 = fadd double %.182, 5.000000e-01
  %.184 = fptosi double %.183 to i32
  tail call void @vg_draw_pixel(i32 %.181, i32 %.184)
  %.186 = load double, double* @x, align 8
  %.187 = fadd double %.186, -2.000000e+00
  %.188 = fadd double %.187, 5.000000e-01
  %.189 = fptosi double %.188 to i32
  %.190 = load double, double* @y, align 8
  %.191 = fadd double %.190, 5.000000e-01
  %.192 = fptosi double %.191 to i32
  tail call void @vg_draw_pixel(i32 %.189, i32 %.192)
  %.194 = load double, double* @x, align 8
  %.195 = fadd double %.194, 5.000000e-01
  %.196 = fptosi double %.195 to i32
  %.197 = load double, double* @y, align 8
  %.198 = fadd double %.197, 2.000000e+00
  %.199 = fadd double %.198, 5.000000e-01
  %.200 = fptosi double %.199 to i32
  tail call void @vg_draw_pixel(i32 %.196, i32 %.200)
  %.202 = load double, double* @x, align 8
  %.203 = fadd double %.202, 5.000000e-01
  %.204 = fptosi double %.203 to i32
  %.205 = load double, double* @y, align 8
  %.206 = fadd double %.205, -2.000000e+00
  %.207 = fadd double %.206, 5.000000e-01
  %.208 = fptosi double %.207 to i32
  tail call void @vg_draw_pixel(i32 %.204, i32 %.208)
  %.211 = load double, double* @rad, align 8
  %.212 = fadd double %.211, 6.000000e+00
  store double %.212, double* @rad, align 8
  %.63 = fcmp olt double %.212, 2.600000e+02
  br i1 %.63, label %for.body.2, label %for.end.2

for.body.3:                                       ; preds = %for.cond.3.preheader, %for.body.3
  %storemerge38 = phi double [ 0.000000e+00, %for.cond.3.preheader ], [ %.277, %for.body.3 ]
  %.225 = load double, double* @t, align 8
  %.226 = fmul double %.225, 1.300000e+01
  %.228 = fmul double %storemerge38, 9.700000e+01
  %.229 = fadd double %.228, %.226
  %.230 = fadd double %.229, 5.000000e-01
  %.231 = fptosi double %.230 to i32
  %.234 = srem i32 %.231, 800
  %.235 = sitofp i32 %.234 to double
  store double %.235, double* @sx, align 8
  %.238 = fmul double %.225, 2.900000e+01
  %.240 = fmul double %storemerge38, 5.300000e+01
  %.241 = fadd double %.240, %.238
  %.242 = fadd double %.241, 5.000000e-01
  %.243 = fptosi double %.242 to i32
  %.246 = srem i32 %.243, 600
  %.247 = sitofp i32 %.246 to double
  store double %.247, double* @sy, align 8
  %.251 = fmul double %storemerge38, 7.000000e+00
  %.252 = fadd double %.251, %.225
  %.253 = fdiv double %.252, 1.000000e+01
  %.254 = fadd double %.253, 5.000000e-01
  %.255 = fptosi double %.254 to i32
  %3 = and i32 %.255, 1
  %.260 = icmp eq i32 %3, 0
  %.6 = select i1 %.260, i32 16777215, i32 65535
  store i32 %.6, i32* @col, align 4
  tail call void @vg_set_color(i32 %.6)
  %.268 = load double, double* @sx, align 8
  %.269 = fadd double %.268, 5.000000e-01
  %.270 = fptosi double %.269 to i32
  %.271 = load double, double* @sy, align 8
  %.272 = fadd double %.271, 5.000000e-01
  %.273 = fptosi double %.272 to i32
  tail call void @vg_draw_pixel(i32 %.270, i32 %.273)
  %.276 = load double, double* @star, align 8
  %.277 = fadd double %.276, 1.000000e+00
  store double %.277, double* @star, align 8
  %.223 = fcmp olt double %.277, 5.000000e+01
  br i1 %.223, label %for.body.3, label %for.end.3

for.end.3:                                        ; preds = %for.body.3
  %.280 = load double, double* @t, align 8
  %.281 = fadd double %.280, 5.000000e-01
  %.282 = fptosi double %.281 to i32
  %.285 = srem i32 %.282, 180
  %.287 = icmp eq i32 %.285, 0
  br i1 %.287, label %then.7, label %endif.7

then.7:                                           ; preds = %for.end.3
  %.289 = load double, double* @cx, align 8
  %.291 = fadd double %.280, 1.230000e+02
  %.292 = fmul double %.291, 3.141600e+00
  %.293 = fdiv double %.292, 1.800000e+02
  %.294 = tail call double @cos(double %.293)
  %.295 = fmul double %.294, 2.600000e+02
  %.296 = fadd double %.289, %.295
  store double %.296, double* @sx, align 8
  %.298 = load double, double* @cy, align 8
  %.299 = load double, double* @t, align 8
  %.300 = fadd double %.299, 1.230000e+02
  %.301 = fmul double %.300, 3.141600e+00
  %.302 = fdiv double %.301, 1.800000e+02
  %.303 = tail call double @sin(double %.302)
  %.304 = fmul double %.303, 2.600000e+02
  %.305 = fadd double %.298, %.304
  store double %.305, double* @sy, align 8
  %.307 = load double, double* @sx, align 8
  store double 0.000000e+00, double* @sparkleT, align 8
  %.27.i = fadd double %.307, 5.000000e-01
  %.28.i = fptosi double %.27.i to i32
  %.30.i = fadd double %.305, 5.000000e-01
  %.31.i = fptosi double %.30.i to i32
  br label %for.body.i

for.body.i:                                       ; preds = %for.body.i, %then.7
  %storemerge2.i = phi double [ 0.000000e+00, %then.7 ], [ %.40.i, %for.body.i ]
  %.12.i = fadd double %storemerge2.i, 5.000000e-01
  %.13.i = fptosi double %.12.i to i32
  %4 = and i32 %.13.i, 1
  %.18.i = icmp eq i32 %4, 0
  %..i = select i1 %.18.i, i32 16711935, i32 16776960
  store i32 %..i, i32* @col, align 4
  tail call void @vg_set_color(i32 %..i)
  %.32.i = load double, double* @sparkleT, align 8
  %.33.i = fmul double %.32.i, 5.000000e-01
  %.34.i = fsub double 4.000000e+00, %.33.i
  %.35.i = fadd double %.34.i, 5.000000e-01
  %.36.i = fptosi double %.35.i to i32
  tail call void @vg_draw_circle(i32 %.28.i, i32 %.31.i, i32 %.36.i)
  %.39.i = load double, double* @sparkleT, align 8
  %.40.i = fadd double %.39.i, 1.000000e+00
  store double %.40.i, double* @sparkleT, align 8
  %.9.i = fcmp olt double %.40.i, 6.000000e+00
  br i1 %.9.i, label %for.body.i, label %endif.7.loopexit

endif.7.loopexit:                                 ; preds = %for.body.i
  br label %endif.7

endif.7:                                          ; preds = %endif.7.loopexit, %for.end.3
  tail call void @vg_wait(i32 2)
  %.315 = load double, double* @t, align 8
  %.316 = fadd double %.315, 2.000000e+00
  store double %.316, double* @t, align 8
  %.18 = fcmp olt double %.316, 3.600000e+04
  br i1 %.18, label %for.body, label %for.end
}

define void @sparkle(double %.1, double %.2) local_unnamed_addr {
entry:
  store double 0.000000e+00, double* @sparkleT, align 8
  %.27 = fadd double %.1, 5.000000e-01
  %.28 = fptosi double %.27 to i32
  %.30 = fadd double %.2, 5.000000e-01
  %.31 = fptosi double %.30 to i32
  br label %for.body

for.body:                                         ; preds = %entry, %for.body
  %storemerge2 = phi double [ 0.000000e+00, %entry ], [ %.40, %for.body ]
  %.12 = fadd double %storemerge2, 5.000000e-01
  %.13 = fptosi double %.12 to i32
  %0 = and i32 %.13, 1
  %.18 = icmp eq i32 %0, 0
  %. = select i1 %.18, i32 16711935, i32 16776960
  store i32 %., i32* @col, align 4
  tail call void @vg_set_color(i32 %.)
  %.32 = load double, double* @sparkleT, align 8
  %.33 = fmul double %.32, 5.000000e-01
  %.34 = fsub double 4.000000e+00, %.33
  %.35 = fadd double %.34, 5.000000e-01
  %.36 = fptosi double %.35 to i32
  tail call void @vg_draw_circle(i32 %.28, i32 %.31, i32 %.36)
  %.39 = load double, double* @sparkleT, align 8
  %.40 = fadd double %.39, 1.000000e+00
  store double %.40, double* @sparkleT, align 8
  %.9 = fcmp olt double %.40, 6.000000e+00
  br i1 %.9, label %for.body, label %for.end

for.end:                                          ; preds = %for.body
  ret void
}

define i32 @_main() local_unnamed_addr {
entry:
  %.2 = tail call i32 @main()
  ret i32 0
}

attributes #0 = { mustprogress nofree nounwind willreturn writeonly }
