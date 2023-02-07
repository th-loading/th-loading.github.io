---
title: Git基础
date: 2023-02-07 18:27:02 
tags: Git
---

# Start

## 基本结构

Working Directory当前使用的branch，与Repo区分，更新比对操作都要指定Repo中的一个Branch进行。

<img src="/images/git.png" alt="图来源于网络,侵删" style="zoom: 50%;"  />

其中Repo中保存了多个branch的版本信息，可以任意切换到Working Directory.

<img src="/images/branch.png" alt="图来源于网络,侵删"  style="zoom: 50%;" />

[image source](https://medium.com/@saicharanadurthi/demystifying-git-stash-basic-workflow-in-the-four-areas-f2192b5e509c) 可以借助stash暂存一部分内容

<img src="/images/git_work_flow.png" style="zoom: 67%;" />

## 注意事项

注意每次使用前先同步，否则可能出现冲突。

## 基本命令

```bash 
# set .gitconfig [user]
# 查看状态
git status
# 查看提交的commit
git log  
git log --pretty=oneline

# 设置代理 也可以直接设置环境变量
git config --global http.proxy http://proxyUsername:proxyPassword@proxy.server.com:port
git config --global --get-regexp http.*
git config --global --unset http.proxy
git config --global --unset http.https://domain.com.proxy
```

# 初始化

标志在于.git文件的生成

```bash
# 复制他人的网址 https://...
git clone  
# 在自己的文件夹下生成 默认的主干main
git init   
# 选择自己的主干的名字
git init -b defualt_branch 
```

# 缓存区管理

## 提交修改

```bash
# cur -> stage 
git add . 
# stage -> repo
git commit -m "log"  
```

## 撤销修改

```bash
# 默认从HEAD去更新
# 撤销unstaged 还未add
git restore [file]
# 撤销stage中的改变 已经add
git reset [file]
git checkout -- test.txt
```

# 分支管理

```bash
# 创建branch
git checkout -b [name]
# 删除
git branch -d
# 合并分支
git merge  
```

# 版本管理

## 比较文件

可以设置--diff-algorithm选择不同的比较方式，一般修改的代码都易于查重。

```bash
# git log 查看后用commit_id比较也可以

# 语法问题 git diff master bug/pr-1 == git diff master..bug/pr-1
# 工作区 (current directory) 与 版本库(HEAD of branch)中最新文件的比较 HEAD
git diff HEAD [file]
# 查看暂存区与版本库(HEAD) 
git diff --staged [file]
# 当前分支(HEAD of branch) 与上一个版本的变化 (@ is an alias for HEAD) (~3 = ^^^ = 回退三个版本)
git diff HEAD^ HEAD
# 与远程库比较 origin一般指代远程库 /main 代表分支
check diff HEAD..origin/main
```

```c++
// 也可以理解成"-"只来自与第一个文件，"+"只来自于第二个文件
'+' -- A line was added here to the first file.
'-' -- A line was removed here from the first file.

// 例子
// 第1个文件展示了8行(10-2)，从第1行开始，第2文件展示了9行(10-1)，从第1行开始

@@ -1,8 +1,9 @@ 
1 #include "cache.h"
2 #include "walker.h"
3
4 -int cmd_http_fetch(int argc, const char **argv, const char *prefix)
5 +int main(int argc, const char **argv)
6  {
7 +       const char *prefix;
8         struct walker *walker;
9         int commits_on_stdin = 0;
10        int commits;
```

## 标签

```bash
# tag/snapshot 指向一个commit(release)

git tag v1.0
git tag v0.9 f52c633
git show v0.9
git tag -d v0.1

git push origin --tags
git tag -d v0.9
```

# 远程管理

```bash
# 先在网页端初始化一个库
# 也可以下载gh
gh auth login  
git remtedeote add origin https://github.com/USER/REPO.git
# 查看情况
git remote -v
git remote rm origin
# 借助PAT(Personal Access Token)连接已有的库 
# git clone = git fetch + git checkout
git clone https://pat@github.com/<account>/<repo>.git
# 上传与更新
git pull branch origin(br)
git push branch origin

# 下载特定的版本 下载完checkout

```

创建branch而非直接合并 refs/remotes/remote-repo，fetch和clone

```bash
git remote add coworkers_repo git@bitbucket.org:coworker/coworkers_repo.git
git fetch coworkers_repo coworkers/feature_branch
fetching coworkers/feature_branch
git checkout coworkers/feature_branch
```

# 文件设置

.gitignore 不同步的后缀

```
# Windows:
Thumbs.db
ehthumbs.db
Desktop.ini

# Python:
*.py[cod]
*.so
*.egg
*.egg-info
dist
build
```

