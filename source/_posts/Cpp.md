---
title: Effective C++
date: 2023-09-19 20:14:53 
tags: CS
---

## Temporary Object

运算符重载后，不改变运算的顺序 

```c++
#include <iostream>
#include <string>
#include <vector>

using namespace std;

class Node {
    public:
        int a;
    	// 增加一些复杂的结构
        vector<string> b;
        string c;
    Node() {}
    Node(int a): a(a) {}
};

Node operator+(const Node &a, const Node &b) {
    Node c;
    c.a = a.a + b.a;
    // cout << "Execute :";
    return c;
}

int main() {
    Node a, b, c, d, e;
    a.a = 1;
    b.a = 2;
    c.a = 3;
    d.a = 4;
    // (a + b) -> a.operator+(b)
    // 根据运算的顺序 从后往前，并没有递归 编译器处理了这个过程
    e = a + (b + (c + d));
}
```

汇编代码分析

```assembly
// g++ -g b.cpp 
// layout split, s si n ni

// g++ -O0 -S b.cpp

// main
// 存储Node数据
main:
    movl	$1, -528(%rbp)
    movl	$2, -464(%rbp)
    movl	$3, -400(%rbp)
    movl	$4, -336(%rbp)
    
    leaq	-208(%rbp), %rax
    leaq	-336(%rbp), %rdx
    leaq	-400(%rbp), %rcx
    movq	%rcx, %rsi
    // 第一个参数用来存储 temporary object在当前main函数（而不是重载后的add函数）
    movq	%rax, %rdi
    // 调用重载
    call	_ZplRK4NodeS1_
    leaq	-144(%rbp), %rax
    leaq	-208(%rbp), %rdx
    leaq	-464(%rbp), %rcx
    movq	%rcx, %rsi
    movq	%rax, %rdi
    call	_ZplRK4NodeS1_

_ZplRK4NodeS1_:
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	%rax, %rdi
	// 在对应地址创建node
	call	_ZN4NodeC1Ev
	// 运算结果
	addl	%eax, %edx
	
	// 把结果存入对应的位置
	movq	-8(%rbp), %rax
	movl	%edx, (%rax)
	
```

实际上等价于栈中的变量，可能在表达式结束后被覆盖

重载运算符的返回变量一般需要加 const，因为没有实际的符号(symbol) ，且函数不能通过 & 调用（编译器会报错），但可以通过 const & 调用。

```c++
Node operator+(const Node &a, Node &b) {
    Node c;
    c.a = a.a + b.a;
    // cout << "Execute :";
    return c;
}

int main() {
    Node a, b, c, d, e;
    a.a = 1;
    b.a = 2;
    c.a = 3;
    d.a = 4;
	// Invalid operands to binary expression ('Node' and 'Node') (clangtypecheck_invalid_operands) 
    e = a + (b + (c + d));
}

// 返回是局部变量的引用, 并不是temporary object，且不同于指针，是调用函数栈的指针。
Node& operator+(const Node &a, const Node &b) {
    Node c;
    c.a = a.a + b.a;
    // cout << "Execute :";
    return c;
}
```