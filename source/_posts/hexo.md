---
title: Hexo配置
date: 2021-10-07 22:05:38
tags: Hexo
---
# Hexo

## 下载与部署(win10)

### 步骤

下载git -> 打开git bash -> 利用官网指令下载并初始化hexo

### 概念

1. 通过git bash在win10代替cmd作为终端。
2. npm是node.js的包管理工具
3. win10的环境变量是程序运行的默认路径，按照顺序找运行命令对应的程序

### 注意事项

1. 注意环境变量的设置

   - 将git加入环境变量
   - 将npm对应bin文件的位置加入环境变量
   - 配置完重启终端

2. 默认情况下，npm和Node一起装在`C:\Program Files (x86)\nodejs`，以下简称`%Program%`；
   而包括npm自己和他全局安装的包（cnpm..etc）是装在另一个user-specific路径的`C:\Users\<username>\AppData\Roaming\npm`，以下简称`%Appdata%`
   因为在环境变量中，安装程序把`%Program%`放在`%Appdata% `前面，他会一直使用和node装一起的npm，而不是你安装的`npm -g install npm@<version>`。(改变顺序后需要重启)

   参考网址:https://segmentfault.com/a/1190000014073800

3. 注意版本（同时确认安装成功）

   - 注意更新git
   - 包管理工具npm的版本更新
   - hexo与node.js的版本是否对应
     - node.js 版本太高，需降至 13 或 12 即可解決

4. 注意插件

   - 如果开启了字数统计，应当安装一下`hexo-wordcount`
   - typora npm install hexo-asset-image


### 常用指令

```bash
# 更新git 否则ctrl无反应
git update-git-for-windows
# 设置代理
npm config set proxy http://127.0.0.1:41091
npm config set https-proxy http://127.0.0.1:41091
# 确认版本
npm -v
# 更新
npm install npm@latest -g
npm install -g npm@6
# check package
npm config get package-lock
npm config set package-lock
npm list -g --depth 0
# 删除
npm rm hexo-cli -g
# 下载
npm install -g hexo-cli
# 确认安装成功
hexo -v
# 初始化
hexo init <folder>
```

## 与远程库进行绑定

### 步骤

在_config配置deploy -> 在source中设置CNAME(custom domain) -> hexo deploy(设置branch,可以为master)

## 使用

```bash
# 创建一个blog
hexo new "project"
# 生成
hexo g
# 本地服务器
hexo s
# 清理
hexo clean
# 上传
hexo deploy
```
