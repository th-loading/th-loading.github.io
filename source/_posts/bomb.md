---
title: CS:APP Bomb Lab记录
date: 2023-02-17 11:56:29 
tags: CS
---

# 前置知识

## objdump

objdump -d可将二进制文件转换为汇编代码（反汇编）

## GDB

类似于图形界面的debugger，通过命令行执行。这里针对汇编进行debug。使用tui进行查看。

### 基本流程

```bash
# 确保debug with source code
gcc -g -ggdb csim.c -o csim.out

# 进入汇编调试
# layout split 可以同时看到源代码和汇编代码
layout asm
# refresh
ref

# 从第一个指令开始debug
# Entry point
starti

# 下断点进行debug(break *main也可以)
break *assmbly_address
next step # 相对source code next跳过function
nexti stepi  # 相对assembly code
c #下一个断点
info break # 查看断点信息
delete id # 删除对应断点
```

### 查看修改信息

```bash
# 寄存器
i reg reg_name
i all-registes
# 16进制 /xs
p/x $esi
# 连续展示40byte 40c就是char
x/40b memory_address
# 修改信息
set $rdi = 0x402400
# 设置特定地址的值
set *0x20001234 = 0xABABABAB
```

## 程序运行

### 寄存器设置

%r/eax 为返回值
%r/ebx 被调用者保存
%r/edi r/esi r/edx r/ecx 4对应第四个-第一个参数
%r/ebp 栈尾 %r/esp 栈顶部

### 调用函数

```c
# 如果需要用到栈
	# 存ebp
	pushl %ebp
	# 新的ebp
	movl %esp, %ebp
    
	movl %ebp,%esp
	popl %ebp b  

# 注意隐含的PC
# parameter 
# PC
# EBP'
```

```assembly
# call Main，函数运行的第一个指令实际并不是Main，而是Entry point，gdb starti / info file可以得知。
# libc initializations, heap allocation, 由编译器确定
# y86也存在一个INIT函数
	movl Stack, %esp
	call Main
	halt

Main: 
	# pushl后指针指向的是栈顶元素，而不是空元素。因此不能直接mov到esp。
	
	# 如果函数需要用到栈时
	# 存ebp
	pushl %ebp
	# 新的ebp
	movl %esp, %ebp
	
	# 传参可以借助edi，也可以借助栈。
	call Add 
	

	movl %ebp,%esp
	popl %ebp
	
	# ebp存储的是PC的值
	ret
Add:
	pushl %ebp
	movl %esp, %ebp
	
	# ！Call函数和ret函数隐含有push，pop PC，且在函数开始时一般都要push ebp，保存被调用者的栈起始指针，因此从在64bit系统中，8(ebp) 代表传的第一个参数。
	movl 8(%ebp),%ecx
	
	movl %ebp,%esp
	popl %ebp
	

```

### 汇编指令

主要基于x86指令集架构，也可以不分析，小数据可以借助gdb调试判断。

```assembly
# 比较
CMPL # unsign 
CMP  # a - b
TEST eax, eax # 若eax = 0, ZF = 1

# 跳转
JA # above unsigned CF = 0 and ZF = 0 
JG # greater

# 赋值
movzbl # zero extend byte to long 0 拓展
# AT&T in this syntax, the source comes first and the destination second. 
# 括号代表访存 多用于取地址操作，当MOV为将对应内存地址的数值赋值时，该操作数表示只计算地址。
lea 0x50(%rsp), %rsi # 只计算具体的地址
# 常用于存储指针。

# 按位异或，相同等价于清零
xorl    %eax, %eax
```

### 数据结构

在处理输入时，若不做限制，可能导致栈溢出，无法return的情况。因为接受输入的栈指针对应栈帧的大小有限。因此为了防止栈溢出覆写数据，跳转到攻击代码的情况，会出现%fs:40，采用段寻址的只读代码，又名为金丝雀值，使用系统随机生成，与栈相应位置进行对比，判断是否相同。

# 具体过程

## Quick Start

[进入网站](http://csapp.cs.cmu.edu/3e/labs.html)，下载write_up.pdf，并在可运行环境下下载文件。

```bash
# wsl ubuntu18.04 x86_64 
wget http://csapp.cs.cmu.edu/3e/bomb.tar
tar -xvf bomb.tar 
```

从bomb.c可知需要输入六句话。只能通过反汇编得到要输入的文件。由write_up的hints可知需要使用到gdb与objdump。有两个方向，通过objdump -d直接分析汇编代码。

```bash
objdump -d bomb > a.asm 
vim a.asm 
# 可对照分析 crtl + w + z 对换;crtl + z 后 fg 保留状态 :vnew bomb.c
```

## bomb1

先分析汇编

```assembly
# main
callq  40149e <read_line>
# 传入第一个参数
mov    %rax,%rdi
# 这里set $rdi = 0x402400 可以直接defuse, 也可以看出，核心在于使得这里的rax变成0x402400...其实是地址,这里以为是数值...
callq  400ee0 <phase_1>

# phase_1
# 留出8Byte
sub    $0x8,%rsp
# ！第二个参数 代表string
mov    $0x402400,%esi
callq  0x401338 <strings_not_equal>                                     
# If %eax为0, 则会跳转 即代表false
test   %eax,%eax 
je     0x400ef7 <phase_1+23>
callq  0x40143a <explode_bomb>  
```

可以得到与rdi比较的16进制表示为0x402400，因此需要输入read_line(string) = 0x402400。先通过gdb观察，输入123，输出的0x603780，而1的ascii码为49 0x31，似乎没有明显联系。

```assembly
# read_lines
sub    $0x8,%rsp
mov    $0x0,%eax
callq  0x4013f9 <skip>
# gdb发现这一步输入就已经是0x603780了 且不管输入什么都是0x603780
test   %rax,%rax
jne    0x40151f <read_line+129>                                         
```

输入1231和abc查看所有的寄存器的区别，发现只有rcx、rbp有不同，似乎是长度，莫非入栈了? 看来需要阅读skip的源码。

```assembly
0x40141c <skip+35>      callq  0x400b80 <fgets@plt>
```

于是问题转换到fgets的数据存在了哪里。原来0x603780指的不是数据，而是内存的地址...

0x603780 0a|33|32|31 按字节编址 'a' 31 'b' 32 'c' 33  a '\n' 0 '0'，从右往左显示...！体现了小端序，这里为了显示数字转置了。

0x603781 00|0a|33|32  0x603782 00|00|0a|33 

所以只需要在比较之前设个断点，看0x402400对应的内存数组就可以了。 x/60s 0x402400。得到结果。Border relations with Canada have never been better.

## bomb2

从源码可以看出，在read_six_number中进行判断。

```bash
break *main+182 
# 自动输入第一次的结果
run a.txt
```

```assembly
sub    $0x18,%rsp                                                    

mov    %rsi,%rdx                                                        
lea    0x4(%rsi),%rcx                                                   
lea    0x14(%rsi),%rax                                                   
mov    %rax,0x8(%rsp)                                                   
lea    0x10(%rsi),%rax                                                   
mov    %rax,(%rsp)                                                      
lea    0xc(%rsi),%r9                                                    
lea    0x8(%rsi),%r8                                                     
# 第二个参数
mov    $0x4025c3,%esi                                                   
mov    $0x0,%eax
# int sscanf(const char *str, const char *format, ...)
# 先存到栈顶
callq  0x400bf0 <__isoc99_sscanf@plt>                                  
cmp    $0x5,%eax 
# 不知道具体的format尝试1 2 3 4 5 6 得到eax=6,成功跳过第一个explode  
# x/16s 4025c3即可得到format "%d %d %d %d %d %d"
jg     0x401499 <read_six_numbers+61>
callq  0x40143a <explode_bomb>
# 释放空间
add    $0x18,%rsp  
retq   

# 第一个int，比较rsp的开头是不是1
cmpl   $0x1,(%rsp)
je     0x400f30 <phase_2+52>
0x40143a <explode_bomb>

# 4byte存储第二个int 
# rsp = 0x7fffffffda90 rbx = 0x7fffffffda94 第二个int
lea    0x4(%rsp),%rbx
# 16 + 8 = 24 byte 的空间 rbp为末尾
lea    0x18(%rsp),%rbp
# ---------- jump ----------- 
# ... 不就是第一个数字
mov    -0x4(%rbx),%eax

# 所以第二个int等于第一个int *2 
add    %eax,%eax
cmp    %eax,(%rbx)

# 第三个int
add    $0x4,%rbx
# 比较rbx是否到头
cmp    %rbp,%rbx
# 比较是否等于2倍的代码
jne    0x400f17 <phase_2+27>
# 直接退出的函数
jmp    0x400f3c <phase_2+64>

# 所以得到两倍递推 
# 1 2 4 8 16 
```

较第一问轻松了不少，熟悉了指令集的分析方式。

## bomb3

照例先分析汇编找方向，从scanf入手

```bash
break *main+210
# 自动输入第一次的结果
run a.txt
# 查看format
i r rsi
x/16s addr
# 得到 "%d %d"
```

```assembly
# 可知所处的位置 接受的第一 第二个int
0x400f4c <phase_3+9>    lea    0x8(%rsp),%rdx
0x400f47 <phase_3+4>    lea    0xc(%rsp),%rcx

# 第一个int应该比7小
cmpl   $0x7,0x8(%rsp)
ja     0x400fad <phase_3+106> # explode 

mov    0x8(%rsp),%eax 
# jump directly
jmpq   *0x402470(,%rax,8)

# x/24x 0x402470 0-7对应的跳转路线
0x00400f7c # 下一跳指令 

0x00400fb9 # 可跳转到
mov    $0x137,%eax
# 十六进制的137
cmp    0xc(%rsp),%eax
je     0x400fc9 <phase_3+134>

0x00400f83  0x00400f8a 0x00400f91 0x00400f98  x00400f9f  0x00400fa6

# 可知 1 311 

```

## bomb4

同理，scanf 入手

```bash
break *main+238
run a.txt
i r rsi
x/16s addr
# "%d %d"
```

后分析汇编

```assembly
# 两组
cmp    $0x2,%eax
jne    0x401035 <phase_4+41> # explode

# 首位不为15
cmpl   $0xe,0x8(%rsp)
jbe    0x40103a <phase_4+46>

# 调用func4, 先分析后面来判断func4的要求

# eax为1时不跳转
test   %eax,%eax
jne    0x401058 <phase_4+76> # explode  

# 第二个数字为0
cmpl   $0x0,0xc(%rsp) 
je     0x40105d <phase_4+81>

# 后分析func4 输入
# edi = 第一个数字 | 三个参数 esi = 0  edx = 15 
mov    %edx, %eax # eax = 15
# eax <- eax - esi
sub    %esi, %eax # eax = eax 
mov    %eax, %ecx # ecx = eax 
# ecx <- ecx >> ecx位数
shr    $0x1f,%ecx # 0x1f = 16 + 15 = 31; ? ecx >> 31
add    %ecx,%eax # eax <- ecx + eax
sar    %eax # eax <- eax / 2
# ecx <- rax + rsi * 1
lea    (%rax,%rsi,1),%ecx # ecx <- rax + rsi * 1 

# 不应跳转，即要ecx > edi
cmp    %edi,%ecx 
jle    0x400ff2 <func4+36> # false 失败

lea    -0x1(%rcx),%edx # edx <- ecx - 1
# 递归 6
callq  0x400fce <func4>

# 递归出口
add    %eax,%eax eax <- eax * 2
jmp    0x401007 <func4+57>

# 若ecx < edi 
mov    $0x0,%eax # eax = 0
cmp    %edi,%ecx 
# 若 ecx >= edi, return 0 
jge    0x401007 <func4+57>
 
lea    0x1(%rcx),%esi # esi <- rcx + 1
callq  0x400fce <func4> 
# 输出
lea    0x1(%rax,%rax,1),%eax  # eax <- 2 * eax + 1
# return
```

化为C语言分析，reg容易混乱

```c
// func4(input, 0, 15)
// eax = tmp 
int func4(int a, int b, int c) {
    int tmp = c;
    tmp -= b;
    int v = tmp;
    v = v >> 31;
    tmp += v;
    tmp = tmp >> 1;
    v = tmp + b;
    if (v <= a) jump nxt;
    c = v - 1;
    // ecx会在一开始就被覆盖，只是局部变量
    tmp = func4(a, b, c);
    return 2 * tmp;
    nxt:
    tmp = 0;
    if (v >= a) return tmp;
    
    b = v + 1;
    tmp = func4(a, b, c);
    return 2 * tmp + 1;
}

// 优化逻辑 a != 15
// 直接模拟 
int func4(int a, int b, int c) {
    int v;
    // 7
    int tmp = ((c - b) + (c - b) >> 31) / 2;
    v = tmp + b;
    if (v == a) return 0;
    // 2 * func4(1, 6, )
    if (v > a) return 2 * func4(a, b, v - 1);
    return 2 * func4(a, v + 1, c) + 1;
}

for (int i = 1; i <= 15; i++) {
    cout << func4(i, 0, 15) << endl;
}

// 综上 1 0；3 0；7 0 应该都可以
// 根据验证 确实
```

## bomb5

```bash
break *main+266
run a.txt
```

```assembly
# 栈的首地址
push   %rbx
sub    $0x20,%rsp
mov    %rdi,%rbx

# 段寻址判断溢出
mov    %fs:0x28,%rax
mov    %rax,0x18(%rsp)

# 长度为6
callq  40131b <string_length>
cmp    $0x6,%eax
je     4010d2 <phase_5+0x70>

# jump_1
mov    $0x0,%eax
jmp    40108b <phase_5+0x29>

# jump_2
# 此处rbx已经等于rdi即输入的地址 即第一个byte的0拓展，对照可知取的时第一个字符的ASCII码
movzbl (%rbx,%rax,1),%ecx
# 这里取ecx的第一个byte到rsp的地址 0x7fffffffdaa0
mov    %cl,(%rsp)
# 栈顶值为 0x402261 
# x/4x 0x7fffffffdaa0  0x61 0x22 0x40 0x00 同样看出小端序
mov    (%rsp),%rdx
# 15, mask, 保留末四位
and    $0xf,%edx
# 偏移
movzbl 0x4024b0(%rdx),%edx
# dl，也就是edx的最后值，作为参数，要对应flyers
mov    %dl,0x10(%rsp,%rax,1)
add    $0x1,%rax
cmp    $0x6,%rax
# 重复6次
jne    40108b <phase_5+0x29>

# 这里可知最后的结果时flyers
movb   $0x0,0x16(%rsp)
mov    $0x40245e,%esi
lea    0x10(%rsp),%rdi
callq  401338 <strings_not_equal>

# 需要返回eax=0，有ZF等于1
test   %eax,%eax
# je不能有溢出 ZF等于1时
je     4010d9 <phase_5+0x77>

# jump
mov    0x18(%rsp),%rax
# 确定栈没问题
xor    %fs:0x28,%rax
je     4010ee <phase_5+0x8c>
retq

# 根据以上可知，只要根据 x 0x4024b0 maduiersnfotvbylSo 拼出flyers即可
# 因为只保留末四位，即16进制的最后一位，因此，最后一位分别为 9 F E 5 6 7
# 对着表找到 9ON567
```

## bomb6

```bash
break *main+294
# 循环太长需要跳过 c
break *phase_6+95 
break *phase_6+123
break *phase_6+183
break *phase_6+222
run a.txt
```

```assembly
# push...
sub    $0x50,%rsp
# 栈顶
mov    %rsp,%r13
mov    %rsp,%rsi

# 存到了 r12 13 
callq  40145c <read_six_numbers>
mov    %rsp,%r14
mov    $0x0,%r12d

# 0x401114
# 可以看出比较的rbp下移了
mov    %r13,%rbp
mov    0x0(%r13),%eax
# 此时rsp r14 r13 rbp 
# eax = int_1

# int_1 <= 6 be below and equal 
sub    $0x1,%eax
cmp    $0x5,%eax
jbe    401128 <phase_6+0x34>
callq  0x40143a <explode_bomb>

# 401128 6次循环 
add    $0x1,%r12d
cmp    $0x6,%r12d
je     401153 <phase_6+0x5f>

# 401135
# ebx = 1第一次循环
mov    %r12d,%ebx
# eax = ebx (循环次数)
movslq %ebx,%rax
# eax = int_1 | 4byte，可以看出是int_1
mov    (%rsp,%rax,4),%eax
# 栈顶 int_1 != int_2 
cmp    %eax,0x0(%rbp)
jne    401145 <phase_6+0x51>
callq  40143a <explode_bomb>

# 401145
# ebx++; 可以看出，这里要求每个后序数字都不等于第一个数字
add    $0x1,%ebx
cmp    $0x5,%ebx
jle    401135 <phase_6+0x41>

# 继续循环 r13 + 4 下一个byte
add    $0x4,%r13
jmp    0x401114 <phase_6+32>

# 可以看出上面要求每个数字小于等于6，且各不相同 取 1 2 3 4 5 6

# 401153 
# 18即为24byte rsi为结束位
lea    0x18(%rsp),%rsi
# 保留栈顶 rax rsp
mov    %r14,%rax
# ecx = 7
mov    $0x7,%ecx

# 401160
# edx = 7
mov    %ecx,%edx
# edx -= int
sub    (%rax),%edx
# int_1 -= 7
mov    %edx,(%rax)
# rax += 4
add    $0x4,%rax
# 是否最后一个byte
cmp    %rsi,%rax
jne    401160 <phase_6+0x6c>

# 以上的目的是将每个数7-int 变为 6 5 4 3 2 1]

# 40116f
# r/esi = 0
mov    $0x0,%esi
jmp    401197 <phase_6+0xa3>

# *(rdx + 8) = rdx 正好等于rdx + 16, 这里一开始以为是直接赋值 + 16 。。。
mov    0x8(%rdx),%rdx
# int > 1, eax = 2
add    $0x1,%eax
cmp    %ecx,%eax
# int > 1, 若eax != ecx， 则重复
jne    401176 <phase_6+0x82>
# int > 1, 有此时ecx == eax == int 
jmp    401188 <phase_6+0x94>

# 401183
# 可以看出若int == 1, 则直接执行这一步
mov    $0x6032d0,%edx

# 401188
# *(rsp + 8 * id) = rdx
mov    %rdx,0x20(%rsp,%rsi,2)
# rsi += 4 可以看出留了8个byte
add    $0x4,%rsi
# 6个数字
cmp    $0x18,%rsi
je     4011ab <phase_6+0xb7> 

# 结束循环 跳转

# 401197
# ecx = int_1
mov    (%rsp,%rsi,1),%ecx
cmp    $0x1,%ecx
# 若ecx <= 1 401183
jle    401183 <phase_6+0x8f>
# 若ecx > 1
mov    $0x1,%eax
mov    $0x6032d0,%edx
jmp    401176 <phase_6+0x82>

# 可以看出，上面的函数就是把数字的偏置转移到了0x6032d0的偏置，并把对应的值按顺序存到了rsp70之后。 
# x/48x 0x7fffffffda70
0x7fffffffda70: 0x20    0x33    0x60    0x00    0x00    0x00    0x00    0x00
0x7fffffffda78: 0x10    0x33    0x60    0x00    0x00    0x00    0x00    0x00
0x7fffffffda80: 0x00    0x33    0x60    0x00    0x00    0x00    0x00    0x00
0x7fffffffda88: 0xf0    0x32    0x60    0x00    0x00    0x00    0x00    0x00
0x7fffffffda90: 0xe0    0x32    0x60    0x00    0x00    0x00    0x00    0x00
0x7fffffffda98: 0xd0    0x32    0x60    0x00    0x00    0x00    0x00    0x00

# 4011ab
# rbx = *(rsp + 20) = cv1
mov    0x20(%rsp),%rbx
# rax = rsp + 28
lea    0x28(%rsp),%rax
# rsi = end
lea    0x50(%rsp),%rsi
# rcx = rbx = cv
mov    %rbx, %rcx

# 4011bd
# rdx = *rax = cv_next
mov    (%rax),%rdx
# *(rcx + 8) = rdx；*(cv + 8) = cv_next
mov    %rdx,0x8(%rcx)
# rax += 8 指向cv_next
add    $0x8,%rax
# 是否结束
cmp    %rsi,%rax
je     4011d2 <phase_6+0xde>
# rcx = rdx
mov    %rdx,%rcx
# 继续循环
jmp    4011bd <phase_6+0xc9>

# 上面函数的含义在于 在cv + 8 存储 cv_next的信息
# x/64b 0x6032d8
# 6032e0是默认值 第一行的值

0x6032d8: 0xe0    0x32    0x60    0x00    0x00    0x00    0x00    0x00
0x6032e8: 0xd0    0x32    0x60    0x00    0x00    0x00    0x00    0x00
0x6032f8: 0xe0    0x32    0x60    0x00    0x00    0x00    0x00    0x00
0x603308: 0xf0    0x32    0x60    0x00    0x00    0x00    0x00    0x00
0x603318: 0x00    0x33    0x60    0x00    0x00    0x00    0x00    0x00
0x603328: 0x10    0x33    0x60    0x00    0x00    0x00    0x00    0x00

# 4011d2
# 将rdx的值清0
movq   $0x0,0x8(%rdx)
# ebp = 5
mov    $0x5,%ebp

# 4011df
# 此时rbx为cv1, 即 rax = *(cv1 + 8) = cv2
# 第五次 rax = *(cv5 + 8) = cv6
mov    0x8(%rbx),%rax
# eax = *cv2 = cv2' (！注意这里并没有 + 8)
mov    (%rax),%eax

cmp    %eax,(%rbx)
jge    4011ee <phase_6+0xfa>
callq  40143a <explode_bomb>

# 4011ee 
mov    0x8(%rbx),%rbx
sub    $0x1,%ebp
jne    4011df <phase_6+0xeb>

# 比较所有的数字，cv2 >= cv3, 即要满足递减，即 
# cv2' >= cv3'
# 实际比较的是未加8的值...
# 14c a8 39c 2b3 1dd 1bb
# id: 1  2  3  4  5  6
#  3 4 5 6 1 2
#  4 3 2 1 6 5
# Got it !! 
retq
```

# 收获

1. 当涉及复杂递归时，可以转换为C语言后优化代码，再通过枚举的方式求出符合条件的解（第四题）。

2. 当分支过多时，可以先将汇编代码分段，尝试一个简单的解，借助gdb，跑一下流程，枚举两三次特殊情况，渐渐就有了基本的思路（第六题）。且最好记忆各个参数的含义和上次更新的值，否则要不断回溯，时间较久。
3. 借助gdb可以节省分析一些没必要分析的函数的时间，类似于状态机的思想，只要知道返回后的寄存器状态，就大概函数的作用（很多负责输入输出的函数）。
4. 一般寄存器的值可能代表地址也可能代表值。另外，机器是64位小端序，注意可能有效位需要借助与mask做与操作取得，可能没有意义（第五题）。
5. 借助文档和教材了解x86指令集。注意由于bomb实验的普及性，很多由两条指令集组成的跳转指令大概率可以直接搜到，而实际状况往往需要自己分析各个寄存器的状态。当分支足够多的时候，若每个分支都要用3的思想，则需要2*分支数的时间，较为低效。 
6. 借助gdb显示格式，如字符串、char、16bit字符串，能够更快明白数据/地址的意义；tui模式更方便debug；多开终端，gdb与源码同时分析；直接打出大段地址，便于分析。
7. 一开始分不清地址还是数据，返回值和参数，不断对一些不相关的readline函数或标准库函数进行分析耗时较长。后面逐渐驾轻就熟，花费的时间则合理了不少。
8. 实验涉及的数值变换较少，一般都只涉及8bit以内的正数，实际大大简化了问题，把rdi、edi甚至di都可以看做是一个数，也更容易理解（虽然汇编代码都使用了很多考虑到有符号数，符号拓展的方式等的函数，实际由于实验的数据较弱，不需要考虑边界情况）。通过gdb不断追踪值也可以确认这种判断。
9. 每隔一段时间容易混淆16进制表示和10进制表示，尤其在计算地址距离时。
10. 汇编指令容易混淆mov对应的地址与值，a, b -> *b = *a，寄存器同理。区分立即数，reg直接，reg间接的写法。mov reg_1, reg_2 -> *reg_1 = *reg_2； mov reg_1, (reg_2) *reg_1 = **reg_2, 即把reg_1的值存到*reg_2上。容易把reg的值当成了地址。一般省略*，直接写成reg_1 = reg_2即可。而lea只做值的运算，mv采用取地址，两者也容易混淆。
