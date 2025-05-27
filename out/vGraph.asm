# VGraph Assembly Code
# Generated from LLVM IR
# Target: x86-64 (linux)
# Syntax: AT&T (GNU Assembler)

	.text
	.file	"<string>"
	.section	.rodata.cst8,"aM",@progbits,8
	.p2align	3
.LCPI0_0:
	.quad	0x4034000000000000
.LCPI0_1:
	.quad	0x3fe0000000000000
.LCPI0_2:
	.quad	0x4028000000000000
.LCPI0_3:
	.quad	0x4018000000000000
.LCPI0_4:
	.quad	0x404e000000000000
.LCPI0_5:
	.quad	0x400921ff2e48e8a7
.LCPI0_6:
	.quad	0x4066800000000000
.LCPI0_7:
	.quad	0x4038000000000000
.LCPI0_8:
	.quad	0x4000000000000000
.LCPI0_9:
	.quad	0xc000000000000000
.LCPI0_10:
	.quad	0x4070400000000000
.LCPI0_11:
	.quad	0x3ff0000000000000
.LCPI0_12:
	.quad	0x402a000000000000
.LCPI0_13:
	.quad	0x4058400000000000
.LCPI0_14:
	.quad	0x403d000000000000
.LCPI0_15:
	.quad	0x404a800000000000
.LCPI0_16:
	.quad	0x401c000000000000
.LCPI0_17:
	.quad	0x4024000000000000
.LCPI0_18:
	.quad	0x4049000000000000
.LCPI0_19:
	.quad	0x405ec00000000000
.LCPI0_20:
	.quad	0x4010000000000000
.LCPI0_21:
	.quad	0x40e1940000000000
	.text
	.globl	main
	.p2align	4, 0x90
	.type	main,@function
main:
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
	subq	$24, %rsp
	.cfi_def_cfa_offset 80
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movq	cx@GOTPCREL(%rip), %rcx
	movabsq	$4645744490609377280, %rax
	movq	%rax, (%rcx)
	movq	cy@GOTPCREL(%rip), %rcx
	movabsq	$4643985272004935680, %rax
	movq	%rax, (%rcx)
	callq	vg_clear@PLT
	xorl	%edi, %edi
	callq	vg_set_color@PLT
	xorl	%edi, %edi
	xorl	%esi, %esi
	movl	$799, %edx
	movl	$599, %ecx
	callq	vg_draw_rect@PLT
	movq	t@GOTPCREL(%rip), %r13
	movq	$0, (%r13)
	xorpd	%xmm0, %xmm0
	movsd	.LCPI0_1(%rip), %xmm1
	movl	$16777215, %ecx
	movq	col@GOTPCREL(%rip), %rdx
	movq	rad@GOTPCREL(%rip), %r15
	movq	x@GOTPCREL(%rip), %rbp
	movq	y@GOTPCREL(%rip), %rbx
	jmp	.LBB0_1
	.p2align	4, 0x90
.LBB0_14:
	movl	$2, %edi
	callq	vg_wait@PLT
	movsd	(%r13), %xmm0
	addsd	.LCPI0_8(%rip), %xmm0
	movsd	%xmm0, (%r13)
	movsd	.LCPI0_21(%rip), %xmm1
	ucomisd	%xmm0, %xmm1
	movsd	.LCPI0_1(%rip), %xmm1
	movl	$16777215, %ecx
	movq	col@GOTPCREL(%rip), %rdx
	jbe	.LBB0_15
.LBB0_1:
	divsd	.LCPI0_0(%rip), %xmm0
	addsd	%xmm1, %xmm0
	movq	%r13, %r14
	cvttsd2si	%xmm0, %eax
	testb	$1, %al
	movl	$65535, %edi
	cmovel	%ecx, %edi
	movl	%edi, (%rdx)
	callq	vg_set_color@PLT
	movq	cx@GOTPCREL(%rip), %rax
	movsd	(%rax), %xmm0
	movsd	.LCPI0_1(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movq	cy@GOTPCREL(%rip), %rax
	movsd	(%rax), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	movsd	(%r13), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %eax
	cltq
	imulq	$1717986919, %rax, %rcx
	movq	%rcx, %rdx
	shrq	$63, %rdx
	sarq	$35, %rcx
	addl	%edx, %ecx
	shll	$2, %ecx
	leal	(%rcx,%rcx,4), %ecx
	subl	%ecx, %eax
	xorps	%xmm0, %xmm0
	cvtsi2sd	%eax, %xmm0
	mulsd	%xmm1, %xmm0
	addsd	.LCPI0_2(%rip), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edx
	callq	vg_draw_circle@PLT
	movq	arm@GOTPCREL(%rip), %rax
	movq	$0, (%rax)
	movsd	.LCPI0_3(%rip), %xmm1
	jmp	.LBB0_2
	.p2align	4, 0x90
.LBB0_6:
	movq	arm@GOTPCREL(%rip), %rax
	movsd	(%rax), %xmm0
	addsd	.LCPI0_11(%rip), %xmm0
	movsd	%xmm0, (%rax)
	ucomisd	%xmm0, %xmm1
	jbe	.LBB0_7
.LBB0_2:
	movabsq	$4618441417868443648, %rax
	movq	%rax, (%r15)
	movapd	%xmm1, %xmm2
	jmp	.LBB0_3
	.p2align	4, 0x90
.LBB0_5:
	movq	col@GOTPCREL(%rip), %rax
	movl	%edi, (%rax)
	callq	vg_set_color@PLT
	movsd	(%rbp), %xmm0
	movsd	.LCPI0_1(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%rbx), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	movl	$4, %edx
	callq	vg_draw_circle@PLT
	movl	$16777215, %edi
	callq	vg_set_color@PLT
	movsd	(%rbp), %xmm0
	movsd	.LCPI0_8(%rip), %xmm1
	addsd	%xmm1, %xmm0
	movsd	.LCPI0_1(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%rbx), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	callq	vg_draw_pixel@PLT
	movsd	(%rbp), %xmm0
	movsd	.LCPI0_9(%rip), %xmm1
	addsd	%xmm1, %xmm0
	movsd	.LCPI0_1(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%rbx), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	callq	vg_draw_pixel@PLT
	movsd	(%rbp), %xmm0
	movsd	.LCPI0_1(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%rbx), %xmm0
	addsd	.LCPI0_8(%rip), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	callq	vg_draw_pixel@PLT
	movsd	(%rbp), %xmm0
	movsd	.LCPI0_1(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%rbx), %xmm0
	addsd	.LCPI0_9(%rip), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	callq	vg_draw_pixel@PLT
	movsd	(%r15), %xmm2
	movsd	.LCPI0_3(%rip), %xmm1
	addsd	%xmm1, %xmm2
	movsd	%xmm2, (%r15)
	movsd	.LCPI0_10(%rip), %xmm0
	ucomisd	%xmm2, %xmm0
	jbe	.LBB0_6
.LBB0_3:
	movsd	%xmm2, 16(%rsp)
	movq	arm@GOTPCREL(%rip), %r12
	movsd	(%r12), %xmm0
	mulsd	.LCPI0_4(%rip), %xmm0
	addsd	(%r13), %xmm0
	addsd	%xmm2, %xmm0
	movq	ang@GOTPCREL(%rip), %r14
	movsd	%xmm0, (%r14)
	movq	cx@GOTPCREL(%rip), %rax
	movsd	(%rax), %xmm1
	movsd	%xmm1, 8(%rsp)
	movsd	.LCPI0_5(%rip), %xmm1
	mulsd	%xmm1, %xmm0
	movsd	.LCPI0_6(%rip), %xmm1
	divsd	%xmm1, %xmm0
	callq	cos@PLT
	mulsd	16(%rsp), %xmm0
	addsd	8(%rsp), %xmm0
	movsd	%xmm0, (%rbp)
	movq	cy@GOTPCREL(%rip), %rax
	movsd	(%rax), %xmm0
	movsd	%xmm0, 8(%rsp)
	movsd	(%r15), %xmm0
	movsd	%xmm0, 16(%rsp)
	movsd	(%r14), %xmm0
	mulsd	.LCPI0_5(%rip), %xmm0
	divsd	.LCPI0_6(%rip), %xmm0
	callq	sin@PLT
	mulsd	16(%rsp), %xmm0
	addsd	8(%rsp), %xmm0
	movsd	%xmm0, (%rbx)
	movsd	(%r15), %xmm0
	divsd	.LCPI0_7(%rip), %xmm0
	addsd	(%r12), %xmm0
	addsd	.LCPI0_1(%rip), %xmm0
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
	jae	.LBB0_5
	cltq
	movl	.Lswitch.table.main(,%rax,4), %edi
	jmp	.LBB0_5
	.p2align	4, 0x90
.LBB0_7:
	movq	star@GOTPCREL(%rip), %r14
	movq	$0, (%r14)
	xorpd	%xmm0, %xmm0
	movsd	.LCPI0_1(%rip), %xmm5
	movq	sx@GOTPCREL(%rip), %r12
	movq	sy@GOTPCREL(%rip), %r14
	.p2align	4, 0x90
.LBB0_8:
	movq	t@GOTPCREL(%rip), %rax
	movsd	(%rax), %xmm1
	movapd	%xmm0, %xmm2
	movapd	%xmm1, %xmm3
	movapd	%xmm0, %xmm4
	mulsd	.LCPI0_16(%rip), %xmm0
	addsd	%xmm1, %xmm0
	mulsd	.LCPI0_12(%rip), %xmm1
	mulsd	.LCPI0_13(%rip), %xmm2
	addsd	%xmm1, %xmm2
	addsd	%xmm5, %xmm2
	cvttsd2si	%xmm2, %eax
	cltq
	imulq	$1374389535, %rax, %rcx
	movq	%rcx, %rdx
	shrq	$63, %rdx
	sarq	$40, %rcx
	addl	%edx, %ecx
	imull	$800, %ecx, %ecx
	subl	%ecx, %eax
	xorps	%xmm1, %xmm1
	cvtsi2sd	%eax, %xmm1
	movsd	%xmm1, (%r12)
	mulsd	.LCPI0_14(%rip), %xmm3
	mulsd	.LCPI0_15(%rip), %xmm4
	addsd	%xmm3, %xmm4
	addsd	%xmm5, %xmm4
	cvttsd2si	%xmm4, %eax
	cltq
	imulq	$458129845, %rax, %rcx
	movq	%rcx, %rdx
	shrq	$63, %rdx
	sarq	$38, %rcx
	addl	%edx, %ecx
	imull	$600, %ecx, %ecx
	subl	%ecx, %eax
	xorps	%xmm1, %xmm1
	cvtsi2sd	%eax, %xmm1
	movsd	%xmm1, (%r14)
	divsd	.LCPI0_17(%rip), %xmm0
	addsd	%xmm5, %xmm0
	cvttsd2si	%xmm0, %eax
	testb	$1, %al
	movl	$65535, %edi
	movl	$16777215, %eax
	cmovel	%eax, %edi
	movq	col@GOTPCREL(%rip), %rax
	movl	%edi, (%rax)
	callq	vg_set_color@PLT
	movsd	(%r12), %xmm0
	addsd	.LCPI0_1(%rip), %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%r14), %xmm0
	addsd	.LCPI0_1(%rip), %xmm0
	cvttsd2si	%xmm0, %esi
	callq	vg_draw_pixel@PLT
	movsd	.LCPI0_1(%rip), %xmm5
	movq	star@GOTPCREL(%rip), %rax
	movsd	(%rax), %xmm0
	addsd	.LCPI0_11(%rip), %xmm0
	movsd	%xmm0, (%rax)
	movsd	.LCPI0_18(%rip), %xmm1
	ucomisd	%xmm0, %xmm1
	ja	.LBB0_8
	movq	t@GOTPCREL(%rip), %rax
	movsd	(%rax), %xmm0
	movapd	%xmm0, %xmm1
	addsd	%xmm5, %xmm1
	cvttsd2si	%xmm1, %eax
	imull	$-1527099483, %eax, %eax
	addl	$47721856, %eax
	rorl	$2, %eax
	cmpl	$23860928, %eax
	movq	sparkleT@GOTPCREL(%rip), %r14
	ja	.LBB0_14
	movq	cx@GOTPCREL(%rip), %rax
	movsd	(%rax), %xmm1
	movsd	%xmm1, 8(%rsp)
	movsd	.LCPI0_19(%rip), %xmm1
	addsd	%xmm1, %xmm0
	movsd	.LCPI0_5(%rip), %xmm1
	mulsd	%xmm1, %xmm0
	movsd	.LCPI0_6(%rip), %xmm1
	divsd	%xmm1, %xmm0
	callq	cos@PLT
	movsd	.LCPI0_10(%rip), %xmm1
	mulsd	%xmm1, %xmm0
	addsd	8(%rsp), %xmm0
	movsd	%xmm0, (%r12)
	movq	cy@GOTPCREL(%rip), %rax
	movsd	(%rax), %xmm0
	movsd	%xmm0, 8(%rsp)
	movsd	(%r13), %xmm0
	addsd	.LCPI0_19(%rip), %xmm0
	mulsd	.LCPI0_5(%rip), %xmm0
	divsd	.LCPI0_6(%rip), %xmm0
	callq	sin@PLT
	mulsd	.LCPI0_10(%rip), %xmm0
	addsd	8(%rsp), %xmm0
	movq	sy@GOTPCREL(%rip), %rax
	movsd	%xmm0, (%rax)
	movq	$0, (%r14)
	movsd	(%r12), %xmm1
	movsd	.LCPI0_1(%rip), %xmm2
	addsd	%xmm2, %xmm1
	cvttsd2si	%xmm1, %r12d
	addsd	%xmm2, %xmm0
	cvttsd2si	%xmm0, %eax
	movl	%eax, 8(%rsp)
	xorpd	%xmm0, %xmm0
	jmp	.LBB0_11
	.p2align	4, 0x90
.LBB0_13:
	movq	col@GOTPCREL(%rip), %rax
	movl	%edi, (%rax)
	callq	vg_set_color@PLT
	movsd	(%r14), %xmm0
	movsd	.LCPI0_1(%rip), %xmm2
	mulsd	%xmm2, %xmm0
	movsd	.LCPI0_20(%rip), %xmm1
	subsd	%xmm0, %xmm1
	addsd	%xmm2, %xmm1
	cvttsd2si	%xmm1, %edx
	movl	%r12d, %edi
	movl	8(%rsp), %esi
	callq	vg_draw_circle@PLT
	movsd	(%r14), %xmm0
	addsd	.LCPI0_11(%rip), %xmm0
	movsd	%xmm0, (%r14)
	movsd	.LCPI0_3(%rip), %xmm1
	ucomisd	%xmm0, %xmm1
	jbe	.LBB0_14
.LBB0_11:
	addsd	.LCPI0_1(%rip), %xmm0
	cvttsd2si	%xmm0, %eax
	testb	$1, %al
	movl	$16711935, %edi
	je	.LBB0_13
	movl	$16776960, %edi
	jmp	.LBB0_13
.LBB0_15:
	xorl	%eax, %eax
	addq	$24, %rsp
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
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc

	.section	.rodata.cst8,"aM",@progbits,8
	.p2align	3
.LCPI1_0:
	.quad	0x3fe0000000000000
.LCPI1_1:
	.quad	0x4010000000000000
.LCPI1_2:
	.quad	0x3ff0000000000000
.LCPI1_3:
	.quad	0x4018000000000000
	.text
	.globl	sparkle
	.p2align	4, 0x90
	.type	sparkle,@function
sparkle:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%r15
	.cfi_def_cfa_offset 24
	pushq	%r14
	.cfi_def_cfa_offset 32
	pushq	%rbx
	.cfi_def_cfa_offset 40
	pushq	%rax
	.cfi_def_cfa_offset 48
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movq	sparkleT@GOTPCREL(%rip), %rbx
	movq	$0, (%rbx)
	movsd	.LCPI1_0(%rip), %xmm2
	addsd	%xmm2, %xmm0
	cvttsd2si	%xmm0, %r14d
	addsd	%xmm2, %xmm1
	cvttsd2si	%xmm1, %ebp
	xorpd	%xmm0, %xmm0
	movq	col@GOTPCREL(%rip), %r15
	jmp	.LBB1_1
	.p2align	4, 0x90
.LBB1_3:
	movl	%edi, (%r15)
	callq	vg_set_color@PLT
	movsd	(%rbx), %xmm0
	movsd	.LCPI1_0(%rip), %xmm2
	mulsd	%xmm2, %xmm0
	movsd	.LCPI1_1(%rip), %xmm1
	subsd	%xmm0, %xmm1
	addsd	%xmm2, %xmm1
	cvttsd2si	%xmm1, %edx
	movl	%r14d, %edi
	movl	%ebp, %esi
	callq	vg_draw_circle@PLT
	movsd	(%rbx), %xmm0
	addsd	.LCPI1_2(%rip), %xmm0
	movsd	%xmm0, (%rbx)
	movsd	.LCPI1_3(%rip), %xmm1
	ucomisd	%xmm0, %xmm1
	movsd	.LCPI1_0(%rip), %xmm2
	jbe	.LBB1_4
.LBB1_1:
	addsd	%xmm2, %xmm0
	cvttsd2si	%xmm0, %eax
	testb	$1, %al
	movl	$16711935, %edi
	je	.LBB1_3
	movl	$16776960, %edi
	jmp	.LBB1_3
.LBB1_4:
	addq	$8, %rsp
	.cfi_def_cfa_offset 40
	popq	%rbx
	.cfi_def_cfa_offset 32
	popq	%r14
	.cfi_def_cfa_offset 24
	popq	%r15
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	sparkle, .Lfunc_end1-sparkle
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
.Lfunc_end2:
	.size	_main, .Lfunc_end2-_main
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

	.type	arm,@object
	.globl	arm
	.p2align	3
arm:
	.quad	0x0000000000000000
	.size	arm, 8

	.type	ang,@object
	.globl	ang
	.p2align	3
ang:
	.quad	0x0000000000000000
	.size	ang, 8

	.type	rad,@object
	.globl	rad
	.p2align	3
rad:
	.quad	0x0000000000000000
	.size	rad, 8

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

	.type	star,@object
	.globl	star
	.p2align	3
star:
	.quad	0x0000000000000000
	.size	star, 8

	.type	sx,@object
	.globl	sx
	.p2align	3
sx:
	.quad	0x0000000000000000
	.size	sx, 8

	.type	sy,@object
	.globl	sy
	.p2align	3
sy:
	.quad	0x0000000000000000
	.size	sy, 8

	.type	sparkleT,@object
	.globl	sparkleT
	.p2align	3
sparkleT:
	.quad	0x0000000000000000
	.size	sparkleT, 8

	.type	col,@object
	.data
	.globl	col
	.p2align	2
col:
	.long	16777215
	.size	col, 4

	.type	.Lswitch.table.main,@object
	.section	.rodata,"a",@progbits
	.p2align	2
.Lswitch.table.main:
	.long	16711680
	.long	16776960
	.long	65280
	.long	65535
	.long	255
	.size	.Lswitch.table.main, 20

	.section	".note.GNU-stack","",@progbits