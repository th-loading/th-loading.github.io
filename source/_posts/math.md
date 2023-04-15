---
title: math
date: 2021-10-07 18:56:08
tags:
---

# matrix

## basic

### dot product


### transpose

$$
(AB)^T = B^TA^T
$$

如果结果为scaler(标量 $1\times1$),则转置等于自身

## regression

### BLUE 

best linear unbiased estimator (最佳线性无偏估计)

### OLS 

ordinary least square
$$
y = X \beta + \epsilon
$$

$$
\begin{bmatrix}
Y_1\\
Y_2\\
\vdots\\
\vdots\\
Y_n
\end{bmatrix}_{n\times1}= \begin{bmatrix}
1 & X_{11} & X_{12} & \dots & X_{1k}\\
1 & X_{21} & X_{22} & \dots & X_{2k}\\
\vdots & \vdots & \vdots & \dots & \vdots\\
\vdots & \vdots & \vdots & \dots & \vdots\\
1 & X_{n1} & X_{n2} & \dots & X_{nk}\\
\end{bmatrix}_{n \times k} \begin{bmatrix}
\beta_1\\
\beta_2\\
\vdots\\
\vdots\\
\beta_n
\end{bmatrix}_{k+1}+\begin{bmatrix}
\epsilon_1\\
\epsilon_2\\
\vdots\\
\vdots\\
\epsilon_n
\end{bmatrix}_{n\times 1}
$$
常数项 $\beta_1$
$$
RSS=e'e=\begin{bmatrix}
e_1 & e_2 & \dots & \dots & e_n
\end{bmatrix}_{1 \times n} \begin{bmatrix}
e_1 \\ e_2 \\ \vdots \\ \vdots \\ e_n
\end{bmatrix}_{n\times1}
$$

$$
\begin{align}
e'e &= (y-X\hat\beta)'(y-X\hat\beta)\\
&=y'y-\hat\beta'X'y-y'X\hat \beta + \hat \beta'X'X\hat \beta\\
&= y'y - 2\hat\beta'X'y + \hat \beta'X'X\hat \beta
\end{align}
$$

由于$\hat \beta'X'y$ 与 $y'X\hat \beta$ 都是scaler，转置为它本身。

## 矩阵求导

 $\frac{\partial X'\beta}{\partial \beta}=X'$

$\frac{\partial h'Vh}{\partial h'}=Vh$ （分别求偏导）
$$
\frac{\partial X\beta}{\partial \beta}= \frac{\partial \beta'X}{\partial \beta} =X\\
\frac{\partial e'e}{\partial \beta } = -2X'y + 2X'X\hat \beta = 0\\
\hat \beta = (X'X)^{-1}X'y
$$

### Assumption

the Gauss-Markov Assumptions

1. $y=X\beta+\epsilon$

   存在某种线性关系

2. X is an $n\times k$ matrix of full rank

   多重共线性 满秩举证

3. $E(\epsilon|X)=0$

4. $E(\epsilon\epsilon'|X)=\sigma^2I$

   homoscedasticity 同方差性 no autocorrelation 相关性

   方差为定值，0均值

5. X is unrelated to $\epsilon$

6. often: $\epsilon|X \sim N[0,\sigma^2I]$

### GLS

heteroscedasticity 异方差

transformation:

使得$P\Sigma$等价于$\epsilon$
$$
var(\epsilon\epsilon'|X) = \sigma^2\Omega\\
Py =PX\hat\beta +P\Sigma\\
P = \Omega^{\frac{1}{2}}
$$

WLS independent value
$$
\Omega_{WLS} = \begin{bmatrix}
w_{11}&0&\dots&0\\
0&w_{22}&\dots&\vdots\\
\vdots&\vdots&\ddots&\vdots\\
0&0&\dots&w_{nn}\\
\end{bmatrix}\\
$$
考虑covariance
$$
\quad\\
\Omega_{GLS} = \begin{bmatrix}
\sigma_{11}&\sigma_{12}&\dots&\sigma_{1n}\\
\sigma_{21}&\sigma_{22}&\dots&\vdots\\
\vdots&\vdots&\ddots&\vdots\\
\sigma_{n1}&\sigma_{n2}&\dots&\sigma_{nn}\\
\end{bmatrix}\\
$$

### ARMA

对残差再进行拟合 -> partial autocorrelation -> 残差与lag相关

### $R^2$

$$
R^2=\frac{\sum\limits^n_{i=0}(\hat y_i-\overline y)^2}{\sum\limits^n_{i=0}(y_i-\overline y)^2}=\frac{Y'P'TLPY}{Y'LY}=1-\frac{Y'MY}{Y'LY} =1-\frac{RSS}{TSS}
$$

TSS: total sum of squares
RSS: residual sum of squares

# 最优化

## Lagrange乘数

Lagrange multiplier
$$
\begin{align}
\max \quad& f(x,y)\\
s.t.\quad&g(x,y)=0
\end{align}
$$

$$
\mathcal{L}(x,y,\lambda)=f(x,y)-\lambda g(x,y)
$$

$$
\bigtriangledown_{x,y,\lambda}\mathcal{L}(x,y,\lambda)=0\\
$$

其中$\bigtriangledown_{x,y,\lambda}\mathcal{L}(x,y,z)$表示函数分别对$x,y,z$取偏导，

### intuition

$$
\begin{cases}
\bigtriangledown f(x,y)=\lambda \bigtriangledown g(x,y)\\
g(x,y)=0
\end{cases}
$$

$g(x,y)$的自由度为1，可视为曲线，而与$f(x,y)$等高线相切的位置，就是函数的一个极值（相交则有多个点）
其中梯度代表了与等高线（降维）垂直的矢量，所以当梯度平行时$\bigtriangledown f(x,y)=\lambda \bigtriangledown g(x,y)$可取到极值。

# 统计

## describe

### skew


### kurtosis

heavy tails and outliers(离群值) -> 常用于黑天鹅事件


power law distribution $x^{-\alpha}$ 均值并不会随样本数的增多而收敛（不满足大数定律）long tail 28定律


## basic

### rvs

Random variates

### 确定参数

通过 maximum likelihood

### normal 

接近样本数极多的二项分布，应用较广，模拟了现实多因素影响（数量极多的二项分布）最终往往趋于正态分布，且互相之间不存在相关性，但正态分布的收敛较快，且金融数据之间相关性较强，不适用于正态分布，数量级为 $e^{-x^2}$

## random walk

### 简单随机游走

simple random walk
$$
Z_i=
\begin{cases}
1 &p=\frac{1}{2}\\
-1&p=\frac{1}{2} 
\end{cases}
$$

$$
S_n = \sum\limits_{j=1}^nZ_i
$$

$$
E(S_n)=0 
$$

$$
\sigma^2 = E(S_n^2) = \sum\limits_{i=1}^nE(Z_i^2)+2\sum\limits_{i=1}^n\sum\limits_{j=1}^nE(Z_iZ_j)=n
$$

$$
\lim\limits_{n \rightarrow\infty}\frac{E(|S_n|)}{\sqrt{n}} = \sqrt{\frac{2}{\pi}}
$$

### Wiener process

$$
\Delta W = \varepsilon_t\sqrt{\Delta t}
$$

取 $\sqrt{\Delta t}$ 的原因：收敛较慢，可以体现锯齿状（jagged）不会出现frozen，和无限大。
$$
\varepsilon_t \sim N(0,1)
$$

$$
E(\Delta W_t^2) = (\sqrt{\Delta t})^2E(\varepsilon^2) = \Delta t
$$

$$
W_T=(\varepsilon_0+\varepsilon_{\Delta_t}+\cdots+\varepsilon_{T-\Delta_t})\sqrt{\Delta t}
$$

$$
E(W_T^2) =n\Delta t = T
$$

$$
W_T\sim N(0,T)
$$

$$
W_{t_2}- W_{t_1} \sim N(0,t_2-t_1)
$$

## test

### t-test

$$
\frac{\overline x-\mu}{s/\sqrt{n}}\sim t(n-1)
$$

自由度与sample个数有关，sample越多越接近正态分布，由于heavy tail常用于金融数据，skew-student可以完善。

置信区间
$$
m\pm t \frac{d}{\sqrt{n}}
$$


## Bayes

### 后验

posterior distribution 
$$
L(\theta|x)\sim Bin(n,p)=\theta ^k(1-\theta)^{n-k}
$$
$L(\theta|x)$为似然估计 likelihood
$$
p(\theta) \sim \beta(a,b)=\frac{\Gamma(a+b)}{\Gamma(a)\Gamma(b)}\theta^{a-1}(1-\theta)^{b-1}
$$
$p(\theta)$为 prior 随着观察次数的改变而改变，a、b 为观察正/反面的情况
$$
\begin{align}
p(\theta|x)&=\frac{L(\theta|x)p(\theta)}{\int^1_0 L(\theta|x)p(\theta)d\theta}\\
&= \frac{\Gamma(a+b+n)}{\Gamma(a+k)\Gamma(b+n-k)}\theta^{a+k-1}(1-\theta)^{b+n-k+1}
\end{align}
$$

$p(\theta|x)$即 posterior distribution

