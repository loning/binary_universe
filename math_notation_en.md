# Binary Universe Theory Mathematical Notation [Core Theory Version: 1.0]

[中文](math_notation.md) | [English](math_notation_en.md)

This document explains the main mathematical symbols used in Binary Universe Theory to help readers understand the formal expressions of the theory.

## Basic Set Symbols

- $\mathbb{B} = \{0, 1\}$: Binary set, the basic state space of the universe
- $\mathbb{B}^{n}$: n-dimensional binary vector space, representing a state space with n bits
- $\mathbb{B}^{n}, n \rightarrow \infty$: Infinite-dimensional binary space, representing the complete state space of the universe

## Operation Symbols

- $\oplus$: Binary XOR operator, defined as 0⊕0=0, 0⊕1=1, 1⊕0=1, 1⊕1=0
- $XOR(a, b)$: XOR function, equivalent to $a \oplus b$
- $\sum_{i=1}^{N}$: Summation symbol, typically used to represent quantum state superposition
- $\rightarrow$: Mapping symbol, e.g., $F: \mathbb{B}^{n} \rightarrow \mathbb{B}^{n}$ represents a function mapping from binary space to itself
- $\subset$: Subset symbol, e.g., $Observer \subset Universe$ indicates that the observer is a subset of the universe

## Special Functions and Operators

- $F(U_t)$: Self-reference function acting on the universe state
- $R(U_t^{(local)})$: Local self-reference mapping, used to define the observer
- $-\sum_{i} p_i \log_2 p_i$: Information entropy expression, where $p_i$ is the probability of the ith state

## State Representations

- $U_t$: Universe state at time t
- $U_{t+1}$: Universe state at the next moment
- $U_t^{(local)}$: Local state of the universe
- $U_t^{(observed)}$: Observed part of the universe state
- $State_i$: One of the possible quantum states
- $QuantumState = \sum_{i=1}^{N} \alpha_i \cdot State_i$: Quantum superposition state
- $ClassicalState$: Classical deterministic state
- $Observer$: Observer state
- $Observation$: Observation result state

## Subscripts and Superscripts

- Subscript $t$: Indicates time, e.g., $U_t$ represents the universe state at time t
- Subscripts $i, j, k$, etc.: Used to index different states or elements
- Superscript $(local)$: Indicates locality, e.g., $U_t^{(local)}$ represents a local state of the universe
- Superscript $(observed)$: Indicates the observed part

## Special Symbols

- $|\alpha_i|^2$: Square of the probability amplitude, representing the probability of obtaining the corresponding state when measured
- $\forall$: Universal quantifier, "for all," e.g., $\forall u \in Universe$ means for all elements in the universe
- $\exists$: Existential quantifier, "there exists," e.g., $\exists b \in \mathbb{B}^{k}$ means there exists a binary sequence
- $\equiv$: Identity, indicating that the left and right sides are equivalent by definition
- $\approx$: Approximately equal to

## Universe Evolution Equations

Core evolution equation of Binary Universe Theory:

$`
U_{t+1} = XOR(U_t, F(U_t))
`$

Observer definition equation:

$`
Observer = XOR(U_t^{(local)}, R(U_t^{(local)}))
`$

Observation process equation:

$`
Observation = XOR(Observer, U_t^{(observed)})
`$

Mapping from quantum state to classical state:

$`
QuantumState \xrightarrow{XOR(Observer, \cdot)} ClassicalState
`$

---

This notation table will be continuously updated and expanded as the theory develops. For special symbols not included here, please refer to the specific explanations in the relevant chapters. 