---
title: Project coding style
date: 2023-10-24 13:20:42 
tags: CS
---

## Python

### Github

commit -m "Update .gitignore"

```
posts/
*.in
__pycache__/
storage/
.vscode/
```

### 命名标准

class 首字母大写，没有下划线

package_name、module_name、function_name、variable_name都可以用下划线

一般函数 do_sth的结构

### 结构

```
// 小型项目

my_project/
├── main.py
├── modules/
│   ├── module1.py
│   ├── module2.py
├── utils/
│   ├── utility1.py

// 引入package
my_project/
├── main.py
├── my_package/
│   ├── __init__.py
│   ├── module1.py
│   ├── module2.py
├── another_package/
│   ├── __init__.py
│   ├── module3.py
```

拆分module的逻辑 

```
my_project/
├── main.py
├── Agent
|   ├── agent.py

单个类，所有需要的存储结构和函数都能通过self

my_project/
├── main.py
├── Agent
|	├── a.py
| 	| 	├── class A 
| 	| 	| 	├── data a
| 	| 	| 	├── get and save data a
| 	| 	| 	├── interface to generate data b
|	├── b.py
| 	| 	├── class B 
| 	| 	| 	├── data b (get Class A)
| 	| 	| 	├── get and save data b
| 	| 	| 	├── interfaces
|   ├── agent.py
| 	| 	├── class Agent 
| 	| 	| 	├── class A -> B
| 	| 	| 	├── interfaces to other modules.

基于类定义的接口，需要输入的参数可以用self引用，但函数的可复用性变差。
接口全定义在一起，代码量大，参数过多。考虑根据接口拆分模块。

my_project/
├── main.py
├── Agent
|	├── Storage
| 	| 	├── class A 
| 	| 	| 	├── data a
| 	| 	| 	├── how to get data a
| 	| 	| 	├── interface to generate data b
| 	| 	├── class B (class A as input)
| 	| 	| 	├── data b 
| 	| 	| 	├── how to get data b  
| 	| 	├── class C
| 	| 	| 	├── class A -> B
|   ├── Action/Utils
| 	| 	├── Class D (class C as input)
| 	| 	| 	├── functions and coefficients
| 	| 	├── Class E (Interface 0) (class C as input)
| 	| 	|	├── Class D
| 	| 	|	├── functions and coefficients 
| 	| 	├── Class F (Interface 1) (class C as input)
| 	| 	|	├── Class D
| 	| 	|	├── functions and coefficients 
| 	├── agent
| 	| 	├── Class C —> Class E, F
| 	| 	├── Interfaces for other modules.

首先确认接口之间的依赖关系，之后定义各个接口需要的输入参数，借助一个大类涵盖所有的输入参数较为省事。
```

### 规范

尽量让每个函数处在相同的逻辑层次。

定义函数时标注类名，func(a: class_name)，方便代码补全。

