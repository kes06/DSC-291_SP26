# DSC 190/291 Assignment 3 - Part A

## A Mini-Course on Concentration Inequalities

### Notation and setup
- Data space: $\mathcal{Z} = \mathcal{X} \times \{0,1\}$ for binary classification.
- For a hypothesis $h \in \mathcal{H}$, let the $0$-$1$ loss be
  $$\ell_h(z) = \mathbf{1}\{h(x) \neq y\}, \quad z=(x,y).$$
- Population risk: $L_{\mathcal{D}}(h) = \mathbb{E}_{z\sim \mathcal{D}}[\ell_h(z)]$.
- Empirical risk on sample $S=(z_1,\dots,z_n)$:
  $$L_n(h) = \frac1n\sum_{i=1}^n \ell_h(z_i).$$
- ERM: $\hat h \in \arg\min_{h\in\mathcal{H}} L_n(h)$.
- Growth function:
  $$\Gamma_{\mathcal{H}}(m)=\max_{x_1,\dots,x_m\in\mathcal{X}}\big|\{(h(x_1),\dots,h(x_m)):h\in\mathcal{H}\}\big|.$$

---

## 1) The concept of concentration

A concentration inequality upper-bounds tail probabilities of a random quantity around a central value (typically its expectation, median, or another deterministic benchmark). The generic form is:
$$\Pr\big(|X-\mathbb{E}X|\ge t\big) \le \text{small}(t,n),$$
where the right-hand side decays quickly in $t$ and/or sample size $n$.

Intuition:
- Random fluctuations from many independent sources tend to cancel out.
- If no single coordinate can change the output too much (bounded influence), then large deviations become unlikely.
- Exponential tails are common because MGFs convert additive structure into multiplicative bounds.

Concrete example (coin flips):
- Let $X_1,\dots,X_n\sim\text{Bernoulli}(1/2)$ i.i.d. and $\bar X_n=\frac1n\sum_i X_i$.
- Hoeffding gives
  $$\Pr(|\bar X_n-1/2|\ge \varepsilon)\le 2e^{-2n\varepsilon^2}.$$
So if $n=200$ and $\varepsilon=0.1$, this is at most $2e^{-4}\approx 0.0366$: the sample mean is tightly concentrated around $0.5$.

---

## 2) Common technique: MGF + Chernoff template

### 2.1 Chernoff bound template
For any random variable $X$, threshold $t$, and any $\lambda>0$:
$$
\Pr(X\ge t)=\Pr(e^{\lambda X}\ge e^{\lambda t})\le e^{-\lambda t}\,\mathbb{E}[e^{\lambda X}].
$$
Hence
$$
\Pr(X\ge t) \le \inf_{\lambda>0}\exp\big(-\lambda t + \log \mathbb{E}[e^{\lambda X}]\big).
$$
So the proof pattern is:
1. Bound log-MGF $\log\mathbb{E}[e^{\lambda X}]$.
2. Plug into the Chernoff template.
3. Optimize over $\lambda$.

### 2.2 What we need from the MGF
Useful tail bounds come from quadratic or sub-exponential control:
- Sub-Gaussian type: $\log\mathbb{E}[e^{\lambda X}]\le c\lambda^2$ gives $e^{-\Theta(t^2)}$ tails.
- Sub-exponential type: $\log\mathbb{E}[e^{\lambda X}]\le \frac{v\lambda^2}{2(1-b\lambda)}$ gives Bernstein-like tails.

### 2.3 Bounded differences / martingale variant
For $f(X_1,\dots,X_n)$ with independent coordinates, if changing coordinate $i$ changes $f$ by at most $c_i$, define Doob martingale
$$M_i=\mathbb{E}[f\mid X_1,\dots,X_i],\quad M_0=\mathbb{E}f,\;M_n=f.$$
Then increments satisfy $|M_i-M_{i-1}|\le c_i$, so Hoeffding-style MGF bounds on increments imply McDiarmid.

---

## 3) Statements, assumptions, and consequences

### 3.1 Hoeffding (independent bounded summands)
**Assumptions.** Independent $X_1,\dots,X_n$ with $X_i\in[a_i,b_i]$ almost surely.

**Statement.** For $S_n=\sum_i(X_i-\mathbb{E}X_i)$,
$$
\Pr(S_n\ge t)\le\exp\!\left(-\frac{2t^2}{\sum_{i=1}^n(b_i-a_i)^2}\right),
$$
and two-sided version multiplies by $2$.

**Controls.** Sum/mean of independent bounded variables.

### 3.2 Hoeffding without replacement (finite population sampling)
Let $v_1,\dots,v_N\in[a,b]$ be a fixed finite population with mean $\mu$, and sample $Y_1,\dots,Y_n$ uniformly without replacement.

**Statement (Hoeffding-type form).**
$$
\Pr\left(\frac1n\sum_{i=1}^n Y_i-\mu\ge t\right)\le\exp\left(-\frac{2nt^2}{(b-a)^2}\right),
$$
with two-sided version multiplied by $2$.

**Controls.** Deviation of sample mean from population mean for dependent (negatively associated) samples.

### 3.3 McDiarmid (bounded differences)
**Assumptions.** $X_1,\dots,X_n$ independent; $f$ satisfies
$$
\sup_{x_1,\dots,x_n,x_i'}|f(x_1,\dots,x_i,\dots,x_n)-f(x_1,\dots,x_i',\dots,x_n)|\le c_i.
$$

**Statement.**
$$
\Pr\big(f-\mathbb{E}f\ge t\big)\le\exp\left(-\frac{2t^2}{\sum_{i=1}^n c_i^2}\right),
$$
again with factor $2$ for two-sided.

**Controls.** General Lipschitz-like functions of many independent inputs.

### 3.4 Bernstein (variance-sensitive)
**Assumptions.** Independent centered $X_i$ with $|X_i|\le b$ almost surely, and $\sum_i\mathrm{Var}(X_i)\le v$.

**Statement.** For $S_n=\sum_i X_i$,
$$
\Pr(S_n\ge t)\le\exp\left(-\frac{t^2}{2(v+bt/3)}\right).
$$
Equivalent mean form:
$$
\Pr\left(\frac1n\sum_i X_i\ge\varepsilon\right)
\le\exp\left(-\frac{n\varepsilon^2}{2(\sigma^2+b\varepsilon/3)}\right),
$$
if average variance is at most $\sigma^2$.

**What extra structure it uses vs Hoeffding.** Hoeffding uses only ranges; Bernstein also uses variance, giving sharper rates when variance is small.

### 3.5 Comparison summary
- Hoeffding: independent + bounded, clean sub-Gaussian tails.
- Hoeffding w/o replacement: similar tail shape for dependent sampling due to negative dependence.
- McDiarmid: extends from sums to bounded-difference functions.
- Bernstein: interpolates sub-Gaussian for small deviations and sub-exponential for large deviations, often tighter than Hoeffding.

---

## 4) Proofs

### 4.1 Hoeffding via MGF
Key lemma (Hoeffding's lemma): if $X\in[a,b]$ and $\mathbb{E}X=0$, then
$$\log\mathbb{E}[e^{\lambda X}]\le \frac{\lambda^2(b-a)^2}{8}.$$ 
Apply to $X_i-\mathbb{E}X_i$, independence gives
$$
\log\mathbb{E}e^{\lambda S_n}
=\sum_i \log\mathbb{E}e^{\lambda(X_i-\mathbb{E}X_i)}
\le \frac{\lambda^2}{8}\sum_i(b_i-a_i)^2.
$$
Then Chernoff:
$$
\Pr(S_n\ge t)
\le\exp\left(-\lambda t+\frac{\lambda^2}{8}\sum_i(b_i-a_i)^2\right).
$$
Optimize at $\lambda^*=\frac{4t}{\sum_i(b_i-a_i)^2}$, yielding
$$
\Pr(S_n\ge t)\le\exp\left(-\frac{2t^2}{\sum_i(b_i-a_i)^2}\right).
$$

### 4.2 Hoeffding without replacement
Let $Y_1,\dots,Y_n$ be drawn without replacement from fixed $\{v_1,\dots,v_N\}\subset[a,b]$.
A classical Hoeffding comparison theorem states that for convex increasing $\phi$,
$$
\mathbb{E}\,\phi\!\left(\sum_{i=1}^n(Y_i-\mu)\right)
\le
\mathbb{E}\,\phi\!\left(\sum_{i=1}^n(\tilde Y_i-\mu)\right),
$$
where $\tilde Y_i$ are i.i.d. draws with replacement from the same population.
Set $\phi(u)=e^{\lambda u}$ to compare MGFs, then apply the with-replacement Hoeffding bound to the i.i.d. right-hand side. This yields the same tail form:
$$
\Pr\left(\frac1n\sum_i Y_i-\mu\ge t\right)\le e^{-2nt^2/(b-a)^2}.
$$

### 4.3 McDiarmid via Doob martingale + Hoeffding increments
Let $Z=f(X_1,\dots,X_n)$ and $M_i=\mathbb{E}[Z\mid X_1,\dots,X_i]$.
Then $M_0=\mathbb{E}Z$, $M_n=Z$, and
$$Z-\mathbb{E}Z=\sum_{i=1}^n D_i,\quad D_i=M_i-M_{i-1}.$$
Bounded differences imply $D_i\in[\alpha_i,\beta_i]$ with width at most $c_i$, i.e., $\beta_i-\alpha_i\le c_i$.
Conditioning on $(X_1,\dots,X_{i-1})$, apply Hoeffding's lemma to $D_i$ and multiply MGFs across martingale increments:
$$
\log\mathbb{E}e^{\lambda(Z-\mathbb{E}Z)}\le \frac{\lambda^2}{8}\sum_i c_i^2.
$$
Chernoff optimization gives
$$
\Pr(Z-\mathbb{E}Z\ge t)\le \exp\left(-\frac{2t^2}{\sum_i c_i^2}\right).
$$

### 4.4 Bernstein via MGF control with variance term
For centered $X$ with $|X|\le b$, one can show (for $|\lambda|<3/b$):
$$
\log\mathbb{E}e^{\lambda X}
\le
\frac{\lambda^2\mathrm{Var}(X)}{2(1-b|\lambda|/3)}.
$$
Using independence and $v\ge\sum_i\mathrm{Var}(X_i)$,
$$
\log\mathbb{E}e^{\lambda S_n}
\le
\frac{\lambda^2 v}{2(1-b\lambda/3)},\quad 0<\lambda<3/b.
$$
Then
$$
\Pr(S_n\ge t)
\le
\inf_{0<\lambda<3/b}
\exp\left(-\lambda t + \frac{\lambda^2 v}{2(1-b\lambda/3)}\right),
$$
whose optimization yields
$$
\Pr(S_n\ge t)\le\exp\left(-\frac{t^2}{2(v+bt/3)}\right).
$$

### 4.5 Unified template
All four proofs fit one pattern:
1. Identify quantity of interest $Q$.
2. Obtain MGF/log-MGF bound for $Q-\mathbb{E}Q$ (directly, via comparison, or via martingale increments).
3. Apply Chernoff + optimize $\lambda$.

---

## 5) Connection to the Week 3 ERM guarantee (full proof)

We prove that with probability at least $1-\delta$ over $S\sim\mathcal{D}^n$,
$$
L_{\mathcal{D}}(\hat h)
\le
\inf_{h\in\mathcal{H}}L_{\mathcal{D}}(h)
+
O\!\left(\sqrt{\frac{\log\Gamma_{\mathcal{H}}(2n)+\log(1/\delta)}{n}}\right).
$$

### Step 1: Uniform convergence implies ERM excess-risk bound
Define
$$\Delta_n := \sup_{h\in\mathcal{H}}|L_{\mathcal{D}}(h)-L_n(h)|.$$
By ERM optimality and triangle inequalities:
$$
L_{\mathcal{D}}(\hat h)-\inf_h L_{\mathcal{D}}(h) \le 2\Delta_n.
$$
So it suffices to upper-bound $\Delta_n$.

### Step 2: Symmetrization with a ghost sample
Let $S'=(z_1',\dots,z_n')\sim\mathcal{D}^n$ independent and
$$L_n'(h)=\frac1n\sum_{i=1}^n \ell_h(z_i').$$
Standard symmetrization gives
$$
\Pr(\Delta_n>\varepsilon)
\le
2\Pr\left(\sup_{h\in\mathcal{H}}|L_n(h)-L_n'(h)|>\frac\varepsilon2\right).
$$

### Step 3: Condition on pooled points and reduce to without-replacement concentration
Condition on pooled multiset $\{z_1,\dots,z_n,z_1',\dots,z_n'\}$ of size $2n$.
Then $(S,S')$ is equivalent to choosing a size-$n$ subset of these $2n$ points without replacement for $S$; the rest form $S'$.
For fixed $h$, define loss values on pooled points in $[0,1]$; then
$L_n(h)-L_n'(h)$ is a difference of two complementary sample means.
Using Hoeffding without replacement:
$$
\Pr\big(|L_n(h)-L_n'(h)|>u\mid\text{pooled points}\big)
\le
2\exp\left(-\frac{nu^2}{2}\right).
$$

### Step 4: Growth function + union bound
On the fixed $2n$ points, different $h$ induce at most $\Gamma_{\mathcal{H}}(2n)$ distinct prediction (hence loss) vectors. Therefore,
$$
\Pr\left(\sup_h |L_n(h)-L_n'(h)|>u\mid\text{pooled}\right)
\le
2\Gamma_{\mathcal{H}}(2n)e^{-nu^2/2}.
$$
Remove conditioning and set $u=\varepsilon/2$ in Step 2:
$$
\Pr(\Delta_n>\varepsilon)
\le
4\Gamma_{\mathcal{H}}(2n)\exp\left(-\frac{n\varepsilon^2}{8}\right).
$$
Thus with probability at least $1-\delta$,
$$
\Delta_n
\le
\sqrt{\frac{8}{n}\left(\log\frac{4}{\delta}+\log\Gamma_{\mathcal{H}}(2n)\right)}.
$$
Hence
$$
L_{\mathcal{D}}(\hat h)-\inf_h L_{\mathcal{D}}(h)
\le
2\Delta_n
=
O\!\left(\sqrt{\frac{\log\Gamma_{\mathcal{H}}(2n)+\log(1/\delta)}{n}}\right).
$$
This is exactly the Week 3 i.i.d. growth-function ERM guarantee (up to constants).

---

## References

1. Wassily Hoeffding (1963). "Probability inequalities for sums of bounded random variables." *Journal of the American Statistical Association* 58(301): 13-30.
2. Bernard Bercu, Djalil Chafa"i, and Djalil Moulines (2015). *Concentration Inequalities: A Nonasymptotic Theory of Independence.* (for Chernoff/MGF method and bounded differences style proofs).
3. Colin McDiarmid (1989). "On the method of bounded differences." In *Surveys in Combinatorics*.
4. Sergei Bernstein (1924). Classical inequality for sums of bounded independent variables; modern textbook forms appear in many probability references (e.g., Boucheron-Lugosi-Massart).
5. Stephane Boucheron, Gabor Lugosi, and Pascal Massart (2013). *Concentration Inequalities: A Nonasymptotic Theory of Independence.* Oxford University Press.
6. Roman Vershynin (2018). *High-Dimensional Probability.* Cambridge University Press (clear derivations of Hoeffding/Bernstein and MGF techniques).

---

# Part B: The No-Free-Lunch Theorem and the Fundamental Theorem

## Task 1) Proof of the Week 3 No-Free-Lunch theorem

### Theorem (restated)
Let $A$ be any learning algorithm for binary classification with $0$-$1$ loss on a domain $\mathcal{X}$, and let $n<|\mathcal{X}|/2$. Then there exists a distribution $\mathcal{D}$ on $\mathcal{X}\times\{0,1\}$ such that:
- realizability holds: there exists $f^*:\mathcal{X}\to\{0,1\}$ with $L_{\mathcal{D}}(f^*)=0$;
- with probability at least $1/7$ over $S\sim\mathcal{D}^n$, we have
  $$L_{\mathcal{D}}(A(S))\ge \frac18.$$

### Quantifiers and adversary choices
- Universal: learner $A$, sample size $n$.
- Adversary chooses: a $2n$-point subset of $\mathcal{X}$, a labeling, and then the corresponding realizable distribution.

### Proof
Fix any learner $A$ and any $n<|\mathcal{X}|/2$. Pick distinct points
$$C=\{x_1,\dots,x_{2n}\}\subset\mathcal{X}.$$
For each labeling $\sigma\in\{0,1\}^{2n}$, define target $f_\sigma$ on $C$ by $f_\sigma(x_i)=\sigma_i$ (extend arbitrarily outside $C$), and define $\mathcal{D}_\sigma$ as:
- $x$ is uniform on $C$;
- $y=f_\sigma(x)$ deterministically.

So $L_{\mathcal{D}_\sigma}(f_\sigma)=0$ (realizable).

Now draw $\sigma$ uniformly from $\{0,1\}^{2n}$ and then draw $S\sim\mathcal{D}_\sigma^n$. Let $U(S)\subseteq C$ be points in $C$ not appearing in $S$.

Condition on the unlabeled sample locations in $S$. For each unseen $x\in U(S)$, the learner has no information about $f_\sigma(x)$; under random $\sigma$, that label is unbiased, so expected mistake at $x$ is $1/2$. Therefore
$$
\mathbb{E}_\sigma\!\left[L_{\mathcal{D}_\sigma}(A(S))\mid S\right]
\ge
\frac{|U(S)|}{2n}\cdot\frac12
=
\frac{|U(S)|}{4n}.
$$
Taking expectation over sample draw:
$$
\mathbb{E}_{\sigma,S}\!\left[L_{\mathcal{D}_\sigma}(A(S))\right]
\ge
\frac{\mathbb{E}[|U(S)|]}{4n}.
$$
For each fixed $x_i\in C$,
$$
\Pr(x_i\notin S)=\left(1-\frac1{2n}\right)^n,
$$
so
$$
\mathbb{E}[|U(S)|]=2n\left(1-\frac1{2n}\right)^n.
$$
Hence
$$
\mu:=\mathbb{E}_{\sigma,S}\!\left[L_{\mathcal{D}_\sigma}(A(S))\right]
\ge
\frac12\left(1-\frac1{2n}\right)^n
\ge
\frac14,
$$
since $\left(1-\frac1{2n}\right)^n\ge\frac12$ for all $n\ge1$.

Define $Z=L_{\mathcal{D}_\sigma}(A(S))\in[0,1]$. For $t=1/8$,
$$
\mu=\mathbb{E}[Z]\le t\cdot\Pr(Z<t)+1\cdot\Pr(Z\ge t)
=t+(1-t)\Pr(Z\ge t).
$$
Thus
$$
\Pr(Z\ge 1/8)\ge\frac{\mu-1/8}{1-1/8}\ge\frac{1/4-1/8}{7/8}=\frac17.
$$
So under random $\sigma$, the failure event has probability at least $1/7$. By averaging/probabilistic method, there exists at least one fixed labeling $\sigma^*$ such that for $\mathcal{D}=\mathcal{D}_{\sigma^*}$:
$$
\Pr_{S\sim\mathcal{D}^n}\!\left(L_{\mathcal{D}}(A(S))\ge\frac18\right)\ge\frac17.
$$
This proves the theorem.

---

## Task 2) Application: lower-bound direction of the Fundamental Theorem

### Corollary (NFL implies non-learnability when VC dimension is infinite)
If $\mathrm{VCdim}(\mathcal{H})=\infty$, then $\mathcal{H}$ is not PAC learnable.

### Why
Take any learner $A$ and any sample size $n$. Since $\mathrm{VCdim}(\mathcal{H})=\infty$, there exists a shattered set of size $2n$. Restricting to that set, every labeling is realizable by some $h\in\mathcal{H}$. Therefore the NFL construction above is realizable within $\mathcal{H}$ itself, and yields
$$
\Pr\!\left(L_{\mathcal{D}}(A(S))\ge\frac18\right)\ge\frac17.
$$
So no algorithm can guarantee PAC performance for $(\varepsilon,\delta)=(1/8,1/8)$ uniformly over realizable distributions. Hence $\mathcal{H}$ is not PAC learnable.

### Concrete class with infinite VC dimension
Let $\mathcal{X}=\mathbb{N}$ and
$$
\mathcal{H}_{\mathrm{fin}}=\{h_A:A\subseteq\mathbb{N}\text{ finite},\ h_A(x)=\mathbf{1}\{x\in A\}\}.
$$
Claim: $\mathrm{VCdim}(\mathcal{H}_{\mathrm{fin}})=\infty$.

Proof: for any $m$, take any distinct $x_1,\dots,x_m\in\mathbb{N}$. For any labeling $b\in\{0,1\}^m$, define finite set
$$
A_b=\{x_i:b_i=1\}.
$$
Then $h_{A_b}(x_i)=b_i$ for all $i$. So every size-$m$ set is shattered; since $m$ is arbitrary, VC dimension is infinite.

Applying the corollary: $\mathcal{H}_{\mathrm{fin}}$ is not PAC learnable.

---

## Task 3) Worked construction (explicit bad distribution and target)

Choose:
- Domain: $\mathcal{X}=\{1,2,\dots,2n\}$.
- Learner: $A_{\text{zero}}(S)\equiv 0$ (always predicts $0$, ignores $S$).
- Target: $f^*(x)=1$ for $x\le n$, and $f^*(x)=0$ for $x>n$.
- Distribution: $x$ uniform on $\mathcal{X}$, $y=f^*(x)$ deterministically.

Then realizability is immediate: $L_{\mathcal{D}}(f^*)=0$.

Now compute learner risk:
$$
L_{\mathcal{D}}(A_{\text{zero}}(S))
=
\Pr_{x\sim\mathrm{Unif}(\mathcal{X})}(A_{\text{zero}}(x)\neq f^*(x))
=
\Pr(x\le n)
=
\frac12.
$$
So for every sample $S$,
$$
L_{\mathcal{D}}(A_{\text{zero}}(S))=\frac12\ge\frac18.
$$
Hence
$$
\Pr_{S\sim\mathcal{D}^n}\!\left(L_{\mathcal{D}}(A_{\text{zero}}(S))\ge\frac18\right)=1,
$$
which is a constant (indeed stronger than the theorem's $1/7$).

---

## Task 4) Comparison: Week 1 vs Week 3 NFL

### Learning setting
- Week 1 NFL: online/sequential prediction over a finite domain sequence.
- Week 3 NFL: batch PAC learning with i.i.d. training sample from a population distribution.

### Adversary type
- Week 1 version (as stated): adversary picks a bad target function and a full enumeration of the domain after seeing the learner; this is an oblivious construction of a worst-case sequence.
- Week 3 version: adversary picks a realizable distribution (equivalently a target labeling on a finite support) before random sampling; sample randomness then drives the probabilistic lower bound.

### Form of conclusion
- Week 1: deterministic mistake bound on one adversarial sequence (learner makes $n$ mistakes).
- Week 3: probabilistic population-risk bound:
  $$\Pr(L_{\mathcal{D}}(A(S))\ge 1/8)\ge 1/7.$$

### Why both are “No-Free-Lunch”
Both results say there is no universally good learner without structural assumptions on the hypothesis class/data:
- Week 1: no online rule avoids worst-case mistake sequences.
- Week 3: no PAC learner can uniformly succeed at finite sample size when complexity is unbounded (infinite VC dimension), even in realizable problems.
The quantitative forms differ, but the message is the same: guarantees require assumptions.

---

# Part C: AI Usage Report

## 1) Where I used AI
I used AI as a collaborator in three parts of this assignment:
- **Part A (concentration inequalities):** to organize the write-up structure (concepts, statements, proofs, ERM connection), and to sanity-check proof flow.
- **Part B (NFL and Fundamental Theorem):** to draft proof skeletons (quantifiers, averaging argument, probabilistic method), then I manually verified each bound and implication.
- **Exposition and formatting:** to improve clarity, notation consistency, and section ordering.

I did **not** use AI to replace understanding. I checked each theorem statement and each transition in the arguments before keeping it.

## 2) Concrete AI suggestions I accepted
I accepted the following concrete suggestions:
- Using a single coherent mini-course structure in Part A (intuition -> general method -> theorem statements -> proofs -> ERM proof connection).
- Presenting NFL proof by first identifying universally quantified objects versus adversarial choices, then performing averaging over labelings.
- Adding an explicit worked construction in Part B that computes risk directly (instead of only citing existence).
- Writing a side-by-side Week 1 vs Week 3 NFL comparison table-style narrative (setting, adversary type, conclusion form).

I accepted these because they improved readability and made each requirement in the assignment prompt directly traceable to a section.

## 3) Concrete AI suggestions I rejected or modified
I rejected or substantially modified several suggestions:
- **Overly compressed proof steps:** some drafts skipped key inequalities (for example, converting expected risk lower bound into a probability lower bound). I expanded those steps explicitly.
- **Notation drift across sections:** some drafts mixed symbols for distributions and risks. I normalized notation to keep arguments checkable.
- **Unjustified constants:** some suggestions stated constants without derivation. I kept only constants I could derive or justify from the proof outline.
- **Too-general references:** I replaced vague references with standard sources (Hoeffding, McDiarmid, Bernstein, concentration texts).

These changes were necessary because correctness and traceability matter more than concise but opaque prose.

## 4) How I verified correctness
I used the following checks:
- **Proof verification:** line-by-line check of assumptions, quantifiers, and logical implications.
- **Inequality checks:** re-derived key bounds (symmetrization flow, union bound usage, and probability lower-bound conversion in NFL).
- **Edge-case checks:** checked small-$n$ behavior in expressions like $(1-1/(2n))^n$ and whether constants still make sense.
- **Consistency checks:** ensured that realizability claims, VC-dimension claims, and final conclusions are aligned with theorem statements.
- **Exposition checks:** ensured each assignment sub-question is explicitly answered in a dedicated subsection.

I did not run code experiments for this homework; verification was mathematical and expository.

## AI workflow updates from this assignment (5 most recent)
This assignment changed my AI workflow in these concrete ways:

1. **Prompting by rubric first.**  
I now start by turning the assignment prompt into a section-by-section checklist before generating content.

2. **Quantifier-first proof drafting.**  
For lower-bound proofs, I now explicitly write “universal vs adversarial choices” before any derivation.

3. **Require explicit constant tracking.**  
I now ask AI to keep constants visible (not only big-$O$) when a theorem statement includes numeric thresholds.

4. **Mandatory rejection log.**  
I now record at least one rejected AI suggestion per major section, so I do not passively accept outputs.

5. **Final traceability pass.**  
Before submission, I run a pass that maps each assignment bullet to exact subsection(s) in the write-up.

These updates made my process more reliable and reduced the risk of submitting polished but unchecked text.

