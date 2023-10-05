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

## Const Object

借助const的操作符重载可以提供const对象的接口

bitwise constness 不可改变对象内任何non-static对象 (可借助指针绕过编译器，不会有二进制级别的检测，消耗过大) 

logical constness 可借助mutable。

```c++
#include <iostream>
#include <vector>
#include <cstring>

using namespace std;

class Base {
private:
public:
    char* a;
    vector<string> b;
    string c;
    Base(){
        b.push_back("abc");
        a = (char *) malloc(sizeof(char) * 6);
        strcpy(a, "123");
    }
    // const 成员函数
    const string& operator[] (size_t pos) const {
        return b[pos];
    }
};

int main() {
    const Base a = Base();
    // 确保了 *v 的值不会被改变
    // 指针的类型经过封装后也有了限制
    vector<string>::const_iterator v = a.b.begin();
    // C 并没有措施
    char *t = a.a;
    *t = 'b';
    // cout << a.a << endl; 成功改变
    
    // 只要得到具体的指针，就可以改变对应值
    string *d = (string *)&a.b[0];
    cout << *d << endl;
    (*d)[0] = 'g';
    cout << *d << endl;

    // 类似的
    string *q = (string *)&a[0];
    (*q)[0] = 'p';
    cout << *q << endl;
    

    const string g = "123";
    // 并不会检查违法的类型转换，iterator会
    string *kk = (string *)&g;
    (*kk)[0] = '3';
    cout << g << endl;
        
    // cout << *p << endl;
    char *p = (char *)&a.b[0];
    for (int i = 0; i < 20; i++) {
        //  逐个bit找到对应位置
        if (*p == 'p') *p = 'a';
        p++;
    }
    // cout << typeid(p).name() << endl;
    // cout << p << endl;
    // p[0] = '2';
    cout << a.b[0] << endl;
    
    // 同理，强制类型转换即可
    const char gg[100] = "ggg";
    cout << gg << endl;
    *(char *)gg = 'a';
    cout << gg << endl;
}
```

