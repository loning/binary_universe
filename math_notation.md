# 二进制宇宙理论数学符号表 [核心理论版本号：1.0]

[中文](math_notation.md) | [English](math_notation_en.md)

本文档说明了二进制宇宙理论中使用的主要数学符号，以便读者理解理论的形式化表达。

## 基本集合符号

- $\mathbb{B} = \{0, 1\}$：二进制集合，宇宙的基本状态空间
- $\mathbb{B}^{n}$：n维二进制向量空间，表示有n个比特的状态空间
- $\mathbb{B}^{n}, n \rightarrow \infty$：无限维二进制空间，表示宇宙的完整状态空间

## 运算符号

- $\oplus$：二进制异或运算符，定义为0⊕0=0, 0⊕1=1, 1⊕0=1, 1⊕1=0
- $XOR(a, b)$：异或函数，等同于$a \oplus b$
- $\sum_{i=1}^{N}$：求和符号，通常用于表示量子态的叠加
- $\rightarrow$：映射符号，如$F: \mathbb{B}^{n} \rightarrow \mathbb{B}^{n}$表示从二进制空间到其自身的函数映射
- $\subset$：子集符号，如$Observer \subset Universe$表示观察者是宇宙的一个子集

## 特殊函数和算子

- $F(U_t)$：作用于宇宙状态的自参照函数
- $R(U_t^{(local)})$：局部自参照映射，用于定义观察者
- $-\sum_{i} p_i \log_2 p_i$：信息熵表达式，其中$p_i$是第i个状态的概率

## 状态表示

- $U_t$：表示宇宙在时刻t的状态
- $U_{t+1}$：表示宇宙在下一时刻的状态
- $U_t^{(local)}$：宇宙的局部状态
- $U_t^{(observed)}$：被观测的宇宙状态部分
- $State_i$：可能的量子态之一
- $QuantumState = \sum_{i=1}^{N} \alpha_i \cdot State_i$：量子叠加态
- $ClassicalState$：经典确定态
- $Observer$：观察者状态
- $Observation$：观测结果状态

## 下标和上标

- 下标$t$：表示时刻，如$U_t$表示时刻t的宇宙状态
- 下标$i, j, k$等：用于索引不同的状态或元素
- 上标$(local)$：表示局部，如$U_t^{(local)}$表示宇宙的局部状态
- 上标$(observed)$：表示被观测的部分

## 特殊符号

- $|\alpha_i|^2$：概率幅的平方，表示测量得到相应状态的概率
- $\forall$：全称量词，"对所有"，如$\forall u \in Universe$表示对宇宙中的所有元素
- $\exists$：存在量词，"存在"，如$\exists b \in \mathbb{B}^{k}$表示存在某个二进制序列
- $\equiv$：恒等，表示左右两边在定义上等价
- $\approx$：近似等于

## 宇宙演化方程

二进制宇宙理论的核心演化方程：

$`
U_{t+1} = XOR(U_t, F(U_t))
`$

观察者定义方程：

$`
Observer = XOR(U_t^{(local)}, R(U_t^{(local)}))
`$

观测过程方程：

$`
Observation = XOR(Observer, U_t^{(observed)})
`$

量子态到经典态的映射：

$`
QuantumState \xrightarrow{XOR(Observer, \cdot)} ClassicalState
`$

---

本符号表将随着理论的发展不断更新和扩充。如有特殊符号未包含在内，请参考相关章节的具体说明。 