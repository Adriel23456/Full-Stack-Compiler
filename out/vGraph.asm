# VGraph Assembly Code
# Generated from LLVM IR
# Target: x86-64
# Syntax: AT&T (GNU Assembler)

	.text
	.file	"<string>"
	.section	.rodata.cst8,"aM",@progbits,8
	.p2align	3
.LCPI0_0:
	.quad	0x400921ff2e48e8a7
.LCPI0_1:
	.quad	0x4066800000000000
.LCPI0_2:
	.quad	0x4074000000000000
.LCPI0_3:
	.quad	0x3fe0000000000000
.LCPI0_4:
	.quad	0x406e000000000000
.LCPI0_5:
	.quad	0x3ff0000000000000
.LCPI0_6:
	.quad	0xbff0000000000000
.LCPI0_7:
	.quad	0x4014000000000000
.LCPI0_8:
	.quad	0x4076800000000000
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
	pushq	%rax
	.cfi_def_cfa_offset 64
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	callq	vg_clear@PLT
	movq	t@GOTPCREL(%rip), %r14
	movq	$0, (%r14)
	xorpd	%xmm1, %xmm1
	movq	x@GOTPCREL(%rip), %rbx
	movl	$255, %r15d
	movq	y@GOTPCREL(%rip), %rbp
	movl	$16711680, %r12d
	movq	c@GOTPCREL(%rip), %r13
	.p2align	4, 0x90
.LBB0_1:
	movsd	%xmm1, (%rsp)
	movapd	%xmm1, %xmm0
	movsd	.LCPI0_0(%rip), %xmm1
	mulsd	%xmm1, %xmm0
	movsd	.LCPI0_1(%rip), %xmm1
	divsd	%xmm1, %xmm0
	callq	cos@PLT
	mulsd	(%rsp), %xmm0
	addsd	.LCPI0_2(%rip), %xmm0
	movsd	%xmm0, (%rbx)
	movsd	(%r14), %xmm0
	movsd	%xmm0, (%rsp)
	mulsd	.LCPI0_0(%rip), %xmm0
	divsd	.LCPI0_1(%rip), %xmm0
	callq	sin@PLT
	movsd	(%r14), %xmm1
	movsd	.LCPI0_3(%rip), %xmm2
	addsd	%xmm2, %xmm1
	cvttsd2si	%xmm1, %eax
	cltq
	imulq	$1431655766, %rax, %rcx
	movq	%rcx, %rdx
	shrq	$63, %rdx
	shrq	$32, %rcx
	addl	%edx, %ecx
	leal	(%rcx,%rcx,2), %ecx
	movl	%eax, %edx
	subl	%ecx, %edx
	cmpl	$1, %edx
	movl	$65280, %edi
	cmovel	%r15d, %edi
	cmpl	%ecx, %eax
	mulsd	(%rsp), %xmm0
	addsd	.LCPI0_4(%rip), %xmm0
	movsd	%xmm0, (%rbp)
	cmovel	%r12d, %edi
	movl	%edi, (%r13)
	callq	vg_set_color@PLT
	movsd	(%rbx), %xmm0
	movsd	.LCPI0_3(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%rbp), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	callq	vg_draw_pixel@PLT
	movsd	(%rbx), %xmm0
	movsd	.LCPI0_5(%rip), %xmm1
	addsd	%xmm1, %xmm0
	movsd	.LCPI0_3(%rip), %xmm2
	addsd	%xmm2, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%rbp), %xmm0
	addsd	%xmm1, %xmm0
	addsd	%xmm2, %xmm0
	cvttsd2si	%xmm0, %esi
	callq	vg_draw_pixel@PLT
	movsd	(%rbx), %xmm0
	addsd	.LCPI0_5(%rip), %xmm0
	movsd	.LCPI0_3(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%rbp), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	callq	vg_draw_pixel@PLT
	movsd	(%rbx), %xmm0
	movsd	.LCPI0_3(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%rbp), %xmm0
	addsd	.LCPI0_5(%rip), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	callq	vg_draw_pixel@PLT
	movsd	(%rbx), %xmm0
	movsd	.LCPI0_6(%rip), %xmm2
	addsd	%xmm2, %xmm0
	movsd	.LCPI0_3(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%rbp), %xmm0
	addsd	%xmm2, %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	callq	vg_draw_pixel@PLT
	movsd	(%rbx), %xmm0
	addsd	.LCPI0_6(%rip), %xmm0
	movsd	.LCPI0_3(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%rbp), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	callq	vg_draw_pixel@PLT
	movsd	(%rbx), %xmm0
	movsd	.LCPI0_3(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%rbp), %xmm0
	addsd	.LCPI0_6(%rip), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	callq	vg_draw_pixel@PLT
	movl	$100, %edi
	callq	vg_wait@PLT
	movsd	(%r14), %xmm1
	addsd	.LCPI0_7(%rip), %xmm1
	movsd	%xmm1, (%r14)
	movsd	.LCPI0_8(%rip), %xmm0
	ucomisd	%xmm1, %xmm0
	ja	.LBB0_1
	xorl	%eax, %eax
	addq	$8, %rsp
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
.Lfunc_end1:
	.size	_main, .Lfunc_end1-_main
	.cfi_endproc

	.type	x,@object
	.bss
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

	.type	t,@object
	.globl	t
	.p2align	3
t:
	.quad	0x0000000000000000
	.size	t, 8

	.type	c,@object
	.data
	.globl	c
	.p2align	2
c:
	.long	16777215
	.size	c, 4

	.section	".note.GNU-stack","",@progbits