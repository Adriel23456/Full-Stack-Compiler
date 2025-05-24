# VGraph Assembly Code
# Generated from LLVM IR
# Target: x86-64
# Syntax: AT&T (GNU Assembler)

	.text
	.file	"<string>"
	.section	.rodata.cst8,"aM",@progbits,8
	.p2align	3
.LCPI0_0:
	.quad	0x3fe0000000000000
.LCPI0_1:
	.quad	0x3ff0000000000000
.LCPI0_2:
	.quad	0x4034000000000000
.LCPI0_3:
	.quad	0x4000000000000000
	.text
	.globl	main
	.p2align	4, 0x90
	.type	main,@function
main:
	.cfi_startproc
	pushq	%r15
	.cfi_def_cfa_offset 16
	pushq	%r14
	.cfi_def_cfa_offset 24
	pushq	%rbx
	.cfi_def_cfa_offset 32
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	.cfi_offset %r15, -16
	movq	c@GOTPCREL(%rip), %rbx
	movl	$16711680, (%rbx)
	movq	x1@GOTPCREL(%rip), %r15
	movabsq	$4607182418800017408, %rax
	movq	%rax, (%r15)
	movq	y1@GOTPCREL(%rip), %r14
	movq	%rax, (%r14)
	movq	x2@GOTPCREL(%rip), %rax
	movabsq	$4621819117588971520, %rcx
	movq	%rcx, (%rax)
	movq	y2@GOTPCREL(%rip), %rax
	movabsq	$4627730092099895296, %rcx
	movq	%rcx, (%rax)
	callq	vg_clear@PLT
	movl	(%rbx), %edi
	callq	vg_set_color@PLT
	movsd	.LCPI0_0(%rip), %xmm1
	movsd	(%r15), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%r14), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	callq	vg_draw_pixel@PLT
	movsd	(%r15), %xmm0
	addsd	.LCPI0_1(%rip), %xmm0
	movsd	.LCPI0_2(%rip), %xmm1
	mulsd	%xmm1, %xmm0
	movsd	.LCPI0_0(%rip), %xmm2
	addsd	%xmm2, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%r14), %xmm0
	addsd	.LCPI0_3(%rip), %xmm0
	mulsd	%xmm1, %xmm0
	addsd	%xmm2, %xmm0
	cvttsd2si	%xmm0, %esi
	callq	vg_draw_pixel@PLT
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
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
	.quad	0x3ff0000000000000
.LCPI1_2:
	.quad	0x4034000000000000
.LCPI1_3:
	.quad	0x4000000000000000
	.text
	.globl	_main
	.p2align	4, 0x90
	.type	_main,@function
_main:
	.cfi_startproc
	pushq	%r15
	.cfi_def_cfa_offset 16
	pushq	%r14
	.cfi_def_cfa_offset 24
	pushq	%rbx
	.cfi_def_cfa_offset 32
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	.cfi_offset %r15, -16
	movq	c@GOTPCREL(%rip), %rbx
	movl	$16711680, (%rbx)
	movq	x1@GOTPCREL(%rip), %r15
	movabsq	$4607182418800017408, %rax
	movq	%rax, (%r15)
	movq	y1@GOTPCREL(%rip), %r14
	movq	%rax, (%r14)
	movq	x2@GOTPCREL(%rip), %rax
	movabsq	$4621819117588971520, %rcx
	movq	%rcx, (%rax)
	movq	y2@GOTPCREL(%rip), %rax
	movabsq	$4627730092099895296, %rcx
	movq	%rcx, (%rax)
	callq	vg_clear@PLT
	movl	(%rbx), %edi
	callq	vg_set_color@PLT
	movsd	.LCPI1_0(%rip), %xmm1
	movsd	(%r15), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%r14), %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %esi
	callq	vg_draw_pixel@PLT
	movsd	(%r15), %xmm0
	addsd	.LCPI1_1(%rip), %xmm0
	movsd	.LCPI1_2(%rip), %xmm1
	mulsd	%xmm1, %xmm0
	movsd	.LCPI1_0(%rip), %xmm2
	addsd	%xmm2, %xmm0
	cvttsd2si	%xmm0, %edi
	movsd	(%r14), %xmm0
	addsd	.LCPI1_3(%rip), %xmm0
	mulsd	%xmm1, %xmm0
	addsd	%xmm2, %xmm0
	cvttsd2si	%xmm0, %esi
	callq	vg_draw_pixel@PLT
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	_main, .Lfunc_end1-_main
	.cfi_endproc

	.type	x1,@object
	.bss
	.globl	x1
	.p2align	3
x1:
	.quad	0x0000000000000000
	.size	x1, 8

	.type	y1,@object
	.globl	y1
	.p2align	3
y1:
	.quad	0x0000000000000000
	.size	y1, 8

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

	.type	a1,@object
	.globl	a1
a1:
	.byte	0
	.size	a1, 1

	.type	b1,@object
	.globl	b1
b1:
	.byte	0
	.size	b1, 1

	.type	c1,@object
	.globl	c1
c1:
	.byte	0
	.size	c1, 1

	.type	c,@object
	.data
	.globl	c
	.p2align	2
c:
	.long	16777215
	.size	c, 4

	.section	".note.GNU-stack","",@progbits