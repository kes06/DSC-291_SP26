# HW5 Solutions (Part A)

## Coverage Map (Part A requirements -> subsection)
1. A1 statistical implication of VC bound and brute-force runtime -> Section A1.
2. A2 reduction from Set Cover to agreement, both directions, and learner-to-agreement consequence -> Section A2.
3. A3 experiment with sparse 0-1 baseline vs convex surrogate, runtime scaling, agreement comparison, and interpretation -> Section A3.

Traceability check: every Part A bullet appears as a named subsection below.

## A1. What Homework 4 Already Gives
Let $d$ be ambient dimension and $k$ the sparsity level.

From Homework 4, for $1 \le k \le d/2$,

```math
\mathrm{VCdim}(\mathcal H_{d,k}) \le C_{\mathrm{vc}}\, k\log\!\left(\frac{ed}{k}\right)
```

for a universal constant $C_{\mathrm{vc}}>0$, and for larger $k$ we have the dense-halfspace bound $\mathrm{VCdim}(\mathcal H_{d,k})\le d+1$.
Hence we can write

```math
v := \mathrm{VCdim}(\mathcal H_{d,k}) \le \min\!\left\{C_{\mathrm{vc}}k\log\!\left(\frac{ed}{k}\right),\ d+1\right\}.
```

If exact ERM over $\mathcal H_{d,k}$ were computationally available, the standard agnostic VC generalization theorem gives sample size

```math
m \ge C_{\mathrm{gen}}\,\frac{v+\log(1/\delta)}{\varepsilon^2}
```

for an absolute constant $C_{\mathrm{gen}}$, to achieve excess $0$-$1$ risk at most $\varepsilon$ with probability at least $1-\delta$. So statistically, sparse proper learning is controlled by $k\log(ed/k)$ (or by $d$ in the dense regime).

Brute-force realizable algorithm runtime (Homework 4): enumerate all supports $S\subseteq[d]$ with $|S|\le k$, and for each support solve linear feasibility on that restricted coordinate set.
If $T_{\mathrm{feas}}(n,d)$ is the feasibility solver time on $n$ examples, runtime is

```math
R(n,d,k)=\left(\sum_{j=0}^k \binom{d}{j}\right)\,T_{\mathrm{feas}}(n,d).
```

Using $\sum_{j=0}^k\binom{d}{j}\le (k+1)(ed/k)^k$, this is

```math
R(n,d,k) \le (k+1)\left(\frac{ed}{k}\right)^k T_{\mathrm{feas}}(n,d).
```

So it is polynomial in $d$ when $k=O(1)$, quasi-polynomial when $k=\Theta(\log d)$, and super-polynomial in general when $k$ grows faster than $\log d$.

Why no contradiction: VC/sample-complexity is an information-theoretic/statistical statement (how many samples suffice), while the support enumeration cost is a computational statement (time to optimize empirical $0$-$1$ objective).

### AI suggestion log (required workflow)
- Rejected suggestion: "state runtime as simply $d^k$ and stop."  
  Why rejected: it hides the exact combinatorial factor and misses regime distinctions requested by the problem.

## A2. Hardness of Agreement via Set Cover
### Universally quantified objects and adversarial choices (setup first)
- Universal instance: Set Cover input $(U,\{S_i\}_{i=1}^m,k)$ with $U=\{u_1,\dots,u_n\}$.
- Adversarial classifier candidate in agreement instance: any $k$-sparse $w\in\mathbb R^m$.
- We must prove both directions exactly.

### Reduction construction
Use one coordinate per set ($d=m$).

Define examples:
1. For each set index $i\in[m]$, include one positive example $(e_i,+1)$, where $e_i$ is the $i$th standard basis vector.
2. For each universe element $u_j$, define incidence vector $v_j\in\{0,1\}^m$ by

```math
(v_j)_i = \mathbf 1[u_j\in S_i].
```

Include $B:=k+1$ copies of $(v_j,-1)$.

Set agreement threshold

```math
q := nB + (m-k).
```

So instance size is $m+nB=m+n(k+1)$, polynomial in input size.

### (=>) If Set Cover is YES, agreement instance is YES
Assume there exists cover $C\subseteq[m]$ with $|C|\le k$ and $\cup_{i\in C}S_i=U$.
Define

```math
w_i = \begin{cases}
-1,& i\in C,\\
0,& i\notin C.
\end{cases}
```

Then $\|w\|_0=|C|\le k$.

- Positive examples: for $(e_i,+1)$, prediction is $\operatorname{sign}(w_i)$. It is wrong exactly when $i\in C$. So positives correct: $m-|C|\ge m-k$.
- Negative element examples: for each $u_j$, because $C$ covers $U$, there exists $i\in C$ with $u_j\in S_i$, so

```math
\langle w,v_j\rangle = -\#\{i\in C: u_j\in S_i\}\le -1 <0,
```

thus each copy of $(v_j,-1)$ is correct. Total negative correct: $nB$.

Total correct is at least

```math
nB + (m-k) = q.
```

Hence agreement is YES.

### (<=) If agreement instance is YES, Set Cover is YES
Assume there exists $w\in\mathbb R^m$ with $\|w\|_0\le k$ that correctly labels at least $q$ examples.

Define

```math
t := |\{i: w_i<0\}|,
```

so $0\le t\le \|w\|_0\le k$.

Let

```math
c := |\{j\in[n]: \langle w,v_j\rangle <0\}|.
```

- Positive examples $(e_i,+1)$: exactly coordinates with $w_i<0$ are mistakes, so positives correct $=m-t$.
- Negative examples: for each $j$ with $\langle w,v_j\rangle<0$, all $B$ copies are correct; otherwise all $B$ are wrong. So negatives correct $=Bc$.

Thus

```math
(m-t)+Bc \ge q = m-k+Bn.
```

Subtract $m$ from both sides:

```math
-t+Bc \ge -k+Bn.
```

Move terms:

```math
B(n-c) \le k-t.
```

Now use explicit constants: $B=k+1$, and $k-t\le k$.
If $c<n$, then $n-c\ge1$, so

```math
B(n-c)\ge B=k+1>k\ge k-t,
```

contradiction. Therefore $c=n$.
So for every $j$, $\langle w,v_j\rangle<0$.

Now define candidate set family

```math
C^-:=\{i\in[m]: w_i<0\},\quad |C^-|=t\le k.
```

Claim: $C^-$ covers $U$. Fix any $u_j$.
If no set in $C^-$ contains $u_j$, then for every $i$ with $(v_j)_i=1$, we have $w_i\ge0$.
Hence

```math
\langle w,v_j\rangle = \sum_{i:(v_j)_i=1} w_i \ge 0,
```

contradicting $\langle w,v_j\rangle<0$.
So some $i\in C^-$ contains $u_j$.
Since $j$ was arbitrary, $\cup_{i\in C^-}S_i=U$ with $|C^-|\le k$.
Therefore Set Cover is YES.

This proves Set Cover $\le_p$ agreement over $\mathcal H_{d,k}$.

### Learner-to-agreement consequence (Week 5)
By the Week 5 learner-to-agreement theorem, an efficient proper agnostic learner for hypothesis family $\mathcal H$ implies an efficient procedure for the corresponding empirical agreement decision problem for $\mathcal H$ (with thresholded agreement target). Applying this to the family $\mathcal H_{d,k}$ when both $d$ and $k$ are part of input would yield a polynomial-time algorithm for our agreement instance. Since Set Cover reduces to that agreement problem, this would imply polynomial-time Set Cover. Therefore, unless $\mathrm{P}=\mathrm{NP}$, there is no efficient proper agnostic PAC learner for sparse linear classifiers when $k$ is part of the input.

### Proof-completeness check (required workflow)
Key inequality/bound steps and justification:
1. $(m-t)+Bc\ge m-k+Bn$ from threshold requirement.  
   Justification: definition of $q$ and exact counting.
2. $B(n-c)\le k-t$ by algebraic rearrangement of Step 1.
3. If $c<n$, then $n-c\ge1$ and $B(n-c)\ge B$ (integer monotonicity).
4. $B=k+1>k\ge k-t$ from $t\ge0$.
5. Steps 3 and 4 contradict Step 2, so $c=n$.
6. If no negative-weight covering set exists for element $u_j$, then $\langle w,v_j\rangle\ge0$ since all active terms are nonnegative; contradiction with $c=n$.

Normalization/constants audit: the repeated-example factor is explicitly $B=k+1$ and is tracked in every count and inequality.

Boundary-case audit:
- Empty universe $n=0$: reduction still valid (only positive examples); both Set Cover and agreement are trivially YES iff $k\ge0$.
- $k=0$: then $B=1$ and threshold becomes $q=n+m$; agreement YES iff all element-incidence negatives can be made correct with $w=0$, which matches Set Cover with zero sets.
- Elements not in any set: then no negative-weight family can force $\langle w,v_j\rangle<0$, so both instances are NO.

### AI suggestion log (required workflow)
- Rejected suggestion: "set non-selected coordinates to +1 in the YES-direction witness."  
  Why rejected: that vector is generally not $k$-sparse and violates the hypothesis-class constraint.

## A3. Experiment and Interpretation
I implemented a reproducible script at [`/Users/keshao/Documents/ucsd/Spring 2026/dsc291/DSC-291_SP26/hw5/partA_experiment.py`](/Users/keshao/Documents/ucsd/Spring%202026/dsc291/DSC-291_SP26/hw5/partA_experiment.py).

### Setup
- Synthetic binary classification with $x\in\mathbb R^d$, labels $y\in\{-1,+1\}$ from a sparse linear ground truth plus Gaussian noise.
- Proper sparse $0$-$1$ baseline (approximate): enumerate all supports with $|S|\le k$, then enumerate a finite weight grid $\{-2,-1,1,2\}^{|S|}$ on that support. Choose best empirical $0$-$1$ agreement.
- Convex surrogate: logistic loss with $\ell_1$ penalty, optimized by subgradient descent.

Important: baseline is **approximate** (finite weight grid), not exact global ERM over all real weights.

### Results (averaged over 3 seeds)
Scaling with $d$ ($n=120$, $k=2$):

| n | d | k | sparse time (s) | surrogate time (s) | train acc sparse | train acc surrogate | val acc sparse | val acc surrogate | surrogate obj | surrogate nnz |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
|120|6|2|0.0212|0.0260|0.931|0.922|0.930|0.917|0.418|6.0|
|120|8|2|0.0449|0.0310|0.956|0.958|0.958|0.947|0.382|8.0|
|120|10|2|0.0794|0.0359|0.925|0.933|0.930|0.902|0.401|10.0|
|120|12|2|0.1279|0.0405|0.942|0.942|0.932|0.915|0.409|12.0|

Scaling with $n$ ($d=10$, $k=2$):

| n | d | k | sparse time (s) | surrogate time (s) | train acc sparse | train acc surrogate | val acc sparse | val acc surrogate | surrogate obj | surrogate nnz |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
|60|10|2|0.0401|0.0183|0.917|0.944|0.905|0.888|0.390|10.0|
|120|10|2|0.0798|0.0360|0.925|0.933|0.930|0.902|0.401|10.0|
|180|10|2|0.1192|0.0539|0.913|0.920|0.910|0.900|0.407|10.0|
|240|10|2|0.1587|0.0717|0.943|0.946|0.942|0.930|0.406|10.0|

### Interpretation
- Runtime: sparse support/grid search grows quickly with $d$ (combinatorial support count), while surrogate scales more smoothly.
- Agreement: in this synthetic setup, both methods achieve similar empirical $0$-$1$ agreement; neither uniformly dominates on validation.
- Geometry/properness: the surrogate solves a convex objective over dense real vectors and here returns dense predictors (nnz approximately $d$), so it is **not** a proper $k$-sparse classifier in general.

This illustrates the Part A message: optimizing empirical $0$-$1$ agreement over proper sparse models is combinatorial, while convex surrogate optimization is computationally cleaner but may leave the proper sparse class.

### AI suggestion log (required workflow)
- Rejected suggestion: "report only one random-seed run."  
  Why rejected: too noisy for runtime/accuracy conclusions; replaced with 3-seed averages.

## References
- Hoeffding, W. (1963). Probability inequalities for sums of bounded random variables.
- Vapnik, V. and Chervonenkis, A. (1971). On the uniform convergence of relative frequencies.

# HW5 Solutions (Part B)

## Coverage Map (Part B requirements -> subsection)
1. Hinge loss with $\ell_1$ constraint as linear program; explain why this is not sparse $0$-$1$ ERM -> Section B1.
2. Concrete surrogate counterexample; compute minimizers; prove stated $0$-$1$ claims -> Section B2.
3. Fixed-feature parity barrier lower bound and matching upper bound -> Section B3.
4. Same predictors with convex vs non-convex optimization geometry -> Section B4.

Traceability check: every Part B bullet appears as a named subsection below.

## B1. Hinge Loss with an $\ell_1$ Constraint as a Linear Program
We are given examples $(x_i,y_i)$ with $y_i\in\{-1,+1\}$ and linear score $f_w(x)=\langle w,x\rangle$.
The optimization problem is

```math
\min_{\|w\|_1\le R}\ \frac1n\sum_{i=1}^n \left(1-y_i\langle w,x_i\rangle\right)_+.
```

Introduce variables:
- $w_j^+\ge 0$, $w_j^-\ge 0$ with $w_j=w_j^+-w_j^-$ for each $j\in[d]$.
- $\xi_i\ge 0$ for hinge slack at each sample $i\in[n]$.

Equivalent LP:

```math
\begin{aligned}
\min_{w^+,w^-,\xi}\quad & \frac1n\sum_{i=1}^n \xi_i\\
\text{s.t.}\quad
& \xi_i \ge 1-y_i\sum_{j=1}^d (w_j^+-w_j^-)x_{ij},\quad i=1,\dots,n,\\
& \xi_i\ge 0,\quad i=1,\dots,n,\\
& \sum_{j=1}^d (w_j^+ + w_j^-) \le R,\\
& w_j^+\ge 0,\ w_j^-\ge 0,\quad j=1,\dots,d.
\end{aligned}
```

Why this is equivalent:
1. For fixed $w$, minimizing over $\xi_i$ with $\xi_i\ge 1-y_if_w(x_i)$ and $\xi_i\ge 0$ gives

```math
\xi_i = \max\{0,\ 1-y_if_w(x_i)\} = (1-y_if_w(x_i))_+.
```

2. The constraint $\sum_j(w_j^++w_j^-)\le R$ is exactly $\|w\|_1\le R$.

Why this LP is not empirical sparse $0$-$1$ agreement over $k$-sparse classifiers:
- Objective mismatch: hinge surrogate vs $0$-$1$ indicator.
- Constraint mismatch: $\|w\|_1\le R$ allows dense vectors; it does not enforce $\|w\|_0\le k$.
- Therefore this LP optimizes a convex surrogate over an $\ell_1$ ball, not proper $k$-sparse ERM.

### AI suggestion log (required workflow)
- Rejected suggestion: "encode $|w_j|$ directly as a linear term without extra variables."
  Why rejected: absolute value is not linear in LP form; must use $w_j^+,w_j^-$.

## B2. A Concrete Counterexample: the Surrogate Comparator Can Be Bad
Let $\alpha\in(0,1/2)$ and $\beta>(1-\alpha)/\alpha$.
Distribution over $(x,y)$:

```math
\mathbb P[(x,y)=(1,+1)] = 1-\alpha,\qquad
\mathbb P[(x,y)=(-\beta,+1)] = \alpha.
```

Predictors are one-dimensional homogeneous linear scores $f_w(x)=wx$.

### Step 1: Population hinge risk and minimizers
Population hinge risk:

```math
\mathcal R_{\mathrm{hinge}}(w)
=(1-\alpha)(1-w)_+ + \alpha(1+\beta w)_+.
```

Piecewise form:
1. If $w\le -1/\beta$, then $1+\beta w\le 0$ and $1-w>0$, so

```math
\mathcal R_{\mathrm{hinge}}(w)=(1-\alpha)(1-w).
```

2. If $-1/\beta \le w\le 1$, both hinge terms are active, so

```math
\mathcal R_{\mathrm{hinge}}(w)
=(1-\alpha)(1-w)+\alpha(1+\beta w)
=1+w\big(\alpha\beta-(1-\alpha)\big).
```

3. If $w\ge 1$, then $1-w\le 0$ and $1+\beta w>0$, so

```math
\mathcal R_{\mathrm{hinge}}(w)=\alpha(1+\beta w).
```

Now analyze slopes:
- Region 1 slope: $-(1-\alpha)<0$.
- Region 2 slope: $\alpha\beta-(1-\alpha)>0$ since $\beta>(1-\alpha)/\alpha$.
- Region 3 slope: $\alpha\beta>0$.

Hence risk decreases up to $w=-1/\beta$ and increases after it, so the unique minimizer is

```math
w^\star_{\mathrm{hinge}}=-\frac1\beta.
```

### Step 2: Prove $0$-$1$ claims exactly
Here $y=+1$ always, and the assignment defines $0$-$1$ margin loss as $\mathbf 1[yf_w(x)\le 0]$.

- On $(x,y)=(1,+1)$, error iff $w\le 0$.
- On $(x,y)=(-\beta,+1)$, error iff $-\beta w\le 0$, i.e., $w\ge 0$.

So:
1. If $w<0$, risk is $1-\alpha$.
2. If $w>0$, risk is $\alpha$.
3. If $w=0$, risk is $1$ (both points are margin-zero errors).

Therefore

```math
\inf_w \mathcal R_{0\text{-}1}(f_w)=\alpha,
```

attained by any $w>0$.

Every hinge minimizer equals $w^\star_{\mathrm{hinge}}=-1/\beta<0$, hence its $0$-$1$ risk is

```math
\mathcal R_{0\text{-}1}(f_{w^\star_{\mathrm{hinge}}})=1-\alpha.
```

So both required statements hold:

```math
\inf_w \mathcal R_{0\text{-}1}(f_w)=\alpha,
\qquad
\text{every hinge-risk minimizer has } \mathcal R_{0\text{-}1}=1-\alpha.
```

Given any $\varepsilon>0$ and $\tau<1$, choose $\alpha\le\varepsilon$ and also $\alpha<1-\tau$; then choose $\beta>(1-\alpha)/\alpha$.
This gives

```math
\inf_w \mathcal R_{0\text{-}1}(f_w)\le \varepsilon
```

while every hinge minimizer has

```math
\mathcal R_{0\text{-}1}(f_{w^\star_{\mathrm{hinge}}})=1-\alpha>\tau.
```

### Proof-completeness check (required workflow)
1. Piecewise decomposition of $(1-w)_+$ and $(1+\beta w)_+$ by sign conditions.
2. Expansion on middle interval:
   $(1-\alpha)(1-w)+\alpha(1+\beta w)=1+w(\alpha\beta-(1-\alpha))$.
3. Slope sign in middle interval uses exactly $\beta>(1-\alpha)/\alpha$.
4. $0$-$1$ risk cases derive from inequalities $w\le0$ and $-\beta w\le0$.
5. Final parameter choice for $(\varepsilon,\tau)$ tracks strict inequality $1-\alpha>\tau$.

### AI suggestion log (required workflow)
- Rejected suggestion: "take $\beta=(1-\alpha)/\alpha$."
  Why rejected: that makes the middle slope zero (non-unique minimizers), while the prompt asks to characterize minimizers cleanly under strict inequality.

## B3. Fixed-Feature Parity Barrier: Proof and Tightness
### Universally quantified objects and adversarial choices
- Universal feature map: $\phi:\{-1,+1\}^n\to\mathbb R^D$.
- Universal subsets: for every $S\subseteq[n]$, parity $\chi_S(x)=\prod_{i\in S}x_i$.
- Assumption: for every $S$, there exists $w_S\in\mathbb R^D$ with

```math
\forall x\in\{-1,+1\}^n,\quad \chi_S(x)=\langle w_S,\phi(x)\rangle.
```

### Lower bound: must have $D\ge 2^n$
Define matrix $M\in\mathbb R^{2^n\times 2^n}$ with rows indexed by $S\subseteq[n]$, columns indexed by $x\in\{-1,+1\}^n$, entries

```math
M_{S,x}=\chi_S(x).
```

Take two rows $S,T$.

```math
\langle M_{S,\cdot},M_{T,\cdot}\rangle
=\sum_{x}\chi_S(x)\chi_T(x)
=\sum_x \chi_{S\triangle T}(x).
```

If $S=T$, then $S\triangle T=\emptyset$ and sum is $2^n$.
If $S\neq T$, pick $j\in S\triangle T$; pairing each $x$ with $x'$ that flips coordinate $j$ gives cancellation
$\chi_{S\triangle T}(x')=-\chi_{S\triangle T}(x)$, so sum is $0$.
Thus rows are orthogonal and nonzero, hence linearly independent, so

```math
\mathrm{rank}(M)=2^n.
```

Now build factorization from representation assumption.
Let $W\in\mathbb R^{2^n\times D}$ have row $S$ equal to $w_S^\top$.
Let $\Phi\in\mathbb R^{D\times 2^n}$ have column $x$ equal to $\phi(x)$.
Then for each $(S,x)$,

```math
(W\Phi)_{S,x}=w_S^\top\phi(x)=\chi_S(x)=M_{S,x},
```

so $M=W\Phi$.
Rank submultiplicativity gives

```math
2^n=\mathrm{rank}(M)\le \min\{\mathrm{rank}(W),\mathrm{rank}(\Phi)\}\le D.
```

Therefore $D\ge 2^n$.

### Upper bound (tightness): construct $D=2^n$
Define feature map with one coordinate per subset:

```math
\phi(x)=\big(\chi_T(x)\big)_{T\subseteq[n]}\in\mathbb R^{2^n}.
```

For any target parity index $S$, choose weight vector $w_S=e_S$ (the standard basis vector at coordinate $S$).
Then

```math
\langle w_S,\phi(x)\rangle = \chi_S(x)
```

for all $x$, exact equality.
So every parity is represented with $D=2^n$, matching the lower bound.

Connection to Week 5: fixed-feature convex optimization can be statistically and computationally clean in parameter space, but for rich classes (all parities) the required feature dimension can be exponential.

### Proof-completeness check (required workflow)
1. Orthogonality identity uses $\chi_S\chi_T=\chi_{S\triangle T}$.
2. Off-diagonal inner-product cancellation uses explicit sign-flip involution on one coordinate in $S\triangle T$.
3. Diagonal norm gives $2^n$ exactly.
4. Rank step uses exact factorization $M=W\Phi$ and rank inequality $\mathrm{rank}(AB)\le\min(\mathrm{rank}(A),\mathrm{rank}(B))$.

Boundary-case audit:
- $n=0$: one parity and one input point, so $D\ge1=2^0$, tight.

### AI suggestion log (required workflow)
- Rejected suggestion: "argue only by counting functions."
  Why rejected: counting alone does not prove exact linear representation dimension; the assignment explicitly asks for the rank/orthogonality argument.

## B4. Same Predictors, Different Optimization Geometry
Given sample $S=((x_1,y_1),\dots,(x_n,y_n))$, $x_i\in\mathbb R^d$, $y_i\in\mathbb R$.

Linear model:

```math
f_w(x)=\langle w,x\rangle,\qquad
\hat R_{\mathrm{lin}}(w)=\frac1n\sum_{i=1}^n(\langle w,x_i\rangle-y_i)^2.
```

Two-layer linear network (one hidden unit):

```math
f_{a,b}(x)=a\langle b,x\rangle,\qquad
\hat R_{\mathrm{net}}(a,b)=\frac1n\sum_{i=1}^n\big(a\langle b,x_i\rangle-y_i\big)^2.
```

### Claim 1: same predictor class
For any $(a,b)$, define $w=ab$ (scalar-times-vector). Then

```math
f_{a,b}(x)=a\langle b,x\rangle=\langle ab,x\rangle=\langle w,x\rangle.
```

For any $w$, choose $a=1$, $b=w$, then $f_{a,b}=f_w$.
So the represented function sets are identical.

### Claim 2: $\hat R_{\mathrm{lin}}$ is convex in $w$
Each term $(\langle w,x_i\rangle-y_i)^2$ is a convex quadratic in $w$ (Hessian $2x_ix_i^\top\succeq0$).
Average of convex functions is convex, hence $\hat R_{\mathrm{lin}}$ is convex.

### Claim 3: $\hat R_{\mathrm{net}}$ is not necessarily convex in $(a,b)$
Concrete dataset: $d=1$, one sample $(x_1,y_1)=(1,1)$.
Then

```math
\hat R_{\mathrm{net}}(a,b)=(ab-1)^2.
```

Take points

```math
\theta_1=(a,b)=(0,0),\qquad \theta_2=(2,2).
```

Compute:

```math
\hat R_{\mathrm{net}}(\theta_1)=(0\cdot0-1)^2=1,\quad
\hat R_{\mathrm{net}}(\theta_2)=(2\cdot2-1)^2=9.
```

Midpoint:

```math
\bar\theta=\frac{\theta_1+\theta_2}{2}=(1,1),\qquad
\hat R_{\mathrm{net}}(\bar\theta)=(1\cdot1-1)^2=0.
```

Jensen convexity would require

```math
\hat R_{\mathrm{net}}(\bar\theta)\le \frac{\hat R_{\mathrm{net}}(\theta_1)+\hat R_{\mathrm{net}}(\theta_2)}2=5,
```

which is true, so this pair does not violate convexity. Use a pair that does:

```math
\theta_1=(-1,-1),\qquad \theta_2=(1,1).
```

Then

```math
\hat R_{\mathrm{net}}(\theta_1)=((-1)(-1)-1)^2=0,\quad
\hat R_{\mathrm{net}}(\theta_2)=(1\cdot1-1)^2=0.
```

Midpoint $\bar\theta=(0,0)$ gives

```math
\hat R_{\mathrm{net}}(\bar\theta)=(0\cdot0-1)^2=1
> \frac{0+0}{2}=0.
```

This is a Jensen inequality violation, so $\hat R_{\mathrm{net}}$ is non-convex in $(a,b)$.

### Claim 4: factorizations of a linear minimizer are global minimizers of network objective
Let $w^\star$ minimize $\hat R_{\mathrm{lin}}$.
For any factorization $w^\star=ab$, define $(a,b)$ accordingly.
For every sample $i$,

```math
a\langle b,x_i\rangle = \langle ab,x_i\rangle = \langle w^\star,x_i\rangle.
```

Hence

```math
\hat R_{\mathrm{net}}(a,b)=\hat R_{\mathrm{lin}}(w^\star).
```

Also, for any $(\tilde a,\tilde b)$ with $\tilde w=\tilde a\tilde b$,

```math
\hat R_{\mathrm{net}}(\tilde a,\tilde b)=\hat R_{\mathrm{lin}}(\tilde w)\ge \hat R_{\mathrm{lin}}(w^\star)=\hat R_{\mathrm{net}}(a,b).
```

So every factorization of $w^\star$ is a global minimizer of $\hat R_{\mathrm{net}}$.

Interpretation: learning features/parameterization can introduce non-convex optimization geometry even when the induced predictor class is unchanged.

### AI suggestion log (required workflow)
- Rejected suggestion: "use only Hessian determinant at one point to claim global non-convexity."
  Why rejected: assignment explicitly asks for a concrete Jensen violation dataset/example.

## Part B Sign/Operator Audit
Checked all key inequalities and operators in final arguments:
- B1: $\ge,\le,+,-$ in LP constraints and objective.
- B2: piecewise boundaries $w\le -1/\beta$, $-1/\beta\le w\le 1$, $w\ge 1$; slope sign comparisons; strict $>$ condition on $\beta$.
- B3: orthogonality $=0$, diagonal norm $=2^n$, rank inequality $\le$.
- B4: Jensen violation strict $>$ at midpoint and minimization inequalities.

# Part C. AI Usage Report

## C1. Where I Used AI
I used AI assistance throughout this assignment as a collaborator for proof planning, algebra checking, experiment design, and exposition. In Part A, I used AI to help structure the Set Cover reduction, check the threshold arithmetic with the repeated negative examples, and design a small synthetic experiment comparing sparse $0$-$1$ search with a convex surrogate method. In Part B, I used AI to help organize the LP formulation, check the piecewise hinge-risk calculation, outline the parity-rank proof, and find a concrete Jensen violation for the non-convex parameterization example.

I did not use AI as an oracle for final correctness. After drafting each proof, I checked the inequality steps, constants, and boundary cases myself against the assignment statement.

## C2. Concrete AI Suggestions I Accepted
One useful AI suggestion was to use $B=k+1$ repeated negative examples in the Set Cover reduction. I accepted this because it creates a clean gap: missing even one universe element loses $B=k+1$ correct negative examples, which cannot be compensated by changing at most $k$ positive-example mistakes. The key inequality becomes

```math
B(n-c)\le k-t,
```

and if $c<n$, then $B(n-c)\ge k+1>k\ge k-t$, which gives the contradiction.

Another accepted suggestion was to prove the parity lower bound using the matrix $M_{S,x}=\chi_S(x)$ and row orthogonality. I accepted this because it directly matches the hint and proves a dimension lower bound through rank, rather than relying on a weaker counting argument.

For the experiment, I accepted the suggestion to report both runtime and empirical agreement, because the point of Part A is not only predictive performance but also the statistical/computational distinction.

## C3. Concrete AI Suggestions I Rejected or Modified
I rejected an early suggestion to use only a counting-functions argument for the parity barrier. Counting does not prove the exact fixed-feature linear representation dimension requested in the problem. I replaced it with the orthogonality and rank factorization proof.

I also rejected a suggestion to set non-selected coordinates to positive values in the Set Cover reduction witness. That would generally make the vector dense and violate the $k$-sparsity requirement. I instead used $w_i=-1$ for selected sets and $w_i=0$ otherwise.

In Part B4, I modified an attempted non-convexity example. The first candidate pair satisfied Jensen's inequality instead of violating it. I replaced it with $\theta_1=(-1,-1)$ and $\theta_2=(1,1)$ for the one-sample dataset $(x,y)=(1,1)$, whose midpoint gives a strict violation:

```math
\hat R_{\mathrm{net}}(0,0)=1>\frac{0+0}{2}.
```

## C4. How I Verified Correctness
For proof sections, I verified correctness by expanding each important inequality step instead of absorbing constants into asymptotic notation. In Part A2, I explicitly tracked the repeated-example factor $B=k+1$ through the correct-label count and checked the implication from agreement back to a valid set cover. I also checked boundary cases such as empty universe, $k=0$, and elements that appear in no set.

For Part B1, I verified that every LP constraint is linear and that the slack variables reproduce the hinge loss at optimum. For Part B2, I recomputed the hinge risk on all three regions, checked the slopes, and separately computed the $0$-$1$ risks for $w<0$, $w=0$, and $w>0$. For Part B3, I checked row orthogonality and the rank factorization $M=W\Phi$. For Part B4, I checked the Jensen violation numerically and algebraically.

For the experiment, I verified the code by using synthetic data with a fixed sparse ground-truth vector and by averaging over multiple random seeds. I also checked whether the surrogate method returned a proper $k$-sparse classifier by counting nonzero coordinates.

## C5. Updates to My AI Workflow
This assignment made me add more explicit proof checks to my workflow. In particular, I used a coverage map before drafting, logged rejected or modified AI suggestions for each major section, and added proof-completeness checks after the main generated proofs. I also added a sign/operator audit at the end of Part B to catch mistakes in inequalities such as $\le$, $\ge$, and strict $>$ comparisons.

The most useful workflow change was forcing every lower-bound or reduction proof to first identify the universally quantified objects and the adversarial choices. That made the Set Cover reduction and parity lower bound easier to verify.

## C6. Where AI Helped the Most
AI helped the most with reduction design and proof organization. The hardest part of Part A was choosing the repeated-example threshold so that a classifier could not trade off uncovered elements against positive examples. The $B=k+1$ construction made that part clean. AI was also useful for organizing the parity proof into the matrix-rank structure requested by the hint.

## C7. One Plausible but Incomplete or Wrong AI Answer
One plausible but wrong AI answer occurred in the non-convexity example for Part B4. The suggested pair $\theta_1=(0,0)$ and $\theta_2=(2,2)$ did not violate Jensen's inequality, because the midpoint had smaller risk:

```math
\hat R_{\mathrm{net}}(1,1)=0\le 5.
```

I caught this by directly substituting both endpoints and the midpoint into $\hat R_{\mathrm{net}}(a,b)=(ab-1)^2$. The corrected pair $\theta_1=(-1,-1)$ and $\theta_2=(1,1)$ has zero risk at both endpoints but risk $1$ at the midpoint, which gives the required strict Jensen violation.

## Part C Traceability Check
The report explicitly answers:
1. which parts used AI;
2. which suggestions were accepted and why;
3. which suggestions were rejected or modified and why;
4. how correctness was verified;
5. what changed in the AI workflow;
6. which part AI helped with most;
7. one plausible incomplete or wrong AI answer and the independent check that caught it.
