---
title: "多元函数微分学五题精讲"
date: 2026-08-09T20:00:00+08:00
draft: false
tags: ["数学", "高数"]
categories: ["学习笔记"]
math: true
---

## 一、连续性判定：放缩 + 夹逼（习题 7.1.3(3)）

### 题目

设

$$z=\begin{cases}\dfrac{\sin(x^3+y^3)}{x^2+y^2}, & x^2+y^2\neq 0\\[4pt] 0, & x^2+y^2=0\end{cases}$$

讨论 $z$ 在原点 $(0,0)$ 处是否连续。

### 思路

分段函数在分段点处讨论连续性，就是验证：当 $(x,y)\to(0,0)$ 时，$z(x,y)$ 的极限是否等于 $z(0,0)=0$。

看到形如 $\dfrac{\sin(\text{小量})}{\text{更小量}}$ 的结构，标准动作是：

1. 用 $|\sin t|\le|t|$ 把分子的三角函数去掉；
2. 用三角不等式把绝对值拆开；
3. 引入 $\rho=\sqrt{x^2+y^2}$，把每个绝对值项都统一归到 $\rho$；
4. 用夹逼定理得极限。

### 详细推导

第一步，用 $|\sin t|\le |t|$：

$$\left|\frac{\sin(x^3+y^3)}{x^2+y^2}\right|\le\frac{|x^3+y^3|}{x^2+y^2}$$

第二步，用三角不等式 $|A+B|\le|A|+|B|$：

$$|x^3+y^3|\le|x|^3+|y|^3$$

第三步，引入 $\rho=\sqrt{x^2+y^2}$，有 $|x|\le\rho$，$|y|\le\rho$，所以

$$|x|^3\le\rho^3,\quad |y|^3\le\rho^3$$

第四步，把所有项归到 $\rho$：

$$0\le\frac{|x|^3+|y|^3}{x^2+y^2}\le\frac{2\rho^3}{\rho^2}=2\rho$$

当 $(x,y)\to(0,0)$ 时 $\rho\to 0$，于是 $2\rho\to 0$。

由夹逼定理：

$$\lim_{(x,y)\to(0,0)}\frac{\sin(x^3+y^3)}{x^2+y^2}=0=z(0,0)$$

故 $z$ 在原点处连续。

### 小结

关键技巧是「统一量纲」：分子里出现了三次方 $x^3+y^3$，分母是二次方 $x^2+y^2$，两者次方不一致，必须用一个公共尺度 $\rho$ 统一起来。一旦都归到 $\rho$ 上，比较谁消失得更快就一目了然了。

---

## 二、混合偏导不等：定义法处理分段（习题 7.2.9）

### 题目

设

$$f(x,y)=\begin{cases}\dfrac{xy(x^2-y^2)}{x^2+y^2}, & x^2+y^2\neq 0\\[4pt] 0, & x^2+y^2=0\end{cases}$$

求 $f'_x(0,y)$ 与 $f'_y(x,0)$，并证明 $f''_{xy}(0,0)\neq f''_{yx}(0,0)$。

### 思路

分段函数在原点附近的偏导必须用定义求，不能直接套商法则：原点的邻域里既有点使 $f$ 走分式段、也有原点本身走常数段，必须按定义做。

具体做法是：

1. 先求一阶偏导 $f'_x(0,y)$：固定 $y$，让 $x$ 沿 $x$ 轴趋向原点；
2. 再求 $f'_y(x,0)$：固定 $x$，让 $y$ 沿 $y$ 轴趋向原点；
3. 在得到的一元函数上继续求导。

### 第一步：求 $f'_x(0,y)$

按偏导数定义：

$$f'_x(0,y)=\lim_{h\to 0}\frac{f(h,y)-f(0,y)}{h}$$

分两种情况讨论。

**情况 A：$y\neq 0$**。这时只要 $h\neq 0$，点 $(h,y)\neq(0,0)$，代入分式段：

$$\frac{f(h,y)-0}{h}=\frac{hy(h^2-y^2)}{h(h^2+y^2)}=\frac{y(h^2-y^2)}{h^2+y^2}$$

令 $h\to 0$：

$$\lim_{h\to 0}\frac{y(h^2-y^2)}{h^2+y^2}=\frac{y(0-y^2)}{0+y^2}=\frac{-y^3}{y^2}=-y$$

**情况 B：$y=0$**。这时 $f(h,0)=0$，所以

$$\frac{f(h,0)-0}{h}=\frac{0}{h}=0$$

与 $-y$ 在 $y=0$ 处的取值一致。

合并得

$$f'_x(0,y)=-y\quad(\text{对所有 }y)$$

### 第二步：求 $f'_y(x,0)$

按偏导数定义：

$$f'_y(x,0)=\lim_{k\to 0}\frac{f(x,k)-f(x,0)}{k}$$

当 $x\neq 0$、$k\neq 0$ 时：

$$\frac{f(x,k)-0}{k}=\frac{xk(x^2-k^2)}{k(x^2+k^2)}=\frac{x(x^2-k^2)}{x^2+k^2}$$

令 $k\to 0$：

$$\lim_{k\to 0}\frac{x(x^2-k^2)}{x^2+k^2}=\frac{x\cdot x^2}{x^2}=x$$

当 $x=0$ 时同样为 0，故

$$f'_y(x,0)=x\quad(\text{对所有 }x)$$

### 第三步：求二阶混合偏导

$f''_{xy}(0,0)$：先把 $f'_x(0,y)=-y$ 在 $y=0$ 处对 $y$ 求导：

$$f''_{xy}(0,0)=\lim_{k\to 0}\frac{f'_x(0,k)-f'_x(0,0)}{k}=\lim_{k\to 0}\frac{-k-0}{k}=-1$$

$f''_{yx}(0,0)$：先把 $f'_y(x,0)=x$ 在 $x=0$ 处对 $x$ 求导：

$$f''_{yx}(0,0)=\lim_{h\to 0}\frac{f'_y(h,0)-f'_y(0,0)}{h}=\lim_{h\to 0}\frac{h-0}{h}=1$$

于是 $f''_{xy}(0,0)=-1\neq 1=f''_{yx}(0,0)$。证毕。

### 小结

教材里"二阶混合偏导相等"是有前提的（连续性）。本题是一个经典反例。看到分段函数，首先应当想到「定义法求导」：分母里的 $(x^2+y^2)$ 在原点处为零，公式 $\dfrac{\partial f}{\partial x}=\dfrac{\partial(\text{分子})/\partial x\cdot\text{分母}-\text{分子}\cdot\partial(\text{分母})/\partial x}{\text{分母}^2}$ 在原点处用不上。

---

## 三、矩阵视角下的梯度变换（例题 7.3.9）

### 题目

设二元函数 $u$ 具有连续偏导数，把

$$\left(\frac{\partial u}{\partial x}\right)^2+\left(\frac{\partial u}{\partial y}\right)^2$$

化为极坐标 $(r,\theta)$ 下的形式。

### 思路

直接展开平方和也能做，但表达式会很乱。更高效的做法是：

1. 把链式法则写成矩阵形式；
2. 观察这个矩阵能否化为正交矩阵；
3. 一旦矩阵正交，向量长度平方在变换前后相等，结论直接出来。

### 第一步：建立链式法则的矩阵形式

设 $x=r\cos\theta$，$y=r\sin\theta$。由链式法则：

$$\begin{cases}\dfrac{\partial u}{\partial r}=\cos\theta\cdot\dfrac{\partial u}{\partial x}+\sin\theta\cdot\dfrac{\partial u}{\partial y}\\[6pt] \dfrac{\partial u}{\partial\theta}=-r\sin\theta\cdot\dfrac{\partial u}{\partial x}+r\cos\theta\cdot\dfrac{\partial u}{\partial y}\end{cases}$$

写成矩阵：

$$\begin{pmatrix}\partial u/\partial r\\ \partial u/\partial\theta\end{pmatrix}=\underbrace{\begin{pmatrix}\cos\theta & \sin\theta\\ -r\sin\theta & r\cos\theta\end{pmatrix}}_{J}\begin{pmatrix}\partial u/\partial x\\ \partial u/\partial y\end{pmatrix}$$

### 第二步：把第二行除以 $r$

把第二行除以 $r$，让第二行变成"梯度"的另一分量形式：

$$\begin{pmatrix}\partial u/\partial r\\ (1/r)\partial u/\partial\theta\end{pmatrix}=\underbrace{\begin{pmatrix}\cos\theta & \sin\theta\\ -\sin\theta & \cos\theta\end{pmatrix}}_{R_\theta}\begin{pmatrix}\partial u/\partial x\\ \partial u/\partial y\end{pmatrix}$$

### 第三步：观察矩阵 $R_\theta$

$R_\theta=\begin{pmatrix}\cos\theta & \sin\theta\\ -\sin\theta & \cos\theta\end{pmatrix}$ 是一个二维旋转矩阵，它满足

$$R_\theta^{\mathsf T}R_\theta=I$$

也就是正交矩阵。正交变换保持向量长度平方不变。

### 第四步：写出最终等式

把上面的矩阵等式记作 $v=R_\theta g$，其中 $g=(\partial u/\partial x,\partial u/\partial y)^{\mathsf T}$，$v=(\partial u/\partial r,(1/r)\partial u/\partial\theta)^{\mathsf T}$。由正交性：

$$\|v\|^2=\|R_\theta g\|^2=\|g\|^2$$

即

$$\boxed{\left(\frac{\partial u}{\partial x}\right)^2+\left(\frac{\partial u}{\partial y}\right)^2=\left(\frac{\partial u}{\partial r}\right)^2+\frac{1}{r^2}\left(\frac{\partial u}{\partial\theta}\right)^2}$$

### 验证

可以用 $u=x=r\cos\theta$ 来验证：

- 左边：$(\partial u/\partial x)^2+(\partial u/\partial y)^2=1^2+0^2=1$；
- 右边：$(\partial u/\partial r)^2+(1/r)^2(\partial u/\partial\theta)^2=(\cos\theta)^2+(1/r)^2(-r\sin\theta)^2=\cos^2\theta+\sin^2\theta=1$。

左右相等，符合。

### 小结

这道题的核心动作是「除以 $r$」。看上去只调整了一行，但这一调整让矩阵变成了正交形式，正交性的几何意义直接给出结果。

---

## 四、Laplacian 在柱坐标下的推导（习题 7.3.21(1)）

### 题目

设三元函数 $u(x,y,z)$ 具有二阶连续偏导数，证明在 $x=r\cos\theta,\,y=r\sin\theta,\,z=z$ 下成立

$$\frac{\partial^2 u}{\partial x^2}+\frac{\partial^2 u}{\partial y^2}+\frac{\partial^2 u}{\partial z^2}=\frac{1}{r}\frac{\partial}{\partial r}\!\left(r\frac{\partial u}{\partial r}\right)+\frac{1}{r^2}\frac{\partial^2 u}{\partial\theta^2}+\frac{\partial^2 u}{\partial z^2}$$

### 思路

把 $z$ 部分单独处理（$z$ 在两种坐标下都是自身），核心是把 $xy$ 平面的 Laplacian $\partial^2 u/\partial x^2+\partial^2 u/\partial y^2$ 化为柱坐标形式。

具体步骤：

1. 用第 3 题的逆变换把 $u_x$、$u_y$ 用 $u_r$、$u_\theta$ 表达；
2. 把算子 $\partial/\partial x$、$\partial/\partial y$ 也写成对 $r$、$\theta$ 求导的算子；
3. 把算子套到 $u_x$、$u_y$ 上，展开相加；
4. 用 $\sin^2\theta+\cos^2\theta=1$ 化简交叉项。

### 第一步：写出 $u_x$、$u_y$（用 $u_r$、$u_\theta$ 表示）

由第 3 题推导中的逆变换（验证见下面小框），

$$u_x=\cos\theta\,u_r-\frac{\sin\theta}{r}u_\theta,\qquad u_y=\sin\theta\,u_r+\frac{\cos\theta}{r}u_\theta$$

**逆变换的来源**：上一步矩阵 $J=\begin{pmatrix}\cos\theta & \sin\theta\\ -r\sin\theta & r\cos\theta\end{pmatrix}$ 的行列式为 $r$，逆矩阵为

$$J^{-1}=\begin{pmatrix}\cos\theta & -\sin\theta/r\\ \sin\theta & \cos\theta/r\end{pmatrix}$$

两边乘以 $J^{-1}$，得到 $u_x,u_y$ 的表达式。

### 第二步：写出算子 $\partial/\partial x$、$\partial/\partial y$

由 $\dfrac{\partial r}{\partial x}=\dfrac{x}{r}=\cos\theta$，$\dfrac{\partial\theta}{\partial x}=-\dfrac{y}{r^2}=-\dfrac{\sin\theta}{r}$ 等，可推出

$$\frac{\partial}{\partial x}=\cos\theta\frac{\partial}{\partial r}-\frac{\sin\theta}{r}\frac{\partial}{\partial \theta}$$

$$\frac{\partial}{\partial y}=\sin\theta\frac{\partial}{\partial r}+\frac{\cos\theta}{r}\frac{\partial}{\partial \theta}$$

> 验证：把 $\partial/\partial x$ 套到 $u$ 上，$\partial u/\partial x=(\partial r/\partial x)\partial u/\partial r+(\partial\theta/\partial x)\partial u/\partial\theta=\cos\theta\,u_r-\dfrac{\sin\theta}{r}u_\theta=u_x$。与第一步的 $u_x$ 表达式一致。$\partial/\partial y$ 同理。

### 第三步：算 $u_{xx}$

把 $\partial/\partial x$ 套到 $u_x$ 上：

$$u_{xx}=\left(\cos\theta\frac{\partial}{\partial r}-\frac{\sin\theta}{r}\frac{\partial}{\partial\theta}\right)\!\left(\cos\theta\,u_r-\frac{\sin\theta}{r}u_\theta\right)$$

先算里面两个偏导：

$$\frac{\partial}{\partial r}\!\left(\cos\theta\,u_r-\frac{\sin\theta}{r}u_\theta\right)=\cos\theta\,u_{rr}+\frac{\sin\theta}{r^2}u_\theta-\frac{\sin\theta}{r}u_{r\theta}$$

（解释：对 $\cos\theta\,u_r$ 求导，$\cos\theta$ 视作常数，得 $\cos\theta\,u_{rr}$；对 $-(\sin\theta/r)u_\theta$ 求导，用乘积法则：$\dfrac{d}{dr}\!\left(\dfrac{\sin\theta}{r}\right)=-\dfrac{\sin\theta}{r^2}$，所以 $-(\sin\theta/r)u_\theta$ 的导数为 $\dfrac{\sin\theta}{r^2}u_\theta-\dfrac{\sin\theta}{r}u_{r\theta}$。）

$$\frac{\partial}{\partial\theta}\!\left(\cos\theta\,u_r-\frac{\sin\theta}{r}u_\theta\right)=-\sin\theta\,u_r+\cos\theta\,u_{r\theta}-\frac{\cos\theta}{r}u_\theta-\frac{\sin\theta}{r}u_{\theta\theta}$$

（解释：对 $\cos\theta\,u_r$ 求导得 $-\sin\theta\,u_r+\cos\theta\,u_{r\theta}$；对 $-(\sin\theta/r)u_\theta$ 求导，$\dfrac{d}{d\theta}(\sin\theta/r)=\cos\theta/r$，所以这部分导数为 $-(\cos\theta/r)u_\theta-(\sin\theta/r)u_{\theta\theta}$。）

代回算子展开式：

$$
\begin{aligned}
u_{xx}&=\cos\theta\!\left(\cos\theta\,u_{rr}+\frac{\sin\theta}{r^2}u_\theta-\frac{\sin\theta}{r}u_{r\theta}\right)\\
&\quad -\frac{\sin\theta}{r}\!\left(-\sin\theta\,u_r+\cos\theta\,u_{r\theta}-\frac{\cos\theta}{r}u_\theta-\frac{\sin\theta}{r}u_{\theta\theta}\right)
\end{aligned}
$$

展开得到 7 项：

$$
\begin{aligned}
u_{xx}&=\cos^2\theta\,u_{rr}+\frac{\cos\theta\sin\theta}{r^2}u_\theta-\frac{\cos\theta\sin\theta}{r}u_{r\theta}\\
&\quad +\frac{\sin^2\theta}{r}u_r-\frac{\sin\theta\cos\theta}{r}u_{r\theta}+\frac{\sin\theta\cos\theta}{r^2}u_\theta+\frac{\sin^2\theta}{r^2}u_{\theta\theta}
\end{aligned}
$$

合并同类项：

$$
u_{xx}=\cos^2\theta\,u_{rr}+\frac{\sin^2\theta}{r}u_r+\frac{2\sin\theta\cos\theta}{r^2}u_\theta-\frac{2\sin\theta\cos\theta}{r}u_{r\theta}+\frac{\sin^2\theta}{r^2}u_{\theta\theta}
$$

### 第四步：算 $u_{yy}$（结构与 $u_{xx}$ 类似）

把 $\partial/\partial y$ 套到 $u_y$ 上：

$$u_{yy}=\left(\sin\theta\frac{\partial}{\partial r}+\frac{\cos\theta}{r}\frac{\partial}{\partial\theta}\right)\!\left(\sin\theta\,u_r+\frac{\cos\theta}{r}u_\theta\right)$$

逐项处理后合并，得

$$
u_{yy}=\sin^2\theta\,u_{rr}+\frac{\cos^2\theta}{r}u_r-\frac{2\sin\theta\cos\theta}{r^2}u_\theta+\frac{2\sin\theta\cos\theta}{r}u_{r\theta}+\frac{\cos^2\theta}{r^2}u_{\theta\theta}
$$

> **怎么从 $u_{xx}$ 推 $u_{yy}$**：把 $u_x$ 表达式里的 $\cos\theta$、$\sin\theta$ 互换位置（$\sin\theta\to\cos\theta$、$\cos\theta\to\sin\theta$）并注意 $1/r$ 那一项的符号变化。最稳妥还是按第三步同样的方法算一遍。

### 第五步：$u_{xx}+u_{yy}$ 相加

| 项 | $u_{xx}$ 系数 | $u_{yy}$ 系数 | 和 |
|---|---|---|---|
| $u_{rr}$ | $\cos^2\theta$ | $\sin^2\theta$ | $1$ |
| $u_r$ | $\sin^2\theta/r$ | $\cos^2\theta/r$ | $1/r$ |
| $u_\theta$ | $2\sin\theta\cos\theta/r^2$ | $-2\sin\theta\cos\theta/r^2$ | $0$ |
| $u_{r\theta}$ | $-2\sin\theta\cos\theta/r$ | $2\sin\theta\cos\theta/r$ | $0$ |
| $u_{\theta\theta}$ | $\sin^2\theta/r^2$ | $\cos^2\theta/r^2$ | $1/r^2$ |

交叉项（$u_\theta$、$u_{r\theta}$ 的系数）相消，剩下的用 $\sin^2\theta+\cos^2\theta=1$ 化简：

$$u_{xx}+u_{yy}=u_{rr}+\frac{1}{r}u_r+\frac{1}{r^2}u_{\theta\theta}$$

右边正好等于

$$\frac{1}{r}\frac{\partial}{\partial r}\!\left(r\frac{\partial u}{\partial r}\right)+\frac{1}{r^2}\frac{\partial^2 u}{\partial\theta^2}$$

（验证：$\dfrac{1}{r}\dfrac{\partial}{\partial r}(ru_r)=\dfrac{1}{r}(u_r+ru_{rr})=\dfrac{u_r}{r}+u_{rr}$。）

### 第六步：加上 $u_{zz}$

$z$ 在两种坐标下都是自身，$\partial^2 u/\partial z^2$ 形式不变，所以

$$u_{xx}+u_{yy}+u_{zz}=\frac{1}{r}\frac{\partial}{\partial r}\!\left(r\frac{\partial u}{\partial r}\right)+\frac{1}{r^2}\frac{\partial^2 u}{\partial\theta^2}+\frac{\partial^2 u}{\partial z^2}$$

证毕。

### 验证

取 $u=r^2=x^2+y^2$（与 $\theta$、$z$ 无关），验证 $xy$ 平面部分：

- 左边：$u_{xx}+u_{yy}=2+2=4$；
- 右边：$u_r=2r$，$u_{rr}=2$，$u_\theta=0$，代入 $u_{rr}+(1/r)u_r+(1/r^2)u_{\theta\theta}=2+2+0=4$。一致。

### 小结

本题的"巧"在于把算子 $\partial/\partial x$ 也用 $(r,\theta)$ 展开。如果直接把 $\partial/\partial y$ 写成 $\sin\theta\,\partial/\partial r+\cos\theta\,\partial/\partial \theta$（漏掉了那个 $\dfrac{1}{r}$ 因子），后面所有符号都会错。本题计算量大，关键是细心记号。

---

## 五、切平面过定点：空间几何综合（习题 7.4.17）

### 题目

设 $f$ 是具有连续偏导数的二元函数，证明：曲面

$$f\!\left(\frac{x-a}{z-c},\frac{y-b}{z-c}\right)=0$$

上任意一点处的切平面都经过同一定点。

### 思路

切平面过定点的题，标准打法是：

1. 写出曲面在任意一点 $(x_0,y_0,z_0)$ 处的切平面方程；
2. 把候选定点 $(a,b,c)$ 代进去；
3. 验证方程恒为零。

候选定点几乎一定是 $(a,b,c)$：曲面方程里出现了 $(x-a)$、$(y-b)$、$(z-c)$，这三个因子在 $(a,b,c)$ 处同时为零，于是偏导前面的系数都会被压成零。

### 第一步：装配复合函数

设 $u=\dfrac{x-a}{z-c}$，$v=\dfrac{y-b}{z-c}$，则 $F(x,y,z)=f(u,v)$，曲面方程为 $F(x,y,z)=0$。

为避免符号混淆，约定 $f_1=\partial f/\partial u$，$f_2=\partial f/\partial v$。

### 第二步：求三个偏导

由链式法则：

$$F_x=f_1\cdot\frac{\partial u}{\partial x}=f_1\cdot\frac{1}{z-c}$$

$$F_y=f_2\cdot\frac{\partial v}{\partial y}=f_2\cdot\frac{1}{z-c}$$

$$
\begin{aligned}
F_z&=f_1\cdot\frac{\partial u}{\partial z}+f_2\cdot\frac{\partial v}{\partial z}\\
&=f_1\cdot\left(-\frac{x-a}{(z-c)^2}\right)+f_2\cdot\left(-\frac{y-b}{(z-c)^2}\right)\\
&=-\frac{f_1(x-a)+f_2(y-b)}{(z-c)^2}
\end{aligned}
$$

要求 $z\neq c$，否则 $u$、$v$ 无意义。

### 第三步：写出切平面方程

设 $(x_0,y_0,z_0)$ 是曲面上一点（$z_0\neq c$），切平面为

$$F_x(x_0,y_0,z_0)(x-x_0)+F_y(x_0,y_0,z_0)(y-y_0)+F_z(x_0,y_0,z_0)(z-z_0)=0$$

把 $F_x$、$F_y$、$F_z$ 代入：

$$\frac{f_1}{z_0-c}(x-x_0)+\frac{f_2}{z_0-c}(y-y_0)-\frac{f_1(x_0-a)+f_2(y_0-b)}{(z_0-c)^2}(z-z_0)=0$$

两边乘以 $(z_0-c)^2$ 化简：

$$(z_0-c)\bigl[f_1(x-x_0)+f_2(y-y_0)\bigr]-\bigl[f_1(x_0-a)+f_2(y_0-b)\bigr](z-z_0)=0$$

### 第四步：代入 $(a,b,c)$ 看是否成立

把 $x=a$、$y=b$、$z=c$ 代入上式。注意三组等式：

- $a-x_0=-(x_0-a)$，$b-y_0=-(y_0-b)$；
- $c-z_0=-(z_0-c)$。

于是

$$
\begin{aligned}
&\;(z_0-c)\bigl[f_1(a-x_0)+f_2(b-y_0)\bigr]-\bigl[f_1(x_0-a)+f_2(y_0-b)\bigr](c-z_0)\\
=&\;(z_0-c)\bigl[-f_1(x_0-a)-f_2(y_0-b)\bigr]+\bigl[f_1(x_0-a)+f_2(y_0-b)\bigr](z_0-c)\\
=&\;-(z_0-c)\bigl[f_1(x_0-a)+f_2(y_0-b)\bigr]+(z_0-c)\bigl[f_1(x_0-a)+f_2(y_0-b)\bigr)\\
=&\;0
\end{aligned}
$$

等式恒成立。因此 $(a,b,c)$ 在曲面上每一点的切平面上。证毕。

### 小结

本题的灵魂在于"把曲面写成以 $(a,b,c)$ 为中心的复合结构"。一旦写成 $u=\dfrac{x-a}{z-c}$、$v=\dfrac{y-b}{z-c}$ 的形式，$(a,b,c)$ 处的 $x-a=0$、$y-b=0$、$z-c=0$ 会让三个偏导前的因子同时为零，整个表达式自动抵消。
