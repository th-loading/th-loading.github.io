---
title: CS:APP Attack Lab记录
date: 2023-06-29 19:23:08 
tags: CS

---



# 前置知识

### Y86

esp - rsp 第三版CSAPP全部使用8Byte

Y86指令集对应Y86处理器，Sequential operation，每个周期执行一个完整的Y86指令，可以拆分出五个阶段，执行指令流水线（？数字电路的实现）

programmer-visible 程序员可见的状态，编译器 / 用汇编代码写程序的人，Y86与x86对应的寄存器结构是类似的，栈指针、传参、返回参数、条件码、PC。

Y86的汇编指令使用内存虚拟地址，由硬件和操作系统在读入程序时载入。状态码Stat 异常状态。

只有8字节的数据，称之为word 字，变长指令字，

addl, subl, andl, and xorl 对应 ZF, SF, and OF (zero, sign, and overflow)

### HCL

硬件控制语言，从逻辑电路图到硬件描述语言，Verilog 根据描述生成电路，high-level Language。Single  Bit，高电平表示1，反之表示0，与或非门。基本的对象时逻辑电路，bool eq = (a && b) || (!a && !b) ，持续响应输入的变化。

出于简单，每个字集都视为int，有 bool Eq = (A == B)。

# 具体流程

## Part A

汇编程序

定义出链表的结构

```assembly
# Sample linked list
.align 8
ele1:
	.quad 0x00a
	.quad ele2
ele2:
	.quad 0x0b0
	.quad ele3
ele3:
	.quad 0xc00
	.quad 0
```

C语言传参与处理的汇编代码

main函数内定义

```c
# C 需要struct Node代表结构体，一般辅助使用typedef 
typedef struct Node{
    int v;
    struct Node *next;
}Node;

int add(Node *head) {
    int v = 0;
    while(head) {
        v += head->v;
        head = head->next; 
    }
}

int main() {
    Node n1, n2, n3;
    n1.v = 1, n1.next = &n2, n2.v = 2, n2.next = &n3, n3.v = 3, n3.next = 0;
    add(&n1); 
}
```

```assembly
# ATT 格式 x86 

# 申请空间
subq	$64, %rsp
# ? 段保护
movq	%fs:40, %rax
# 占一个8Byte
movq	%rax, -8(%rbp)
# 清 0
xorl	%eax, %eax

# n1.v = 1
movl	$1, -64(%rbp)

# &n2 -> n1.next
leaq	-48(%rbp), %rax
movq	%rax, -56(%rbp)

# n2.v = 2, 同时代表&n2
movl	$2, -48(%rbp)
leaq	-32(%rbp), %rax
movq	%rax, -40(%rbp)
movl	$3, -32(%rbp)
movq	$0, -24(%rbp)

# 传入 &n1
leaq	-64(%rbp), %rax

movq	%rax, %rdi
```

全局变量的定义

```c
typedef struct Node{
    int v;
    struct Node *next;
}Node;

Node n3 = {3, 0}, n2 = {2, &n3}, n1 = {1, &n2};

int add(Node *head) {
    int v = 0;
    while(head) {
        v += head->v;
        head = head->next; 
    }
}

int main() {
    add(&n1); 
}
```

```assembly
n3:
	.long	3
	.zero	4
	.quad	0
	.globl	n2
	.section	.data.rel.local,"aw"
	.align 16
	.type	n2, @object
	.size	n2, 16
n2:
	.long	2
	.zero	4
	.quad	n3
	.globl	n1
	.align 16
	.type	n1, @object
	.size	n1, 16
n1:
	.long	1
	.zero	4
	.quad	n2
	.text
	.globl	add
	.type	add, @function

# [rip + a] or AT&T a(%rip) means to calculate a rel32 displacement to reach a

# 代表n1的地址 （指向代码段而不是栈，代表全局变量）
leaq	n1(%rip), %rdi

# 后借助8 Byte后的地址完成跳转
movq	-24(%rbp), %rax
movq	8(%rax), %rax
```

ys中都使用全局变量的方式，寻址的方式也较为简单

注意有INIT的过程，需要手动声明栈大小等。

```assembly
# Sample linked list
    .pos 0
    irmovq stack, %rsp 
    call main
    halt
    
    .align 8
ele1:
	.quad 0x00a
	.quad ele2
ele2:
	.quad 0x0b0
	.quad ele3
ele3:
	.quad 0xc00
	.quad 0

main:
    irmovq ele1, %rdx
    pushq %rdx
    call add
    ret

add:
    pushq %rbp
    rrmovq %rsp, %rbp
    xorq %rax, %rax
    mrmovq 16(%rbp), %rcx
loop:
    andq %rcx, %rcx
    je end
    mrmovq (%rcx), %rdx
    addq %rdx, %rax
    mrmovq 8(%rcx), %rcx
    jmp loop
end: 
    popq %rbp
    ret    

    .pos 200
stack:
```

结果

```
Stopped in 33 steps at PC = 0x18.  Status 'HLT', CC Z=1 S=0 O=0
Changes to registers:
%rax:   0x0000000000000000      0x0000000000000cba
```

```assembly
main:
    irmovq ele1, %rdi
    call rsum
    ret

rsum:
    xorq %rax, %rax 
    andq %rdi, %rdi
    je end
    pushq %rbp
    rrmovq %rsp, %rbp 
    mrmovq (%rdi), %rcx
    mrmovq 8(%rdi), %rdi
    pushq %rcx
    call rsum
    popq %rcx
    addq %rcx, %rax 
    rrmovq %rbp, %rsp
    popq %rbp
end:
    ret 

# 十进制 200会爆栈
    .pos 0x200
stack:
```

结果：

```
Stopped in 52 steps at PC = 0x13.  Status 'HLT', CC Z=0 S=0 O=0
Changes to registers:
%rax:   0x0000000000000000      0x0000000000000cba
```

```assembly
# Source block
src:
    .quad 0x00a
    .quad 0x0b0
    .quad 0xc00

# Destination block
dest:
    .quad 0x111
    .quad 0x222
    .quad 0x333

copy:
    mrmovq 8(%rsp), %rdx
    mrmovq 16(%rsp), %rcx
    mrmovq 24(%rsp), %rbx
    xorq %rax, %rax   
loop:
    andq %rdx, %rdx
    je end
    irmovq $-1, %r8
    addq %r8, %rdx
    mrmovq (%rbx), %r8
    xorq %r8, %rax
    rmmovq %r8, (%rcx) 
    irmovq $8, %r8
    addq %r8, %rcx
    addq %r8, %rbx  
    jmp loop
end:
    ret

main:
    irmovq src, %rdx
    pushq %rdx
    irmovq dest, %rdx
    pushq %rdx
    irmovq 0x3, %rdx
    pushq %rdx
    call copy
    ret

    .pos 0x200
stack:
```

结果

```
Stopped in 51 steps at PC = 0x3.  Status 'HLT', CC Z=1 S=0 O=0
Changes to registers:
%rax:   0x0000000000000000      0x0000000000000cba
%rcx:   0x0000000000000000      0x0000000000000048
%rbx:   0x0000000000000000      0x0000000000000030
%rsp:   0x0000000000000000      0x00000000000001e8
%r8:    0x0000000000000000      0x0000000000000008

Changes to memory:
0x0030: 0x0000000000000111      0x000000000000000a
0x0038: 0x0000000000000222      0x00000000000000b0
0x0040: 0x0000000000000333      0x0000000000000c00
```

