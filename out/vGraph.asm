# VGraph Assembly Code
# Generated from LLVM IR
# Target: x86-64
# Syntax: AT&T (GNU Assembler)

	.text
	.file	"<string>"
	.section	.rodata.cst8,"aM",@progbits,8
	.p2align	3
.LCPI0_0:
	.quad	0x4024000000000000
.LCPI0_1:
	.quad	0x4066800000000000
.LCPI0_2:
	.quad	0x3fe0000000000000
.LCPI0_3:
	.quad	0x4038000000000000
.LCPI0_4:
	.quad	0x3ff0000000000000
.LCPI0_5:
	.quad	0x405e000000000000
.LCPI0_6:
	.quad	0x3ff8000000000000
.LCPI0_7:
	.quad	0x403e000000000000
.LCPI0_8:
	.quad	0xbff0000000000000
.LCPI0_9:
	.quad	0x4042000000000000
.LCPI0_10:
	.quad	0x406e000000000000
.LCPI0_11:
	.quad	0x4004000000000000
.LCPI0_12:
	.quad	0x4045000000000000
.LCPI0_13:
	.quad	0x4008000000000000
.LCPI0_14:
	.quad	0x4115f90000000000
	.text
	.globl	main
	.p2align	4, 0x90
	.type	main,@function
main:
	.cfi_startproc
	pushq	%r14
	.cfi_def_cfa_offset 16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	pushq	%rax
	.cfi_def_cfa_offset 32
	.cfi_offset %rbx, -24
	.cfi_offset %r14, -16
	movq	cx@GOTPCREL(%rip), %rax
	movabsq	$4645744490609377280, %rcx
	movq	%rcx, (%rax)
	movq	cy@GOTPCREL(%rip), %rax
	movabsq	$4643985272004935680, %rcx
	movq	%rcx, (%rax)
	movq	blades@GOTPCREL(%rip), %r14
	movabsq	$4622945017495814144, %rax
	movq	%rax, (%r14)
	movq	t@GOTPCREL(%rip), %rbx
	movq	$0, (%rbx)
	.p2align	4, 0x90
.LBB0_1:
	xorl	%edi, %edi
	callq	vg_set_color@PLT
	xorl	%edi, %edi
	xorl	%esi, %esi
	movl	$799, %edx
	movl	$599, %ecx
	callq	vg_draw_rect@PLT
	movsd	(%rbx), %xmm0
	movsd	(%r14), %xmm1
	movsd	.LCPI0_0(%rip), %xmm2
	movsd	.LCPI0_1(%rip), %xmm3
	callq	aperture@PLT
	movsd	(%rbx), %xmm2
	movapd	%xmm2, %xmm0
	movsd	.LCPI0_2(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %eax
	cltq
	imulq	$1717986919, %rax, %rcx
	movq	%rcx, %rdx
	shrq	$63, %rdx
	shrq	$32, %rcx
	sarl	$3, %ecx
	addl	%edx, %ecx
	shll	$2, %ecx
	leal	(%rcx,%rcx,4), %ecx
	negl	%ecx
	leal	60(%rax,%rcx), %eax
	xorps	%xmm0, %xmm0
	cvtsi2sd	%eax, %xmm0
	movsd	.LCPI0_3(%rip), %xmm1
	movsd	.LCPI0_4(%rip), %xmm3
	callq	drawRing@PLT
	movsd	(%rbx), %xmm2
	movapd	%xmm2, %xmm0
	addsd	.LCPI0_2(%rip), %xmm0
	cvttsd2si	%xmm0, %eax
	cltq
	imulq	$1717986919, %rax, %rcx
	movq	%rcx, %rdx
	shrq	$63, %rdx
	shrq	$32, %rcx
	sarl	$3, %ecx
	addl	%edx, %ecx
	shll	$2, %ecx
	leal	(%rcx,%rcx,4), %ecx
	subl	%ecx, %eax
	xorps	%xmm1, %xmm1
	cvtsi2sd	%eax, %xmm1
	movsd	.LCPI0_5(%rip), %xmm0
	subsd	%xmm1, %xmm0
	mulsd	.LCPI0_6(%rip), %xmm2
	movsd	.LCPI0_7(%rip), %xmm1
	movsd	.LCPI0_8(%rip), %xmm3
	callq	drawRing@PLT
	movsd	(%rbx), %xmm2
	movapd	%xmm2, %xmm0
	addsd	.LCPI0_2(%rip), %xmm0
	cvttsd2si	%xmm0, %eax
	cltq
	imulq	$-2004318071, %rax, %rcx
	shrq	$32, %rcx
	addl	%eax, %ecx
	movl	%ecx, %edx
	shrl	$31, %edx
	sarl	$3, %ecx
	addl	%edx, %ecx
	leal	(%rcx,%rcx,4), %ecx
	leal	(%rcx,%rcx,2), %ecx
	negl	%ecx
	leal	180(%rax,%rcx), %eax
	xorps	%xmm0, %xmm0
	cvtsi2sd	%eax, %xmm0
	addsd	%xmm2, %xmm2
	movsd	.LCPI0_9(%rip), %xmm1
	movsd	.LCPI0_4(%rip), %xmm3
	callq	drawRing@PLT
	movsd	(%rbx), %xmm2
	movapd	%xmm2, %xmm0
	addsd	.LCPI0_2(%rip), %xmm0
	cvttsd2si	%xmm0, %eax
	cltq
	imulq	$-2004318071, %rax, %rcx
	shrq	$32, %rcx
	addl	%eax, %ecx
	movl	%ecx, %edx
	shrl	$31, %edx
	sarl	$3, %ecx
	addl	%edx, %ecx
	leal	(%rcx,%rcx,4), %ecx
	leal	(%rcx,%rcx,2), %ecx
	subl	%ecx, %eax
	xorps	%xmm1, %xmm1
	cvtsi2sd	%eax, %xmm1
	movsd	.LCPI0_10(%rip), %xmm0
	subsd	%xmm1, %xmm0
	mulsd	.LCPI0_11(%rip), %xmm2
	movsd	.LCPI0_12(%rip), %xmm1
	movsd	.LCPI0_8(%rip), %xmm3
	callq	drawRing@PLT
	movl	$100, %edi
	callq	vg_wait@PLT
	movsd	(%rbx), %xmm0
	addsd	.LCPI0_13(%rip), %xmm0
	movsd	%xmm0, (%rbx)
	movsd	.LCPI0_14(%rip), %xmm1
	ucomisd	%xmm0, %xmm1
	ja	.LBB0_1
	xorl	%eax, %eax
	addq	$8, %rsp
	.cfi_def_cfa_offset 24
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%r14
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc

	.section	.rodata.cst8,"aM",@progbits,8
	.p2align	3
.LCPI1_0:
	.quad	0x4076800000000000
.LCPI1_1:
	.quad	0x400921ff2e48e8a7
.LCPI1_2:
	.quad	0x4066800000000000
.LCPI1_3:
	.quad	0x3fe0000000000000
.LCPI1_4:
	.quad	0x3ff0000000000000
	.text
	.globl	drawRing
	.p2align	4, 0x90
	.type	drawRing,@function
drawRing:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%r15
	.cfi_def_cfa_offset 24
	pushq	%r14
	.cfi_def_cfa_offset 32
	pushq	%r13
	.cfi_def_cfa_offset 40
	pushq	%r12
	.cfi_def_cfa_offset 48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	subq	$40, %rsp
	.cfi_def_cfa_offset 96
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movsd	%xmm3, 32(%rsp)
	movsd	%xmm2, 24(%rsp)
	movsd	%xmm0, 8(%rsp)
	movq	seg@GOTPCREL(%rip), %rbx
	movq	$0, (%rbx)
	xorpd	%xmm0, %xmm0
	ucomisd	%xmm0, %xmm1
	jbe	.LBB1_5
	movq	ang@GOTPCREL(%rip), %r14
	movq	x@GOTPCREL(%rip), %r12
	movq	cy@GOTPCREL(%rip), %r13
	movq	y@GOTPCREL(%rip), %rbp
	movq	col@GOTPCREL(%rip), %r15
	movsd	%xmm1, 16(%rsp)
	jmp	.LBB1_2
	.p2align	4, 0x90
.LBB1_4:
	movl	%edi, (%r15)
	callq	vg_set_color@PLT
	movsd	(%r12), %xmm0
	movsd	.LCPI1_3(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%rbp), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	movl	$5, %edx
	callq	vg_draw_circle@PLT
	movsd	(%rbx), %xmm0
	addsd	.LCPI1_4(%rip), %xmm0
	movsd	%xmm0, (%rbx)
	movsd	16(%rsp), %xmm1
	ucomisd	%xmm0, %xmm1
	jbe	.LBB1_5
.LBB1_2:
	mulsd	32(%rsp), %xmm0
	mulsd	.LCPI1_0(%rip), %xmm0
	divsd	%xmm1, %xmm0
	addsd	24(%rsp), %xmm0
	movsd	%xmm0, (%r14)
	movq	cx@GOTPCREL(%rip), %rax
	movsd	(%rax), %xmm1
	movsd	%xmm1, (%rsp)
	movsd	.LCPI1_1(%rip), %xmm2
	mulsd	%xmm2, %xmm0
	movsd	.LCPI1_2(%rip), %xmm2
	divsd	%xmm2, %xmm0
	callq	cos@PLT
	mulsd	8(%rsp), %xmm0
	addsd	(%rsp), %xmm0
	movsd	%xmm0, (%r12)
	movsd	(%r13), %xmm0
	movsd	%xmm0, (%rsp)
	movsd	(%r14), %xmm0
	mulsd	.LCPI1_1(%rip), %xmm0
	divsd	.LCPI1_2(%rip), %xmm0
	callq	sin@PLT
	mulsd	8(%rsp), %xmm0
	addsd	(%rsp), %xmm0
	movsd	%xmm0, (%rbp)
	movsd	(%rbx), %xmm0
	addsd	.LCPI1_3(%rip), %xmm0
	cvttsd2si	%xmm0, %eax
	cltq
	imulq	$715827883, %rax, %rcx
	movq	%rcx, %rdx
	shrq	$63, %rdx
	shrq	$32, %rcx
	addl	%edx, %ecx
	addl	%ecx, %ecx
	leal	(%rcx,%rcx,2), %ecx
	subl	%ecx, %eax
	movl	$16711935, %edi
	cmpl	$5, %eax
	jae	.LBB1_4
	cltq
	movl	.Lswitch.table.drawRing(,%rax,4), %edi
	jmp	.LBB1_4
.LBB1_5:
	addq	$40, %rsp
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%r12
	.cfi_def_cfa_offset 40
	popq	%r13
	.cfi_def_cfa_offset 32
	popq	%r14
	.cfi_def_cfa_offset 24
	popq	%r15
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	drawRing, .Lfunc_end1-drawRing
	.cfi_endproc

	.section	.rodata.cst8,"aM",@progbits,8
	.p2align	3
.LCPI2_0:
	.quad	0x4076800000000000
.LCPI2_1:
	.quad	0x400921ff2e48e8a7
.LCPI2_2:
	.quad	0x4066800000000000
.LCPI2_3:
	.quad	0x3fe0000000000000
.LCPI2_4:
	.quad	0x3ff0000000000000
	.text
	.globl	aperture
	.p2align	4, 0x90
	.type	aperture,@function
aperture:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%r15
	.cfi_def_cfa_offset 24
	pushq	%r14
	.cfi_def_cfa_offset 32
	pushq	%r13
	.cfi_def_cfa_offset 40
	pushq	%r12
	.cfi_def_cfa_offset 48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	subq	$40, %rsp
	.cfi_def_cfa_offset 96
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movsd	%xmm3, 24(%rsp)
	movsd	%xmm2, 16(%rsp)
	movsd	%xmm0, 8(%rsp)
	movq	ray@GOTPCREL(%rip), %rbp
	movq	$0, (%rbp)
	xorpd	%xmm0, %xmm0
	ucomisd	%xmm0, %xmm1
	jbe	.LBB2_3
	movsd	8(%rsp), %xmm2
	addsd	%xmm2, %xmm2
	movsd	%xmm2, 8(%rsp)
	movsd	%xmm1, 32(%rsp)
	.p2align	4, 0x90
.LBB2_2:
	mulsd	.LCPI2_0(%rip), %xmm0
	divsd	%xmm1, %xmm0
	addsd	8(%rsp), %xmm0
	movq	ang@GOTPCREL(%rip), %rax
	movsd	%xmm0, (%rax)
	movq	%rax, %rbx
	movq	cx@GOTPCREL(%rip), %r14
	movsd	(%r14), %xmm1
	movsd	%xmm1, (%rsp)
	movsd	.LCPI2_1(%rip), %xmm1
	mulsd	%xmm1, %xmm0
	movsd	.LCPI2_2(%rip), %xmm1
	divsd	%xmm1, %xmm0
	callq	cos@PLT
	mulsd	16(%rsp), %xmm0
	addsd	(%rsp), %xmm0
	movq	x@GOTPCREL(%rip), %r12
	movsd	%xmm0, (%r12)
	movq	cy@GOTPCREL(%rip), %r15
	movsd	(%r15), %xmm0
	movsd	%xmm0, (%rsp)
	movq	%rbx, %r12
	movsd	(%rbx), %xmm0
	mulsd	.LCPI2_1(%rip), %xmm0
	divsd	.LCPI2_2(%rip), %xmm0
	callq	sin@PLT
	mulsd	16(%rsp), %xmm0
	addsd	(%rsp), %xmm0
	movq	y@GOTPCREL(%rip), %r13
	movsd	%xmm0, (%r13)
	movsd	(%r14), %xmm0
	movsd	%xmm0, (%rsp)
	movsd	(%rbx), %xmm0
	mulsd	.LCPI2_1(%rip), %xmm0
	divsd	.LCPI2_2(%rip), %xmm0
	callq	cos@PLT
	mulsd	24(%rsp), %xmm0
	addsd	(%rsp), %xmm0
	movq	x2@GOTPCREL(%rip), %r14
	movsd	%xmm0, (%r14)
	movsd	(%r15), %xmm0
	movsd	%xmm0, (%rsp)
	movsd	(%rbx), %xmm0
	mulsd	.LCPI2_1(%rip), %xmm0
	divsd	.LCPI2_2(%rip), %xmm0
	callq	sin@PLT
	mulsd	24(%rsp), %xmm0
	addsd	(%rsp), %xmm0
	movq	y2@GOTPCREL(%rip), %r15
	movsd	%xmm0, (%r15)
	movsd	(%rbp), %xmm0
	movsd	.LCPI2_3(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %eax
	testb	$1, %al
	movl	$65535, %edi
	movl	$16777215, %eax
	cmovel	%eax, %edi
	movq	col@GOTPCREL(%rip), %rax
	movl	%edi, (%rax)
	callq	vg_set_color@PLT
	movq	x@GOTPCREL(%rip), %rbx
	movsd	(%rbx), %xmm0
	movsd	.LCPI2_3(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%r13), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	movsd	(%r14), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edx
	movsd	(%r15), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %ecx
	callq	vg_draw_line@PLT
	movsd	(%rbx), %xmm0
	movsd	.LCPI2_4(%rip), %xmm1
	addsd	%xmm1, %xmm0
	movapd	%xmm1, %xmm2
	movsd	.LCPI2_3(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%r13), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	movsd	(%r14), %xmm0
	addsd	%xmm2, %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edx
	movsd	(%r15), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %ecx
	callq	vg_draw_line@PLT
	movsd	32(%rsp), %xmm1
	movsd	(%rbp), %xmm0
	addsd	.LCPI2_4(%rip), %xmm0
	movsd	%xmm0, (%rbp)
	ucomisd	%xmm0, %xmm1
	ja	.LBB2_2
.LBB2_3:
	addq	$40, %rsp
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%r12
	.cfi_def_cfa_offset 40
	popq	%r13
	.cfi_def_cfa_offset 32
	popq	%r14
	.cfi_def_cfa_offset 24
	popq	%r15
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end2:
	.size	aperture, .Lfunc_end2-aperture
	.cfi_endproc

	.globl	_main
	.p2align	4, 0x90
	.type	_main,@function
_main:
	.cfi_startproc
	pushq	%rax
	.cfi_def_cfa_offset 16
	callq	main@PLT
	xorl	%eax, %eax
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end3:
	.size	_main, .Lfunc_end3-_main
	.cfi_endproc

	.type	cx,@object
	.bss
	.globl	cx
	.p2align	3
cx:
	.quad	0x0000000000000000
	.size	cx, 8

	.type	cy,@object
	.globl	cy
	.p2align	3
cy:
	.quad	0x0000000000000000
	.size	cy, 8

	.type	t,@object
	.globl	t
	.p2align	3
t:
	.quad	0x0000000000000000
	.size	t, 8

	.type	seg,@object
	.globl	seg
	.p2align	3
seg:
	.quad	0x0000000000000000
	.size	seg, 8

	.type	ang,@object
	.globl	ang
	.p2align	3
ang:
	.quad	0x0000000000000000
	.size	ang, 8

	.type	x,@object
	.globl	x
	.p2align	3
x:
	.quad	0x0000000000000000
	.size	x, 8

	.type	y,@object
	.globl	y
	.p2align	3
y:
	.quad	0x0000000000000000
	.size	y, 8

	.type	ray,@object
	.globl	ray
	.p2align	3
ray:
	.quad	0x0000000000000000
	.size	ray, 8

	.type	x2,@object
	.globl	x2
	.p2align	3
x2:
	.quad	0x0000000000000000
	.size	x2, 8

	.type	y2,@object
	.globl	y2
	.p2align	3
y2:
	.quad	0x0000000000000000
	.size	y2, 8

	.type	blades,@object
	.globl	blades
	.p2align	3
blades:
	.quad	0x0000000000000000
	.size	blades, 8

	.type	col,@object
	.data
	.globl	col
	.p2align	2
col:
	.long	16777215
	.size	col, 4

	.type	.Lswitch.table.drawRing,@object
	.section	.rodata,"a",@progbits
	.p2align	2
.Lswitch.table.drawRing:
	.long	16711680
	.long	16776960
	.long	65280
	.long	65535
	.long	255
	.size	.Lswitch.table.drawRing, 20

	.section	".note.GNU-stack","",@progbits