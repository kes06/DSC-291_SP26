# Part A · Sparse Linear Predictors and Model Selection

Notation: \(\mathcal X=\mathbb R^d\), \(\mathcal Y=\{-1,+1\}\), \(\mathcal H_k=\{x\mapsto \mathrm{sign}(\langle w,x\rangle):\|w\|_0\le k\}\), \(\mathcal H=\cup_{k=1}^d\mathcal H_k\), and \(S\sim\mathcal D^n\).

## A.0 Requirement Mapping
- A1 VC bound via supports: Section A1.
- A2 penalty-SRM oracle inequality: Section A2.
- A3 sparse-vs-dense sample complexity comparison: Section A3.
- A4 validation model-selection bound and comparison: Section A4.
- A5 brute-force computation/runtime discussion: Section A5.

## A1. VC dimension through supports
For each \(I\subseteq[d]\) with \(|I|=k\), define
\[
\mathcal H_I=\{x\mapsto \mathrm{sign}(\langle w,x\rangle):\mathrm{supp}(w)\subseteq I\}.
\]
Then
\[
\mathcal H_k=\bigcup_{I:|I|=k}\mathcal H_I,\qquad \#\{I:|I|=k\}=\binom{d}{k}.
\]
Growth function:
\[
\Pi_{\mathcal H_k}(n)\le \sum_{I:|I|=k}\Pi_{\mathcal H_I}(n)
\le \binom{d}{k}\max_I \Pi_{\mathcal H_I}(n).
\]
Each \(\mathcal H_I\) is homogeneous halfspaces in \(\mathbb R^k\), so by Sauer–Shelah
\[
\Pi_{\mathcal H_I}(n)\le \sum_{j=0}^k\binom{n}{j}\le (en/k)^k.
\]
Hence
\[
\Pi_{\mathcal H_k}(n)\le \binom{d}{k}(en/k)^k\le (ed/k)^k(en/k)^k.
\]
Setting \(m=\mathrm{VCdim}(\mathcal H_k)\) and using \(\Pi_{\mathcal H_k}(m)=2^m\):
\[
2^m\le (e^2dm/k^2)^k
\]
Taking logs:
\[
m\log 2\le k\log(e^2d/k^2)+k\log m
\]
so
\[
\frac{m}{k}\le \frac{1}{\log 2}\!\left(\log(e^2d/k^2)+\log m\right),
\]
and the RHS grows only logarithmically in \(m\), hence \(m\le C\,k\log(ed/k)\) for a universal constant \(C\). Therefore
\[
\boxed{\mathrm{VCdim}(\mathcal H_k)=O\!\big(k\log(ed/k)\big).}
\]

AI suggestion rejected/modified:
- Rejected: cite a black-box union-VC lemma only. Modified to explicit growth-function steps to match the hint.

## A2. Penalty-based SRM
Choose prior \((p_k)_{k=1}^d\), \(p_k>0\), \(\sum_k p_k\le 1\). For each \(k\), from A1:
\[
d_k:=\mathrm{VCdim}(\mathcal H_k)\le C_1 k\log(ed/k).
\]
A class-level SRM bound gives (simultaneously for all \(k,h\in\mathcal H_k\), w.p. \(1-\delta\)):
\[
L_{\mathcal D}(h)\le L_S(h)+2\sqrt{\frac{d_k+\log(1/p_k)+\log(1/\delta)}{n}},
\]
where the constant \(2\) can be replaced by the lecture-version constant (absorbed later into \(C\)).
Define
\[
\mathrm{pen}(k,n,\delta):=2\sqrt{\frac{C_1k\log(ed/k)+\log(1/p_k)+\log(1/\delta)}{n}}.
\]
Let
\[
\hat h\in\arg\min_{1\le k\le d,\ h\in\mathcal H_k}\{L_S(h)+\mathrm{pen}(k,n,\delta)\}.
\]
Then on the same event:
\[
\boxed{
L_{\mathcal D}(\hat h)\le
\inf_{1\le k\le d,\ h\in\mathcal H_k}
\left\{
L_{\mathcal D}(h)+
C\sqrt{\frac{k\log(ed/k)+\log(1/p_k)+\log(1/\delta)}{n}}
\right\}
}
\]
for a universal \(C\).

Interpretation of costs:
- \(k\log(ed/k)\): statistical price for choosing support coordinates (which sparse directions).
- \(\log(1/p_k)\): extra price for choosing the sparsity level \(k\) across models.

AI suggestion rejected/modified:
- Rejected: use \(p_k\equiv 1/d\) without discussion. Modified to keep general \(p_k\), as requested by the prompt.

## A3. Comparison with dense halfspaces
Assume \(\exists w^\star\) with \(\|w^\star\|_0\le s\) and \(L_{\mathcal D}(w^\star)\le \eta\). Plug \(k=s,h=w^\star\) in A2:
\[
L_{\mathcal D}(\hat h)\le \eta+
C\sqrt{\frac{s\log(ed/s)+\log(1/p_s)+\log(1/\delta)}{n}}.
\]
To guarantee \(L_{\mathcal D}(\hat h)\le \eta+\varepsilon\), it is sufficient that
\[
n\ \ge\ \frac{C^2}{\varepsilon^2}\Big(s\log(ed/s)+\log(1/p_s)+\log(1/\delta)\Big).
\]
For dense homogeneous halfspaces in \(\mathbb R^d\), VC dimension is \(\Theta(d)\), giving sample size
\[
n=\Theta\!\left(\frac{d+\log(1/\delta)}{\varepsilon^2}\right).
\]
Sparse SRM is smaller when
\[
s\log(ed/s)+\log(1/p_s)\ll d.
\]
In particular, if \(p_k\propto 1/k^2\), then \(\log(1/p_s)=O(\log s+\log\sum_{j=1}^d1/j^2)=O(\log s)\), so the dominant term is \(s\log(ed/s)\).

AI suggestion rejected/modified:
- Rejected: hide \(\log(1/p_s)\) inside \(O(\cdot)\). Modified to keep constants/terms explicit.

## A4. Validation as model selection
Split \(S\) into \(S_1,S_2\) of size \(n/2\). For each \(k\), fit
\[
w_k\in\arg\min_{\|w\|_0\le k}L_{S_1}(w),
\]
then select
\[
\hat k\in\arg\min_{1\le k\le d}L_{S_2}(w_k),\qquad \hat w:=w_{\hat k}.
\]
Condition on \(S_1\): candidates \(\{w_1,\dots,w_d\}\) are fixed, so validation is finite-class ERM over \(d\) hypotheses. With prob. \(1-\delta/2\) over \(S_2\),
\[
L_{\mathcal D}(\hat w)\le \min_k L_{\mathcal D}(w_k)+C_3\sqrt{\frac{\log(d/\delta)}{n/2}}.
\]
Also, with prob. \(1-\delta/2\) over \(S_1\), uniformly in \(k\):
\[
L_{\mathcal D}(w_k)\le \inf_{\|w\|_0\le k}L_{\mathcal D}(w)
+
C_4\sqrt{\frac{k\log(ed/k)+\log(d/\delta)}{n/2}}.
\]
Since \(1/(n/2)=2/n\), the extra factor \(\sqrt{2}\) is absorbed into constants. Therefore, by a union bound, with prob. \(1-\delta\):
\[
\boxed{
L_{\mathcal D}(\hat w)\le
\inf_{1\le k\le d,\ \|w\|_0\le k}
\left\{
L_{\mathcal D}(w)+
C\sqrt{\frac{k\log(ed/k)+\log(d/\delta)}{n}}
\right\}.
}
\]

Comparison to penalty-SRM:
- Penalty-SRM: same sample used for fitting and choosing \(k\); pays \(\log(1/p_k)\) model-index cost.
- Validation: \(S_1\) fits predictors, \(S_2\) chooses \(k\); pays finite-choice cost \(\log d\) and a factor from sample split.

AI suggestion rejected/modified:
- Rejected: treat \(\{w_k\}\) as independent of \(S_1\). Modified by conditioning on \(S_1\) before applying finite-class bound.

## A5. Computation in realizable case
Assume there exists a \(k\)-sparse consistent homogeneous halfspace for the sample.

Brute force algorithm:
1. Enumerate all supports \(I\subseteq[d]\), \(|I|=k\) (there are \(\binom dk\)).
2. Restrict each sample \(x_i\) to coordinates in \(I\), obtaining points in \(\mathbb R^k\).
3. Solve feasibility: find \(u\in\mathbb R^k\) such that \(y_i\langle u,x_i^{(I)}\rangle>0\) for all \(i\) (or non-strict with margin slack/LP reformulation).
4. If feasible, lift \(u\) back to \(w\in\mathbb R^d\) with support \(I\), output \(w\).

If feasibility per support costs \(T(n,k)\) (polynomial in \(n,k\)), total runtime is
\[
O\!\left(\binom dk\,T(n,k)\right)\approx O\!\left((ed/k)^k\,T(n,k)\right).
\]
So it is polynomial in \(d\) when \(k=O(1)\), quasi-polynomial/subexponential for \(k=\Theta(\log d)\), and exponential in \(d\) when \(k=\Theta(d^\alpha)\) (\(\alpha>0\)).

This illustrates Week 4: sample complexity can be small (depends on \(k\log(ed/k)\)) while exact computation can still be intractable due to support search.

AI suggestion rejected/modified:
- Rejected: call runtime “polynomial” for all \(k\). Modified to explicit dependence via \(\binom dk\).

## A6. Traceability pass for Part A
- A1 support-union and growth-function combination: done in A1.
- A2 SRM oracle inequality with instantiated terms and interpretation: done in A2.
- A3 sparse-vs-dense sample-size comparison and regime statement: done in A3.
- A4 validation oracle inequality and comparison with penalty-SRM: done in A4.
- A5 brute-force algorithm, runtime, and computational-vs-statistical discussion: done in A5.

References: Sauer (1972), Shelah (1972), Hoeffding (1963), McDiarmid (1989).

---

# Part B · PAC-Bayes for Thresholds

We use the notation from the prompt:
\[
\mathcal X_N=\{1,2,\dots,N\},\quad \mathcal Y=\{0,1\},\quad
\mathcal H_N=\{h_t:t\in\{1,\dots,N+1\}\},\quad h_t(x)=\mathbf 1[x\ge t].
\]
In Part B we are in the realizable setting.

## B.0 Requirement Mapping (assignment bullet \(\to\) section)
- B1 (VC dimension and point posterior): Sections B1.1-B1.4.
- B2 (version space form, size, KL, empirical risk, interpretation): Sections B2.1-B2.5.
- B3 (risk formula for uniform posterior on \(W\), concrete example, why no contradiction): Sections B3.1-B3.4.
- B4 (fixed prior attack, probability event, unique consistent threshold, KL lower bound, interpretation): Sections B4.1-B4.6.

## B1. VC dimension and point-posterior PAC-Bayes

### B1.1 Prove \(\mathrm{VCdim}(\mathcal H_N)=1\)
Lower bound \(\ge 1\): a single point \(\{x\}\) can be labeled both ways by choosing
\(t=x\) (label 1) and \(t=x+1\) (label 0).

Upper bound \(\le 1\): no two-point set can be shattered. Let \(x_1<x_2\). For any threshold classifier, if \(h_t(x_1)=1\), then automatically \(h_t(x_2)=1\). So labeling \((1,0)\) on \((x_1,x_2)\) is impossible. Therefore no size-2 set is shattered.

Hence
\[
\boxed{\mathrm{VCdim}(\mathcal H_N)=1.}
\]

### B1.2 Point posterior KL
Let \(P\) be uniform on \(\mathcal H_N\), so
\[
P(h_t)=\frac1{N+1}\quad\forall t.
\]
Let ERM return a consistent \(\hat h_t\), and set
\[
Q_S=\delta_{\hat h_t}.
\]
Then
\[
\mathrm{KL}(Q_S\|P)
=\sum_h Q_S(h)\log\frac{Q_S(h)}{P(h)}
=\log\frac1{P(\hat h_t)}
=\log(N+1).
\]

### B1.3 Plug into PAC-Bayes bound
Using the lecture bound in the prompt,
\[
L_\mathcal D(Q)
\le L_S(Q)+\sqrt{\frac{\mathrm{KL}(Q\|P)+\log\frac{2n}{\delta}}{2(n-1)}}.
\]
For \(Q_S=\delta_{\hat h_t}\), realizability plus consistency gives \(L_S(Q_S)=0\), hence
\[
\boxed{
L_\mathcal D(Q_S)
\le
\sqrt{\frac{\log(N+1)+\log\frac{2n}{\delta}}{2(n-1)}}.
}
\]

### B1.4 Why this scales with \(\log(N+1)\)
The point posterior commits all mass to one threshold, so the KL term pays a coding cost of identifying one hypothesis among \(N+1\) possibilities, namely \(\log(N+1)\). VC-style realizable guarantees for thresholds depend on VC dimension \(=1\), not on the domain size \(N\), so they do not carry this \(\log N\) dependence.

### B1.5 AI suggestion rejected/modified
- Rejected suggestion: state \(\mathrm{VCdim}(\mathcal H_N)=1\) without proving non-shatterability of two points.
- Reason: the assignment asks for a proof, so the monotonic-threshold argument on \(x_1<x_2\) is written explicitly.

## B2. Version-space posterior

Define
\[
a(S)=\max\{x_i:y_i=0\},\ a(S)=0\text{ if no negatives},
\]
\[
b(S)=\min\{x_i:y_i=1\},\ b(S)=N+1\text{ if no positives}.
\]

### B2.1 Characterize consistent thresholds
A threshold \(h_t\) is consistent iff it predicts 0 on every negative and 1 on every positive.

For a negative point \(x_i\) (label 0), consistency means
\[
h_t(x_i)=\mathbf1[x_i\ge t]=0 \iff x_i<t.
\]
So we must have \(t>a(S)\).

For a positive point \(x_i\) (label 1), consistency means
\[
h_t(x_i)=\mathbf1[x_i\ge t]=1 \iff x_i\ge t.
\]
So we must have \(t\le b(S)\).

Combining both,
\[
V(S)=\{t: a(S)<t\le b(S)\}.
\]
Therefore
\[
|V(S)|=b(S)-a(S).
\]
Edge cases are consistent with this formula: if there are no negatives then \(a(S)=0\) and only \(t\le b(S)\) is required; if there are no positives then \(b(S)=N+1\) and only \(t>a(S)\) is required.

### B2.2 Uniform posterior on version space
Let
\[
Q_V(h_t)=\begin{cases}
\frac1{|V(S)|}, & t\in V(S),\\
0,&t\notin V(S).
\end{cases}
\]
Prior is uniform: \(P(h_t)=1/(N+1)\).

Then
\[
\mathrm{KL}(Q_V\|P)
=\sum_{t\in V(S)}\frac1{|V(S)|}\log\frac{1/|V(S)|}{1/(N+1)}
=\log\frac{N+1}{|V(S)|}.
\]

### B2.3 Show \(L_S(Q_V)=0\)
Every \(h_t\) with \(t\in V(S)\) is consistent with \(S\), so \(L_S(h_t)=0\).
Hence
\[
L_S(Q_V)=\mathbb E_{h\sim Q_V}[L_S(h)]=0.
\]

### B2.4 Why this can improve the PAC-Bayes certificate
For point posterior \(\delta_{\hat h}\): \(\mathrm{KL}=\log(N+1)\).
For version posterior \(Q_V\): \(\mathrm{KL}=\log((N+1)/|V(S)|)\).
If \(|V(S)|\) is large, then
\[
\log\frac{N+1}{|V(S)|}\ll \log(N+1),
\]
so the complexity term in PAC-Bayes is smaller.

### B2.5 AI suggestion rejected/modified
- Rejected suggestion: claim \(|V(S)|=b(S)-a(S)+1\).
- Reason: thresholds are indexed by integers with strict/weak inequalities \(a(S)<t\le b(S)\), so the exact count is \(b(S)-a(S)\).

## B3. Spreading helps KL, but can hurt true risk

Assume realizable \(\mathcal D\): \(X\sim\mathrm{Unif}(\{1,\dots,N\})\), and labels are generated by \(h_\tau\).
For nonempty \(W\subseteq\{1,\dots,N+1\}\), let \(Q_W\) be uniform on \(\{h_t:t\in W\}\).

### B3.1 Compute \(L_\mathcal D(Q_W)\)
For fixed \(t\), \(L_\mathcal D(h_t)\) equals disagreement probability between \(h_t\) and \(h_\tau\):
\[
L_\mathcal D(h_t)=\frac1N\,\big|\{x\in\{1,\dots,N\}:h_t(x)\neq h_\tau(x)\}\big|.
\]
If \(t\ge \tau\), disagreement occurs on \(x\in\{\tau,\dots,t-1\}\), count \(t-\tau\).
If \(t<\tau\), disagreement occurs on \(x\in\{t,\dots,\tau-1\}\), count \(\tau-t\).
So in all cases,
\[
L_\mathcal D(h_t)=\frac{|t-\tau|}{N}.
\]
Averaging under \(Q_W\):
\[
L_\mathcal D(Q_W)
=\frac1{|W|}\sum_{t\in W}L_\mathcal D(h_t)
=\frac1{N|W|}\sum_{t\in W}|t-\tau|.
\]
This is exactly the required formula.

### B3.2 Concrete example (\(N\ge 20\))
Take
\[
N=20,\quad \tau=11.
\]
Take realizable sample
\[
S=\{(1,0),(20,1)\}.
\]
This is realizable by \(h_{11}\) since \(1<11\Rightarrow y=0\), \(20\ge 11\Rightarrow y=1\).

For this sample,
\[
a(S)=1,\quad b(S)=20,
\]
so
\[
V(S)=\{2,3,\dots,20\},\quad |V(S)|=19
\]
(large).

KL comparison under uniform prior on \(N+1=21\) thresholds:
\[
\mathrm{KL}(Q_{V(S)}\|P)=\log\frac{21}{19},
\]
while
\[
\mathrm{KL}(\delta_{h_\tau}\|P)=\log 21.
\]
Hence
\[
\mathrm{KL}(Q_{V(S)}\|P)<\mathrm{KL}(\delta_{h_\tau}\|P).
\]

Risk comparison:
\[
L_\mathcal D(\delta_{h_\tau})=0
\]
(since \(h_\tau\) is Bayes/realizable truth), but
\[
L_\mathcal D(Q_{V(S)})
=\frac1{20\cdot 19}\sum_{t=2}^{20}|t-11|
=\frac{90}{380}
=\frac9{38}
>0.
\]
So the required strict inequality holds.

### B3.3 Why this does not contradict PAC-Bayes
PAC-Bayes gives an upper bound on true risk, not a guarantee that lower KL implies lower true risk for every posterior. A spread posterior can reduce KL but still average in many inaccurate hypotheses, increasing \(L_\mathcal D\). No contradiction occurs because the theorem compares each posterior to its own bound; it does not totally order posteriors by true risk via KL alone.

### B3.4 AI suggestion rejected/modified
- Rejected suggestion: use a non-realizable sample to make \(|V(S)|\) large.
- Reason: the question explicitly requires a realizable sample, so the example was chosen to be consistent with \(h_\tau\).

## B4. Every fixed prior can be attacked

Let any prior \(P\) over \(\mathcal H_N\) be fixed before data; assume \(N\ge 3\).

### B4.1 Find an internal threshold with small prior mass
There are \(N-1\) internal thresholds \(\{2,\dots,N\}\). Their masses sum to at most 1:
\[
\sum_{t=2}^N P(h_t)\le 1.
\]
By averaging/pigeonhole, there exists
\[
\tau\in\{2,\dots,N\}\quad\text{such that}\quad P(h_\tau)\le \frac1{N-1}.
\]

### B4.2 Define adversarial realizable distribution
Define \(\mathcal D_\tau\) on two points:
\[
\Pr[(x,y)=(\tau-1,0)]=\frac12,
\qquad
\Pr[(x,y)=(\tau,1)]=\frac12.
\]
This is realizable by threshold \(h_\tau\).

### B4.3 Probability sample contains both support points
For \(S\sim \mathcal D_\tau^n\), event “miss \((\tau-1,0)\)” has probability \((1/2)^n\). Same for “miss \((\tau,1)\)”. By union bound,
\[
\Pr[\text{at least one support point missing}]
\le 2\cdot\left(\frac12\right)^n
=2^{1-n}.
\]
Therefore
\[
\Pr[\text{both support points appear}]
\ge 1-2^{1-n}.
\]

### B4.4 On this event, \(V(S)=\{\tau\}\)
If both points appear, consistency requires:
- \(h_t(\tau-1)=0\Rightarrow \tau-1<t\),
- \(h_t(\tau)=1\Rightarrow t\le \tau\).
Hence
\[
\tau-1<t\le \tau.
\]
Since \(t\) is integer, uniquely \(t=\tau\). So
\[
V(S)=\{\tau\}.
\]

### B4.5 Consequence for zero-empirical-error posteriors and KL
If \(L_S(Q)=0\), every hypothesis in support of \(Q\) must be consistent with all sample points. But on this event only \(h_\tau\) is consistent, so
\[
Q=\delta_{h_\tau}.
\]
Justification of the first sentence: \(L_S(Q)=\mathbb E_{h\sim Q}[L_S(h)]=0\) with \(L_S(h)\ge 0\) for all \(h\), so any \(h\) with \(Q(h)>0\) must satisfy \(L_S(h)=0\) (otherwise the expectation would be strictly positive).
Then
\[
\mathrm{KL}(Q\|P)=\log\frac1{P(h_\tau)}
\ge \log(N-1).
\]
So on that event, for every zero-training-error posterior,
\[
\boxed{\mathrm{KL}(Q\|P)\ge \log(N-1).}
\]

### B4.6 What this does and does not show
It shows a limitation of fixed-prior, zero-empirical-error PAC-Bayes certificates: for some realizable distributions, the KL term is inevitably large. It does not show a sample-complexity lower bound for learning thresholds; thresholds still have VC dimension 1 and are learnable with sample complexity independent of \(N\) (up to \(\varepsilon,\delta\) terms). The result is about certificate tightness under this proof template, not impossibility of learning.

### B4.7 AI suggestion rejected/modified
- Rejected suggestion: conclude this proves thresholds need \(\Omega(\log N)\) more samples.
- Reason: that conclusion is false; the argument lower-bounds a PAC-Bayes KL certificate for fixed prior and zero training error, not the true PAC sample complexity.

## B5. Traceability pass for Part B
- B1 VC dimension proof and point-posterior PAC-Bayes: done in B1.1-B1.4.
- B2 version-space form, cardinality, exact KL, and \(L_S(Q_V)=0\): done in B2.1-B2.3.
- B2 interpretation (why version posterior can improve bound): done in B2.4.
- B3 exact formula for \(L_\mathcal D(Q_W)\): done in B3.1.
- B3 concrete \(N\ge 20\) example satisfying both inequalities: done in B3.2.
- B3 explanation of no contradiction: done in B3.3.
- B4 existence of internal \(\tau\) with small prior mass: done in B4.1.
- B4 high-probability event \(\ge 1-2^{1-n}\): done in B4.3.
- B4 uniqueness \(V(S)=\{\tau\}\), zero-error posterior characterization, and KL lower bound: done in B4.4-B4.5.
- B4 interpretation (what it does/does not show): done in B4.6.

References: Hoeffding (1963), McDiarmid (1989), PAC-Bayes lecture theorem.

---

# Part C · AI Usage Report

I used AI in both Part A and Part B. I used it to check algebra and bound forms, and to help type and format my write-up. I treated AI as a collaborator, not as an oracle.

AI suggestions were used across the whole process: drafting structure, checking intermediate derivations, and revising for completeness. I ran follow-up checks on contradiction steps, sample-splitting factors, and edge cases.

One AI suggestion I rejected was in Part A.3: an earlier version hid terms such as \(\log(1/p_s)\) inside big-O notation too early. I rejected that and kept these terms explicit to match the assignment requirement.

I manually verified all final content before submission. In particular, I checked inequality transitions, sample-splitting denominators, edge cases, and sign/operator correctness in equations.

## Process improvements from this assignment
1. Add a proof-completeness checklist prompt after each AI draft: list every inequality/bound step and cite the theorem used.
2. Add a constant/normalization tracking step: explicitly track scaling factors and constants through to the final bound.
3. Add an edge-case checklist for set/interval characterizations (for example, no-positive or no-negative samples).
4. Separate derivation and interpretation passes: one pass for math steps, one pass for “what this shows vs. what it does not show.”
5. Add a final sign/operator check to ensure all \(+,\le,\ge\) symbols are present and correct.
