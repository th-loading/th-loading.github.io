---
title: CS:APP Cache Lab记录
date: 2023-06-27 14:58:08 
tags: CS
---



# 前置知识

## 多级缓存

本质是基于代码运行时的时间局部性与空间局部性，往往顺序取指令，顺序访问内存中的元素，一段时间内选择的内存区域也往往相同。

# 具体流程

## Part A

<img src="/images/cache-1.png" alt="cache结构" style="zoom:50%;"/>

在c语言的文件中模拟出以上结构的二级缓存。该实验只模拟数据Cache，因此忽视I开头的请求，只需要考虑L load，读取数据；S store 存储数据；M modify load 后 store。

### 提取参数

需要有两个可选择的功能，四个必要的参数。若缺少参数时需要打印Usage、option，只要含有-h 只打印帮助。

```c
// Get_opt API 处理不同参数的情况
// 注意if处理的先后对命令行的影响
// 比如在最后加入一个多余的参数，尽管其他条件都符合 都不会执行

//	if there exists -h
	// "Usage" 
	// return 0 

//	if there dosen't exist four valid mandatory parameters 
// 	? 缺少定义 重复定义 出现不合规的定义 -> 借助Get_opt处理  
	// "./csim: Missing required command line argument"
	// "Usage"
	// return 0  

//  if there exist invalid option
//	存在多余的参数
	// "./csim: invalid option -- 'f'" (order of apperance in command line)
	// "Usage" 
	// return 0	

//	if file not found
	// "traces/yi.trac: No such file or directory"
	// return 0
```

```c
// c函数中处理输入的参数

// argc 参数的多少 至少非负

// 可以是**argv *argv[] 字符串数组
// ./main a b c
// argv[0] = ./main (相当于对命令行做拆分)

#include <unistd.h> 
int main(int argc, char *argv[]) {
	// getopt(int argc, char *const argv[], const char *optstring)
    // : required argument :: optional
    // 默认会进行排序，使得需要的参数在前面
    int arg, verbose = 0;
    int S, s = -1, E = -1, B, b = -1;
    char *path = NULL;
    FILE *fp;    
    // C 打开文件并处理输入k
    // crefsim 没有做边界保护 "-1" 就会死循环
    // getopt 并不会强制判断哪些参数一定要存在    
    while((opt = getopt(argc, argv, “:if:lrx”)) != -1) {
        switch (arg) {
            case 'h':
                OutputUsage();                
                return 0;
                break;
            case 'v':
                verbose = 1;
                break;
            case 's':
                s = atoi(optarg);
                break;
            case 'E':
                E = atoi(optarg);
                break; 
            case 'b':
                b = atoi(optarg);
                break;
            case 't':
                // printf("%d\n", optind);
                path = argv[optind - 1];
                break;
            case ':':
                printf("%s: Missing required command line argument\n", argv[0]);
                OutputUsage();
                return 0;
                break;
            default:
                printf("%s: invalid option -- '%c'\n", argv[0], optopt);
                OutputUsage();
                return 0;
                break;
        }		   
    }
    if (s <= 0 || E <= 0 || b <= 0 || path == NULL) {
        printf("%s: Missing required command line argument\n", argv[0]);
        OutputUsage();
        return 0;
    }    
    fp = fopen(path, "r");
    if (!fp) {
        printf("%s: No such file or directory\n", path); 
        return 0;
    }
}
```

