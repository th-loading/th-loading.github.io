---
title: CS143 Compiler
date: 2023-07-20 16:20:04 
tags: CS
---

## 前置知识

Interpreter 解释器：程序与数据 输出output 在线 (script) 速度更慢

Compiler 编译器：Program -> C -> exec (+ data) -> output 离线

Formulas translation - Fortran

### Linking 链接
```c
// .out .o .elf 都属于可链接文件 不同格式对应的elf文件结构也有区别
extern int foo;
int func() {
    return foo;
}

// readelf --relocs ./a.o
// Relocation section '.rel.text' at offset 0x2dc contains 1 entries:
// Offset     Info    Type            Sym.Value  Sym. Name
// 00000004  00000801 R_386_32        00000000   foo

// .rel decides the localtion of variable 
// objdump --disassembly ./a.out
// 3:    a1 
// 4: 00 00 00 00         mov    0x0,%eax

// readelf --headers /bin/ls
// [...]
// ELF Header:
// [...]
//   Entry point address:               0x8049bb0

// Program Headers:
// 生成sections
//   Type           Offset   VirtAddr   PhysAddr   FileSiz MemSiz  Flg Align
// [...]
//   LOAD           0x000000 0x08048000 0x08048000 0x16f88 0x16f88 R E 0x1000
//   LOAD           0x016f88 0x0805ff88 0x0805ff88 0x01543 0x01543 RW  0x1000

// 整体的地址空间的映射，因此原来的基于RIP偏移的代码仍然可以复用 
// RIP不能直接获得，可以借助函数调用的栈顶间接获得

// 链接时需要预留代码空间，建立符号链接，便于动态加载器处理
// 

```

