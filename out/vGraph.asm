# VGraph Assembly Code
# Generated from LLVM IR
# Target: x86-64 (windows)
# Syntax: AT&T (GNU Assembler)

	.text
	.def	@feat.00;
	.scl	3;
	.type	0;
	.endef
	.globl	@feat.00
.set @feat.00, 0
	.file	"<string>"
	.def	main;
	.scl	2;
	.type	32;
	.endef
	.globl	__real@4034000000000000
	.section	.rdata,"dr",discard,__real@4034000000000000
	.p2align	3
__real@4034000000000000:
	.quad	0x4034000000000000
	.globl	__real@3fe0000000000000
	.section	.rdata,"dr",discard,__real@3fe0000000000000
	.p2align	3
__real@3fe0000000000000:
	.quad	0x3fe0000000000000
	.globl	__real@4028000000000000
	.section	.rdata,"dr",discard,__real@4028000000000000
	.p2align	3
__real@4028000000000000:
	.quad	0x4028000000000000
	.globl	__real@4018000000000000
	.section	.rdata,"dr",discard,__real@4018000000000000
	.p2align	3
__real@4018000000000000:
	.quad	0x4018000000000000
	.globl	__real@404e000000000000
	.section	.rdata,"dr",discard,__real@404e000000000000
	.p2align	3
__real@404e000000000000:
	.quad	0x404e000000000000
	.globl	__real@400921ff2e48e8a7
	.section	.rdata,"dr",discard,__real@400921ff2e48e8a7
	.p2align	3
__real@400921ff2e48e8a7:
	.quad	0x400921ff2e48e8a7
	.globl	__real@4066800000000000
	.section	.rdata,"dr",discard,__real@4066800000000000
	.p2align	3
__real@4066800000000000:
	.quad	0x4066800000000000
	.globl	__real@4038000000000000
	.section	.rdata,"dr",discard,__real@4038000000000000
	.p2align	3
__real@4038000000000000:
	.quad	0x4038000000000000
	.globl	__real@4000000000000000
	.section	.rdata,"dr",discard,__real@4000000000000000
	.p2align	3
__real@4000000000000000:
	.quad	0x4000000000000000
	.globl	__real@c000000000000000
	.section	.rdata,"dr",discard,__real@c000000000000000
	.p2align	3
__real@c000000000000000:
	.quad	0xc000000000000000
	.globl	__real@4070400000000000
	.section	.rdata,"dr",discard,__real@4070400000000000
	.p2align	3
__real@4070400000000000:
	.quad	0x4070400000000000
	.globl	__real@3ff0000000000000
	.section	.rdata,"dr",discard,__real@3ff0000000000000
	.p2align	3
__real@3ff0000000000000:
	.quad	0x3ff0000000000000
	.globl	__real@402a000000000000
	.section	.rdata,"dr",discard,__real@402a000000000000
	.p2align	3
__real@402a000000000000:
	.quad	0x402a000000000000
	.globl	__real@4058400000000000
	.section	.rdata,"dr",discard,__real@4058400000000000
	.p2align	3
__real@4058400000000000:
	.quad	0x4058400000000000
	.globl	__real@403d000000000000
	.section	.rdata,"dr",discard,__real@403d000000000000
	.p2align	3
__real@403d000000000000:
	.quad	0x403d000000000000
	.globl	__real@404a800000000000
	.section	.rdata,"dr",discard,__real@404a800000000000
	.p2align	3
__real@404a800000000000:
	.quad	0x404a800000000000
	.globl	__real@401c000000000000
	.section	.rdata,"dr",discard,__real@401c000000000000
	.p2align	3
__real@401c000000000000:
	.quad	0x401c000000000000
	.globl	__real@4024000000000000
	.section	.rdata,"dr",discard,__real@4024000000000000
	.p2align	3
__real@4024000000000000:
	.quad	0x4024000000000000
	.globl	__real@4049000000000000
	.section	.rdata,"dr",discard,__real@4049000000000000
	.p2align	3
__real@4049000000000000:
	.quad	0x4049000000000000
	.globl	__real@405ec00000000000
	.section	.rdata,"dr",discard,__real@405ec00000000000
	.p2align	3
__real@405ec00000000000:
	.quad	0x405ec00000000000
	.globl	__real@4010000000000000
	.section	.rdata,"dr",discard,__real@4010000000000000
	.p2align	3
__real@4010000000000000:
	.quad	0x4010000000000000
	.globl	__real@40e1940000000000
	.section	.rdata,"dr",discard,__real@40e1940000000000
	.p2align	3
__real@40e1940000000000:
	.quad	0x40e1940000000000
	.text
	.globl	main
	.p2align	4, 0x90
main:
.seh_proc main
	pushq	%r14
	.seh_pushreg %r14
	pushq	%rsi
	.seh_pushreg %rsi
	pushq	%rdi
	.seh_pushreg %rdi
	pushq	%rbp
	.seh_pushreg %rbp
	pushq	%rbx
	.seh_pushreg %rbx
	subq	$192, %rsp
	.seh_stackalloc 192
	movaps	%xmm15, 176(%rsp)
	.seh_savexmm %xmm15, 176
	movaps	%xmm14, 160(%rsp)
	.seh_savexmm %xmm14, 160
	movaps	%xmm13, 144(%rsp)
	.seh_savexmm %xmm13, 144
	movaps	%xmm12, 128(%rsp)
	.seh_savexmm %xmm12, 128
	movapd	%xmm11, 112(%rsp)
	.seh_savexmm %xmm11, 112
	movapd	%xmm10, 96(%rsp)
	.seh_savexmm %xmm10, 96
	movaps	%xmm9, 80(%rsp)
	.seh_savexmm %xmm9, 80
	movaps	%xmm8, 64(%rsp)
	.seh_savexmm %xmm8, 64
	movapd	%xmm7, 48(%rsp)
	.seh_savexmm %xmm7, 48
	movapd	%xmm6, 32(%rsp)
	.seh_savexmm %xmm6, 32
	.seh_endprologue
	movabsq	$4645744490609377280, %rax
	movq	%rax, cx(%rip)
	movabsq	$4643985272004935680, %rax
	movq	%rax, cy(%rip)
	callq	vg_clear
	xorl	%ecx, %ecx
	callq	vg_set_color
	xorl	%ecx, %ecx
	xorl	%edx, %edx
	movl	$799, %r8d
	movl	$599, %r9d
	callq	vg_draw_rect
	movq	$0, t(%rip)
	xorpd	%xmm0, %xmm0
	movsd	__real@3fe0000000000000(%rip), %xmm8
	movl	$16777215, %ebp
	movabsq	$4618441417868443648, %r14
	movsd	__real@4018000000000000(%rip), %xmm9
	movsd	__real@400921ff2e48e8a7(%rip), %xmm12
	movsd	__real@4066800000000000(%rip), %xmm14
	leaq	.Lswitch.table.main(%rip), %rbx
	movsd	__real@4000000000000000(%rip), %xmm15
	movsd	__real@c000000000000000(%rip), %xmm13
	jmp	.LBB0_1
	.p2align	4, 0x90
.LBB0_14:
	movl	$2, %ecx
	callq	vg_wait
	movsd	t(%rip), %xmm0
	addsd	%xmm15, %xmm0
	movsd	%xmm0, t(%rip)
	movsd	__real@40e1940000000000(%rip), %xmm1
	ucomisd	%xmm0, %xmm1
	jbe	.LBB0_15
.LBB0_1:
	divsd	__real@4034000000000000(%rip), %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %eax
	testb	$1, %al
	movl	$65535, %ecx
	cmovel	%ebp, %ecx
	movl	%ecx, col(%rip)
	callq	vg_set_color
	movsd	cx(%rip), %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %ecx
	movsd	cy(%rip), %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %edx
	movsd	t(%rip), %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %eax
	cltq
	imulq	$1717986919, %rax, %rdi
	movq	%rdi, %rsi
	shrq	$63, %rsi
	sarq	$35, %rdi
	addl	%esi, %edi
	shll	$2, %edi
	leal	(%rdi,%rdi,4), %edi
	subl	%edi, %eax
	xorps	%xmm0, %xmm0
	cvtsi2sd	%eax, %xmm0
	mulsd	%xmm8, %xmm0
	addsd	__real@4028000000000000(%rip), %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %r8d
	callq	vg_draw_circle
	movq	$0, arm(%rip)
	jmp	.LBB0_2
	.p2align	4, 0x90
.LBB0_6:
	movsd	arm(%rip), %xmm0
	movsd	__real@3ff0000000000000(%rip), %xmm7
	addsd	%xmm7, %xmm0
	movsd	%xmm0, arm(%rip)
	ucomisd	%xmm0, %xmm9
	jbe	.LBB0_7
.LBB0_2:
	movq	%r14, rad(%rip)
	movapd	%xmm9, %xmm11
	jmp	.LBB0_3
	.p2align	4, 0x90
.LBB0_5:
	movl	%ecx, col(%rip)
	callq	vg_set_color
	movsd	x(%rip), %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %ecx
	movsd	y(%rip), %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %edx
	movl	$4, %r8d
	callq	vg_draw_circle
	movl	$16777215, %ecx
	callq	vg_set_color
	movsd	x(%rip), %xmm0
	addsd	%xmm15, %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %ecx
	movsd	y(%rip), %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %edx
	callq	vg_draw_pixel
	movsd	x(%rip), %xmm0
	addsd	%xmm13, %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %ecx
	movsd	y(%rip), %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %edx
	callq	vg_draw_pixel
	movsd	x(%rip), %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %ecx
	movsd	y(%rip), %xmm0
	addsd	%xmm15, %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %edx
	callq	vg_draw_pixel
	movsd	x(%rip), %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %ecx
	movsd	y(%rip), %xmm0
	addsd	%xmm13, %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %edx
	callq	vg_draw_pixel
	movsd	rad(%rip), %xmm11
	addsd	%xmm9, %xmm11
	movsd	%xmm11, rad(%rip)
	movsd	__real@4070400000000000(%rip), %xmm0
	ucomisd	%xmm11, %xmm0
	jbe	.LBB0_6
.LBB0_3:
	movsd	arm(%rip), %xmm0
	mulsd	__real@404e000000000000(%rip), %xmm0
	addsd	t(%rip), %xmm0
	addsd	%xmm11, %xmm0
	movsd	%xmm0, ang(%rip)
	movsd	cx(%rip), %xmm10
	mulsd	%xmm12, %xmm0
	divsd	%xmm14, %xmm0
	callq	cos
	mulsd	%xmm11, %xmm0
	addsd	%xmm10, %xmm0
	movsd	%xmm0, x(%rip)
	movsd	cy(%rip), %xmm6
	movsd	rad(%rip), %xmm7
	movsd	ang(%rip), %xmm0
	mulsd	%xmm12, %xmm0
	divsd	%xmm14, %xmm0
	callq	sin
	mulsd	%xmm7, %xmm0
	addsd	%xmm6, %xmm0
	movsd	%xmm0, y(%rip)
	movsd	rad(%rip), %xmm0
	divsd	__real@4038000000000000(%rip), %xmm0
	addsd	arm(%rip), %xmm0
	addsd	%xmm8, %xmm0
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
	movl	$16711935, %ecx
	cmpl	$5, %eax
	jae	.LBB0_5
	cltq
	movl	(%rbx,%rax,4), %ecx
	jmp	.LBB0_5
	.p2align	4, 0x90
.LBB0_7:
	movq	$0, star(%rip)
	xorpd	%xmm0, %xmm0
	movsd	__real@404a800000000000(%rip), %xmm6
	movsd	__real@401c000000000000(%rip), %xmm10
	movsd	__real@4024000000000000(%rip), %xmm11
	.p2align	4, 0x90
.LBB0_8:
	movsd	t(%rip), %xmm1
	movapd	%xmm0, %xmm2
	movapd	%xmm1, %xmm3
	movapd	%xmm0, %xmm4
	mulsd	%xmm10, %xmm0
	addsd	%xmm1, %xmm0
	mulsd	__real@402a000000000000(%rip), %xmm1
	mulsd	__real@4058400000000000(%rip), %xmm2
	addsd	%xmm1, %xmm2
	addsd	%xmm8, %xmm2
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
	movsd	%xmm1, sx(%rip)
	mulsd	__real@403d000000000000(%rip), %xmm3
	mulsd	%xmm6, %xmm4
	addsd	%xmm3, %xmm4
	addsd	%xmm8, %xmm4
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
	movsd	%xmm1, sy(%rip)
	divsd	%xmm11, %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %eax
	testb	$1, %al
	movl	$65535, %ecx
	cmovel	%ebp, %ecx
	movl	%ecx, col(%rip)
	callq	vg_set_color
	movsd	sx(%rip), %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %ecx
	movsd	sy(%rip), %xmm0
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %edx
	callq	vg_draw_pixel
	movsd	star(%rip), %xmm0
	addsd	%xmm7, %xmm0
	movsd	%xmm0, star(%rip)
	movsd	__real@4049000000000000(%rip), %xmm1
	ucomisd	%xmm0, %xmm1
	ja	.LBB0_8
	movsd	t(%rip), %xmm0
	movapd	%xmm0, %xmm1
	addsd	%xmm8, %xmm1
	cvttsd2si	%xmm1, %eax
	imull	$-1527099483, %eax, %eax
	addl	$47721856, %eax
	rorl	$2, %eax
	cmpl	$23860928, %eax
	ja	.LBB0_14
	movsd	cx(%rip), %xmm6
	movsd	__real@405ec00000000000(%rip), %xmm11
	addsd	%xmm11, %xmm0
	mulsd	%xmm12, %xmm0
	divsd	%xmm14, %xmm0
	callq	cos
	movsd	__real@4070400000000000(%rip), %xmm10
	mulsd	%xmm10, %xmm0
	addsd	%xmm6, %xmm0
	movsd	%xmm0, sx(%rip)
	movsd	cy(%rip), %xmm6
	movsd	t(%rip), %xmm0
	addsd	%xmm11, %xmm0
	mulsd	%xmm12, %xmm0
	divsd	%xmm14, %xmm0
	callq	sin
	mulsd	%xmm10, %xmm0
	addsd	%xmm6, %xmm0
	movsd	__real@4010000000000000(%rip), %xmm6
	movsd	%xmm0, sy(%rip)
	movq	$0, sparkleT(%rip)
	movsd	sx(%rip), %xmm1
	addsd	%xmm8, %xmm1
	cvttsd2si	%xmm1, %esi
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %edi
	xorpd	%xmm0, %xmm0
	jmp	.LBB0_11
	.p2align	4, 0x90
.LBB0_13:
	movl	%ecx, col(%rip)
	callq	vg_set_color
	movsd	sparkleT(%rip), %xmm0
	mulsd	%xmm8, %xmm0
	movapd	%xmm6, %xmm1
	subsd	%xmm0, %xmm1
	addsd	%xmm8, %xmm1
	cvttsd2si	%xmm1, %r8d
	movl	%esi, %ecx
	movl	%edi, %edx
	callq	vg_draw_circle
	movsd	sparkleT(%rip), %xmm0
	addsd	%xmm7, %xmm0
	movsd	%xmm0, sparkleT(%rip)
	ucomisd	%xmm0, %xmm9
	jbe	.LBB0_14
.LBB0_11:
	addsd	%xmm8, %xmm0
	cvttsd2si	%xmm0, %eax
	testb	$1, %al
	movl	$16711935, %ecx
	je	.LBB0_13
	movl	$16776960, %ecx
	jmp	.LBB0_13
.LBB0_15:
	xorl	%eax, %eax
	movaps	32(%rsp), %xmm6
	movaps	48(%rsp), %xmm7
	movaps	64(%rsp), %xmm8
	movaps	80(%rsp), %xmm9
	movaps	96(%rsp), %xmm10
	movaps	112(%rsp), %xmm11
	movaps	128(%rsp), %xmm12
	movaps	144(%rsp), %xmm13
	movaps	160(%rsp), %xmm14
	movaps	176(%rsp), %xmm15
	addq	$192, %rsp
	popq	%rbx
	popq	%rbp
	popq	%rdi
	popq	%rsi
	popq	%r14
	retq
	.seh_endproc

	.def	sparkle;
	.scl	2;
	.type	32;
	.endef
	.globl	sparkle
	.p2align	4, 0x90
sparkle:
.seh_proc sparkle
	pushq	%rsi
	.seh_pushreg %rsi
	pushq	%rdi
	.seh_pushreg %rdi
	subq	$104, %rsp
	.seh_stackalloc 104
	movaps	%xmm9, 80(%rsp)
	.seh_savexmm %xmm9, 80
	movaps	%xmm8, 64(%rsp)
	.seh_savexmm %xmm8, 64
	movaps	%xmm7, 48(%rsp)
	.seh_savexmm %xmm7, 48
	movaps	%xmm6, 32(%rsp)
	.seh_savexmm %xmm6, 32
	.seh_endprologue
	movq	$0, sparkleT(%rip)
	movsd	__real@3fe0000000000000(%rip), %xmm6
	addsd	%xmm6, %xmm0
	cvttsd2si	%xmm0, %esi
	addsd	%xmm6, %xmm1
	cvttsd2si	%xmm1, %edi
	xorpd	%xmm0, %xmm0
	movsd	__real@4010000000000000(%rip), %xmm8
	movsd	__real@3ff0000000000000(%rip), %xmm9
	movsd	__real@4018000000000000(%rip), %xmm7
	jmp	.LBB1_1
	.p2align	4, 0x90
.LBB1_3:
	movl	%ecx, col(%rip)
	callq	vg_set_color
	movsd	sparkleT(%rip), %xmm0
	mulsd	%xmm6, %xmm0
	movapd	%xmm8, %xmm1
	subsd	%xmm0, %xmm1
	addsd	%xmm6, %xmm1
	cvttsd2si	%xmm1, %r8d
	movl	%esi, %ecx
	movl	%edi, %edx
	callq	vg_draw_circle
	movsd	sparkleT(%rip), %xmm0
	addsd	%xmm9, %xmm0
	movsd	%xmm0, sparkleT(%rip)
	ucomisd	%xmm0, %xmm7
	jbe	.LBB1_4
.LBB1_1:
	addsd	%xmm6, %xmm0
	cvttsd2si	%xmm0, %eax
	testb	$1, %al
	movl	$16711935, %ecx
	je	.LBB1_3
	movl	$16776960, %ecx
	jmp	.LBB1_3
.LBB1_4:
	movaps	32(%rsp), %xmm6
	movaps	48(%rsp), %xmm7
	movaps	64(%rsp), %xmm8
	movaps	80(%rsp), %xmm9
	addq	$104, %rsp
	popq	%rdi
	popq	%rsi
	retq
	.seh_endproc

	.def	_main;
	.scl	2;
	.type	32;
	.endef
	.globl	_main
	.p2align	4, 0x90
_main:
.seh_proc _main
	subq	$40, %rsp
	.seh_stackalloc 40
	.seh_endprologue
	callq	main
	xorl	%eax, %eax
	addq	$40, %rsp
	retq
	.seh_endproc

	.bss
	.globl	cx
	.p2align	3
cx:
	.quad	0x0000000000000000

	.globl	cy
	.p2align	3
cy:
	.quad	0x0000000000000000

	.globl	t
	.p2align	3
t:
	.quad	0x0000000000000000

	.globl	arm
	.p2align	3
arm:
	.quad	0x0000000000000000

	.globl	ang
	.p2align	3
ang:
	.quad	0x0000000000000000

	.globl	rad
	.p2align	3
rad:
	.quad	0x0000000000000000

	.globl	x
	.p2align	3
x:
	.quad	0x0000000000000000

	.globl	y
	.p2align	3
y:
	.quad	0x0000000000000000

	.globl	star
	.p2align	3
star:
	.quad	0x0000000000000000

	.globl	sx
	.p2align	3
sx:
	.quad	0x0000000000000000

	.globl	sy
	.p2align	3
sy:
	.quad	0x0000000000000000

	.globl	sparkleT
	.p2align	3
sparkleT:
	.quad	0x0000000000000000

	.data
	.globl	col
	.p2align	2
col:
	.long	16777215

	.section	.rdata,"dr"
	.p2align	2
.Lswitch.table.main:
	.long	16711680
	.long	16776960
	.long	65280
	.long	65535
	.long	255

	.globl	_fltused