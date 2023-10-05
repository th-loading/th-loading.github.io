---
title: CS:APP Malloc Lab记录 date: 2023-07-12 23:29:21
tags: CS 
---

## 前置知识

### 内存对齐

从Cache和内存的读写方式可以看出，内存采用

参考CPU读取内存的方式，

### 常见分配方式

MMU处理虚拟内存借助页表映射，而对于C语言而言，malloc得到的堆中的虚拟内存，需要连续的虚拟空间。

借助内置malloc申请一大块空间，就可以模拟这个过程。

有多种数据。

1. 每一块包括前缀、后缀，顺序访问
2. 双向链表
3. 分块 + 二进制分块
4. 特别的系统，只存在2^i的对象，可以不断二分分配空间。

## 双向链表
### 基本思路
将空闲块通过双向链表组织，双向链表可以O(1)调整，可以从逻辑上排序链表，而不基于物理空间的遍历。

### 细节处理
1. 确保每个块的开头Alignment
2. 需要增加LOG系统，便于调试链表出问题的位置
3. 可以借助链接等方式，优先调用mymalloc，用于对比mymalloc和标准库的性能。DLL - MAP .data .plt Call - 物理地址

### Code
```c++
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>
#include <string.h>

/* single word (4) or double word (8) alignment */
#define ALIGNMENT 8

// malloc所需的数据结构
#define HEADER (sizeof(size_t))
#define FOOTER (sizeof(size_t))
// 两个指针
#define EXTRA (2*sizeof(void*))
#define FILL (ALIGN(HEADER + EXTRA))

/* rounds up to the nearest multiple of ALIGNMENT */
#define ALIGN(size) (((size) + (ALIGNMENT-1)) & ~0x7)

#define SIZE_T_SIZE (ALIGN(sizeof(size_t)))

#define MAX(x, y) ((x) > (y)? (x) : (y))
#define GET(p) (*(size_t *)(p))
#define GET_P(p) (*(void **)(p))
#define GET_SIZE(p) (GET(p) & ~0x7)
#define GET_ALLOC(p) (GET(p) & 0x1)
#define GET_PREV(p) (GET_P(p + HEADER))
#define GET_NEXT(p) (GET_P(p + HEADER + sizeof(void*)))

#define SET(p) (*(size_t*)(p) = (GET(p) | 1))
#define PUT(p, val) (*(size_t *)(p) = (val))
#define PUT_F(p, val) (*(size_t *)(p + val - FOOTER) = (val))
#define PUT_P(p, val) (*(void **)(p) = (val))
#define PUT_PREV(p, val) (PUT_P(p + HEADER, val))
#define PUT_NEXT(p, val) (PUT_P(p + HEADER + sizeof(void*), val))
#define FULL_SIZE(content) (ALIGN(FILL + content + FOOTER))
#define SPACE(sz) (sz - FILL - FOOTER)

void del_p(void *p);

static void *START, *END;
static void *FP = NULL;

void set_blk(void *p, size_t sz) {
    PUT(p, sz);
    PUT_F(p, sz);
}

void insert_head(void *p) {
    // printf("insert: %x\n", (uintptr_t)p);
    PUT_PREV(p, NULL);
    if (FP == NULL) {
        FP = p;
        PUT_NEXT(p, NULL);
    }
    else {
        PUT_NEXT(p, FP);
        PUT_PREV(FP, p);
        FP = p;
    }
}

/* 
 * mm_init - initialize the malloc package.
 */
void printlist(void) {
    printf("FREE LIST\n");
    void *cur = FP;
    int cnt = 0;
    while (cur) {
        void *nxt = GET_NEXT(cur);
        int sz = GET_SIZE(cur);
        int al = GET_ALLOC(cur);
        int sp = SPACE(sz);
        printf("pointer: %x, size: %x, space: %x, alloc: %x\n", (uintptr_t)cur, sz, sp, al);
        cur = nxt;
        cnt++;
        if (cnt > 10) {
            printf("ERROR\n");
            exit(0);
        }
    }
}

void printlog(void) {
    printf("log START: %x, END: %x\n", (uintptr_t)START, (uintptr_t)END);
    void *cur = START;
    while (cur < END) {
        int sz = GET_SIZE(cur);
        int al = GET_ALLOC(cur);
        int sp = SPACE(sz);
        printf("pointer: %x, size: %x, space: %x, alloc: %x\n", (uintptr_t)cur, sz, sp, al);
        cur += sz;
    }
    printlist();
    printf("END\n");
}

int mm_init(void) {
    // printf("init\n");
    mem_deinit();
    mem_init();
    // 初始化数据结构
    // 确保初始化
    START = (void*)(ALIGN((uintptr_t)mem_heap_lo()));
    END = START;
    FP = NULL;
    mem_sbrk(START - mem_heap_lo());
    return 0;
}

void *mm_malloc(size_t size) {
    // printf("MALLOC: %x\n", size);
    // 确保开始时ALIGN的
    // 隐含p也是ALIGN的
    // 增加同样是ALIGN的 
    void *tmp = FP;
    while (tmp) {
        void *nxt = GET_NEXT(tmp);
        size_t sz = GET_SIZE(tmp);
        if (SPACE(sz) >= size) {
            // 移除队列
            del_p(tmp);
            size_t tar = FULL_SIZE(size);
            if (sz - tar >= FULL_SIZE(ALIGNMENT)) {
                set_blk(tmp, tar);
                set_blk(tmp + tar, sz - tar);
                insert_head(tmp + tar);
            }
            SET(tmp);
            // printlog(); 
            return tmp + FILL;
        }
        tmp = nxt;
    }
    size_t sz = FULL_SIZE(ALIGN(size));
    mem_sbrk(sz);
    set_blk(END, sz);
    SET(END);
    END += sz;
    // printlog();
    return END - sz + FILL;
}

void del_p(void *p) {
    // printf("del: %x\n", (uintptr_t)p);
    void *prev = GET_PREV(p);
    void *nxt = GET_NEXT(p);
    if (prev == NULL && nxt == NULL) {
        FP = NULL;
        return;
    }
    if (prev == NULL) {
        FP = nxt; 
        PUT_PREV(FP, NULL);
        return;
    } 
    if (nxt == NULL) {
        PUT_NEXT(prev, NULL);
        return;
    }
    PUT_NEXT(prev, nxt);
    PUT_PREV(nxt, prev);
    return;
}

// 只维护链表结构
void combine(void *p1, void *p2) {
    size_t sz = GET_SIZE(p1) + GET_SIZE(p2);
    del_p(p1); 
    del_p(p2);
    set_blk(p1, sz);
    insert_head(p1);
}

void mm_free(void *ptr) {
    void *head = ptr - FILL;
    // printf("free: %x\n",(uintptr_t)head); 
    void *cur = head;
    void *nxt = head + GET_SIZE(head);
    // combine的时候用到的信息在这里被覆盖了
    PUT(head, GET_SIZE(head));
    insert_head(head);
    if (head > START) {
        void *last = head - GET_SIZE(head - FOOTER);
        if (!GET_ALLOC(last)) {
            combine(last, cur);
            cur = last;
        }
    }
    if (nxt < END) {
        if (!GET_ALLOC(nxt)) {
            combine(cur, nxt);
        }
    }
    // printlog();
}

void *mm_realloc(void *ptr, size_t size)
{
    void *oldptr = ptr;
    void *newptr;
    size_t copySize;
    
    newptr = mm_malloc(size);
    if (newptr == NULL)
      return NULL;
    // 根据保存的大小信息
    copySize = (size_t)SPACE(ptr);
    if (size < copySize)
      copySize = size;
    memcpy(newptr, oldptr, copySize);
    mm_free(oldptr);
    return newptr;
}
```
### Result  
```
Team Name:ateam
Member 1 :Harry Bovik:bovik@cs.cmu.edu
Using default tracefiles in ../traces/
Perf index = 44 (util) + 9 (thru) = 53/100
```

## 小结

### 满分思路


