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
	.globl	__real@4062c00000000000
	.section	.rdata,"dr",discard,__real@4062c00000000000
	.p2align	3
__real@4062c00000000000:
	.quad	0x4062c00000000000
	.globl	__real@4084500000000000
	.section	.rdata,"dr",discard,__real@4084500000000000
	.p2align	3
__real@4084500000000000:
	.quad	0x4084500000000000
	.globl	__real@3ff0000000000000
	.section	.rdata,"dr",discard,__real@3ff0000000000000
	.p2align	3
__real@3ff0000000000000:
	.quad	0x3ff0000000000000
	.globl	__real@4059000000000000
	.section	.rdata,"dr",discard,__real@4059000000000000
	.p2align	3
__real@4059000000000000:
	.quad	0x4059000000000000
	.globl	__real@4079000000000000
	.section	.rdata,"dr",discard,__real@4079000000000000
	.p2align	3
__real@4079000000000000:
	.quad	0x4079000000000000
	.globl	__real@4000000000000000
	.section	.rdata,"dr",discard,__real@4000000000000000
	.p2align	3
__real@4000000000000000:
	.quad	0x4000000000000000
	.globl	__real@407c200000000000
	.section	.rdata,"dr",discard,__real@407c200000000000
	.p2align	3
__real@407c200000000000:
	.quad	0x407c200000000000
	.globl	__real@4008000000000000
	.section	.rdata,"dr",discard,__real@4008000000000000
	.p2align	3
__real@4008000000000000:
	.quad	0x4008000000000000
	.globl	__real@4010000000000000
	.section	.rdata,"dr",discard,__real@4010000000000000
	.p2align	3
__real@4010000000000000:
	.quad	0x4010000000000000
	.globl	__xmm@40845000000000004079000000000000
	.section	.rdata,"dr",discard,__xmm@40845000000000004079000000000000
	.p2align	4
__xmm@40845000000000004079000000000000:
	.quad	0x4079000000000000
	.quad	0x4084500000000000
	.globl	__xmm@407c200000000000407f400000000000
	.section	.rdata,"dr",discard,__xmm@407c200000000000407f400000000000
	.p2align	4
__xmm@407c200000000000407f400000000000:
	.quad	0x407f400000000000
	.quad	0x407c200000000000
	.globl	__real@404e000000000000
	.section	.rdata,"dr",discard,__real@404e000000000000
	.p2align	3
__real@404e000000000000:
	.quad	0x404e000000000000
	.globl	__real@4018000000000000
	.section	.rdata,"dr",discard,__real@4018000000000000
	.p2align	3
__real@4018000000000000:
	.quad	0x4018000000000000
	.text
	.globl	main
	.p2align	4, 0x90
main:
.seh_proc main
	pushq	%rsi
	.seh_pushreg %rsi
	pushq	%rdi
	.seh_pushreg %rdi
	subq	$216, %rsp
	.seh_stackalloc 216
	movaps	%xmm15, 192(%rsp)
	.seh_savexmm %xmm15, 192
	movaps	%xmm14, 176(%rsp)
	.seh_savexmm %xmm14, 176
	movaps	%xmm13, 160(%rsp)
	.seh_savexmm %xmm13, 160
	movaps	%xmm12, 144(%rsp)
	.seh_savexmm %xmm12, 144
	movaps	%xmm11, 128(%rsp)
	.seh_savexmm %xmm11, 128
	movaps	%xmm10, 112(%rsp)
	.seh_savexmm %xmm10, 112
	movaps	%xmm9, 96(%rsp)
	.seh_savexmm %xmm9, 96
	movapd	%xmm8, 80(%rsp)
	.seh_savexmm %xmm8, 80
	movaps	%xmm7, 64(%rsp)
	.seh_savexmm %xmm7, 64
	movaps	%xmm6, 48(%rsp)
	.seh_savexmm %xmm6, 48
	.seh_endprologue
	xorl	%ecx, %ecx
	callq	vg_set_color
	xorl	%ecx, %ecx
	xorl	%edx, %edx
	movl	$799, %r8d
	movl	$599, %r9d
	callq	vg_draw_rect
	movabsq	$4617315517961601024, %rax
	movq	%rax, depth(%rip)
	movabsq	$4654751689864118272, %rax
	movq	%rax, len100(%rip)
	movq	$0, pos(%rip)
	xorpd	%xmm8, %xmm8
	movsd	__real@4062c00000000000(%rip), %xmm9
	movsd	__real@404e000000000000(%rip), %xmm10
	movsd	__real@3ff0000000000000(%rip), %xmm7
	movsd	__real@4018000000000000(%rip), %xmm6
	movsd	__real@4084500000000000(%rip), %xmm11
	movsd	__real@4059000000000000(%rip), %xmm12
	movsd	__real@4079000000000000(%rip), %xmm13
	movsd	__real@4000000000000000(%rip), %xmm14
	movsd	__real@407c200000000000(%rip), %xmm15
	leaq	__xmm@40845000000000004079000000000000(%rip), %rsi
	leaq	__xmm@407c200000000000407f400000000000(%rip), %rdi
	xorpd	%xmm0, %xmm0
	.p2align	4, 0x90
.LBB0_1:
	ucomisd	%xmm8, %xmm0
	movaps	%xmm9, %xmm1
	movaps	%xmm9, %xmm2
	jne	.LBB0_6
	jnp	.LBB0_2
.LBB0_6:
	ucomisd	%xmm7, %xmm0
	movaps	%xmm11, %xmm1
	movaps	%xmm9, %xmm2
	jne	.LBB0_7
	jnp	.LBB0_2
.LBB0_7:
	ucomisd	%xmm14, %xmm0
	movaps	%xmm13, %xmm1
	movaps	%xmm12, %xmm2
	jne	.LBB0_8
	jnp	.LBB0_2
.LBB0_8:
	ucomisd	__real@4008000000000000(%rip), %xmm0
	movaps	%xmm9, %xmm1
	movaps	%xmm15, %xmm2
	jne	.LBB0_9
	jnp	.LBB0_2
.LBB0_9:
	cmpeqsd	__real@4010000000000000(%rip), %xmm0
	movq	%xmm0, %rax
	andl	$1, %eax
	movsd	(%rsi,%rax,8), %xmm1
	movsd	(%rdi,%rax,8), %xmm2
	.p2align	4, 0x90
.LBB0_2:
	movsd	%xmm1, x1(%rip)
	movsd	%xmm2, y1(%rip)
	movq	$0, axis(%rip)
	xorpd	%xmm3, %xmm3
	.p2align	4, 0x90
.LBB0_3:
	mulsd	%xmm10, %xmm3
	movsd	%xmm3, ang(%rip)
	movsd	x1(%rip), %xmm0
	movsd	y1(%rip), %xmm1
	movsd	len100(%rip), %xmm2
	movsd	depth(%rip), %xmm4
	movsd	%xmm4, 32(%rsp)
	callq	triBranch
	movsd	axis(%rip), %xmm3
	addsd	%xmm7, %xmm3
	movsd	%xmm3, axis(%rip)
	ucomisd	%xmm3, %xmm6
	ja	.LBB0_3
	movsd	pos(%rip), %xmm0
	addsd	%xmm7, %xmm0
	movsd	%xmm0, pos(%rip)
	ucomisd	%xmm0, %xmm6
	ja	.LBB0_1
	xorl	%eax, %eax
	movaps	48(%rsp), %xmm6
	movaps	64(%rsp), %xmm7
	movaps	80(%rsp), %xmm8
	movaps	96(%rsp), %xmm9
	movaps	112(%rsp), %xmm10
	movaps	128(%rsp), %xmm11
	movaps	144(%rsp), %xmm12
	movaps	160(%rsp), %xmm13
	movaps	176(%rsp), %xmm14
	movaps	192(%rsp), %xmm15
	addq	$216, %rsp
	popq	%rdi
	popq	%rsi
	retq
	.seh_endproc

	.def	triBranch;
	.scl	2;
	.type	32;
	.endef
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
	.globl	__real@3fe0000000000000
	.section	.rdata,"dr",discard,__real@3fe0000000000000
	.p2align	3
__real@3fe0000000000000:
	.quad	0x3fe0000000000000
	.globl	__real@4049000000000000
	.section	.rdata,"dr",discard,__real@4049000000000000
	.p2align	3
__real@4049000000000000:
	.quad	0x4049000000000000
	.globl	__real@bff0000000000000
	.section	.rdata,"dr",discard,__real@bff0000000000000
	.p2align	3
__real@bff0000000000000:
	.quad	0xbff0000000000000
	.globl	__real@c04e000000000000
	.section	.rdata,"dr",discard,__real@c04e000000000000
	.p2align	3
__real@c04e000000000000:
	.quad	0xc04e000000000000
	.text
	.globl	triBranch
	.p2align	4, 0x90
triBranch:
.seh_proc triBranch
	pushq	%rsi
	.seh_pushreg %rsi
	pushq	%rdi
	.seh_pushreg %rdi
	subq	$216, %rsp
	.seh_stackalloc 216
	movapd	%xmm15, 192(%rsp)
	.seh_savexmm %xmm15, 192
	movapd	%xmm14, 176(%rsp)
	.seh_savexmm %xmm14, 176
	movapd	%xmm13, 160(%rsp)
	.seh_savexmm %xmm13, 160
	movapd	%xmm12, 144(%rsp)
	.seh_savexmm %xmm12, 144
	movaps	%xmm11, 128(%rsp)
	.seh_savexmm %xmm11, 128
	movapd	%xmm10, 112(%rsp)
	.seh_savexmm %xmm10, 112
	movaps	%xmm9, 96(%rsp)
	.seh_savexmm %xmm9, 96
	movapd	%xmm8, 80(%rsp)
	.seh_savexmm %xmm8, 80
	movapd	%xmm7, 64(%rsp)
	.seh_savexmm %xmm7, 64
	movaps	%xmm6, 48(%rsp)
	.seh_savexmm %xmm6, 48
	.seh_endprologue
	movapd	%xmm1, %xmm9
	movapd	%xmm0, %xmm6
	movsd	272(%rsp), %xmm11
	xorpd	%xmm12, %xmm12
	ucomisd	%xmm12, %xmm11
	jne	.LBB1_1
	jp	.LBB1_1
.LBB1_5:
	movl	$65280, %ecx
	callq	vg_set_color
	movsd	__real@3fe0000000000000(%rip), %xmm0
	addsd	%xmm0, %xmm6
	cvttsd2si	%xmm6, %ecx
	addsd	%xmm0, %xmm9
	cvttsd2si	%xmm9, %edx
	movl	$2, %r8d
	movaps	48(%rsp), %xmm6
	movaps	64(%rsp), %xmm7
	movaps	80(%rsp), %xmm8
	movaps	96(%rsp), %xmm9
	movaps	112(%rsp), %xmm10
	movaps	128(%rsp), %xmm11
	movaps	144(%rsp), %xmm12
	movaps	160(%rsp), %xmm13
	movaps	176(%rsp), %xmm14
	movaps	192(%rsp), %xmm15
	addq	$216, %rsp
	popq	%rdi
	popq	%rsi
	jmp	vg_draw_circle
.LBB1_1:
	movapd	%xmm3, %xmm8
	movapd	%xmm2, %xmm10
	movsd	__real@4059000000000000(%rip), %xmm15
	movsd	__real@3fe0000000000000(%rip), %xmm13
	leaq	.Lswitch.table.triBranch(%rip), %rdi
	movsd	__real@3ff0000000000000(%rip), %xmm14
	jmp	.LBB1_2
	.p2align	4, 0x90
.LBB1_4:
	movl	%ecx, col(%rip)
	callq	vg_set_color
	movapd	%xmm6, %xmm0
	addsd	%xmm13, %xmm0
	cvttsd2si	%xmm0, %ecx
	addsd	%xmm13, %xmm9
	cvttsd2si	%xmm9, %esi
	movsd	x2(%rip), %xmm0
	addsd	%xmm13, %xmm0
	cvttsd2si	%xmm0, %r8d
	movsd	y2(%rip), %xmm0
	addsd	%xmm13, %xmm0
	cvttsd2si	%xmm0, %r9d
	movl	%esi, %edx
	callq	vg_draw_line
	addsd	%xmm14, %xmm6
	addsd	%xmm13, %xmm6
	cvttsd2si	%xmm6, %ecx
	movsd	x2(%rip), %xmm0
	addsd	%xmm14, %xmm0
	addsd	%xmm13, %xmm0
	cvttsd2si	%xmm0, %r8d
	movsd	y2(%rip), %xmm0
	addsd	%xmm13, %xmm0
	cvttsd2si	%xmm0, %r9d
	movl	%esi, %edx
	callq	vg_draw_line
	mulsd	__real@4049000000000000(%rip), %xmm10
	divsd	%xmm15, %xmm10
	movsd	x2(%rip), %xmm0
	movsd	y2(%rip), %xmm1
	addsd	__real@bff0000000000000(%rip), %xmm11
	movsd	%xmm11, 32(%rsp)
	movapd	%xmm10, %xmm2
	movapd	%xmm8, %xmm3
	callq	triBranch
	movsd	x2(%rip), %xmm0
	movsd	y2(%rip), %xmm1
	movapd	%xmm8, %xmm3
	addsd	__real@c04e000000000000(%rip), %xmm3
	movsd	%xmm11, 32(%rsp)
	movapd	%xmm10, %xmm2
	callq	triBranch
	movsd	x2(%rip), %xmm6
	movsd	y2(%rip), %xmm9
	addsd	__real@404e000000000000(%rip), %xmm8
	ucomisd	%xmm12, %xmm11
	jne	.LBB1_2
	jnp	.LBB1_5
.LBB1_2:
	movapd	%xmm8, %xmm7
	mulsd	__real@400921ff2e48e8a7(%rip), %xmm7
	divsd	__real@4066800000000000(%rip), %xmm7
	movapd	%xmm7, %xmm0
	callq	cos
	mulsd	%xmm10, %xmm0
	divsd	%xmm15, %xmm0
	addsd	%xmm6, %xmm0
	movsd	%xmm0, x2(%rip)
	movapd	%xmm7, %xmm0
	callq	sin
	mulsd	%xmm10, %xmm0
	divsd	%xmm15, %xmm0
	movapd	%xmm9, %xmm1
	subsd	%xmm0, %xmm1
	movsd	%xmm1, y2(%rip)
	movapd	%xmm11, %xmm0
	addsd	%xmm13, %xmm0
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
	cmpl	$4, %eax
	ja	.LBB1_4
	cltq
	movl	(%rdi,%rax,4), %ecx
	jmp	.LBB1_4
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
	.globl	x1
	.p2align	3
x1:
	.quad	0x0000000000000000

	.globl	y1
	.p2align	3
y1:
	.quad	0x0000000000000000

	.globl	x2
	.p2align	3
x2:
	.quad	0x0000000000000000

	.globl	y2
	.p2align	3
y2:
	.quad	0x0000000000000000

	.globl	len100
	.p2align	3
len100:
	.quad	0x0000000000000000

	.globl	ang
	.p2align	3
ang:
	.quad	0x0000000000000000

	.globl	depth
	.p2align	3
depth:
	.quad	0x0000000000000000

	.globl	axis
	.p2align	3
axis:
	.quad	0x0000000000000000

	.globl	pos
	.p2align	3
pos:
	.quad	0x0000000000000000

	.data
	.globl	col
	.p2align	2
col:
	.long	16777215

	.section	.rdata,"dr"
	.p2align	2
.Lswitch.table.triBranch:
	.long	16711680
	.long	16776960
	.long	65280
	.long	65535
	.long	255

	.globl	_fltused