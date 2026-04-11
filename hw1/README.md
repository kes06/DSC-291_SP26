# HW1 Parts A-D

## Part A: Repository Setup

My GitHub repository for this course is:

[https://github.com/kes06/DSC-291_SP26](https://github.com/kes06/DSC-291_SP26)

## Part B: Theory Problem

Throughout, let $X = [0,1]$, $Y = \{-1,+1\}$, and

$$
h_\theta(x) = \mathrm{sign}(x-\theta),
$$

where $\mathrm{sign}(z) = +1$ for $z \ge 0$ and
$\mathrm{sign}(z) = -1$ for $z < 0$.

A sequence $((x_t, y_t))_{t=1}^T$ is $\Delta$-separated
threshold-realizable if there exists $\theta^* \in [0,1]$ such that

- $y_t = h_{\theta^*}(x_t)$, and
- $|x_t - \theta^*| \ge \Delta$ for every round $t$.

The following records the Part B prompt and the solution from my handwritten
notes for Questions 1-3.

### B1. From Continuous Thresholds To A Finite Class

**Problem.** Design a finite grid $G \subseteq [0,1]$ whose size depends only
on $\Delta$, and consider the associated finite threshold class
$H_G = \{h_\theta : \theta \in G\}$. Prove that for every
$\Delta$-separated threshold-realizable sequence, there exists some
$\hat{\theta} \in G$ such that $h_{\hat{\theta}}(x_t) = y_t$ for all
$t = 1, \dots, T$. Then use the Halving theorem to derive a mistake bound of
order $O(\log(1/\Delta))$. The answer should state the choice of grid $G$, the
size of $G$ as a function of $\Delta$, and the resulting mistake bound.

**Solution.** Let $m = \lceil 1/\Delta \rceil$ and define the grid

$$
G = \{0, \frac{1}{m}, \frac{2}{m}, \dots, \frac{m-1}{m}, 1\}.
$$

Then $|G| = m+1$. Since $m = \lceil 1/\Delta \rceil$, we have $m \ge 1/\Delta$,
so $1/m \le \Delta$.

Let $\theta^*$ be the threshold realizing the sequence. Because the grid spacing
is $1/m$, there exists $\hat{\theta} \in G$ such that

$$
|\theta^* - \hat{\theta}| < \frac{1}{m} \le \Delta.
$$

It remains to show that $h_{\hat{\theta}}(x_t) = y_t$ for every $t$.

For each round $t$, the $\Delta$-separation condition gives
$|x_t - \theta^*| \ge \Delta$.
There are two cases:

- If $x_t > \theta^* + \Delta$, then
  $x_t - \hat{\theta} > \theta^* + \Delta - \hat{\theta}
  \ge \Delta - |\theta^* - \hat{\theta}| > 0$,
  so $h_{\hat{\theta}}(x_t) = +1 = h_{\theta^*}(x_t) = y_t$.
- If $x_t < \theta^* - \Delta$, then
  $x_t - \hat{\theta} < \theta^* - \Delta - \hat{\theta}
  \le -\Delta + |\theta^* - \hat{\theta}| < 0$,
  so $h_{\hat{\theta}}(x_t) = -1 = h_{\theta^*}(x_t) = y_t$.

Thus $h_{\hat{\theta}}(x_t) = y_t$ for all $t$.

By the Halving theorem, the mistake bound is

$$
M \le \log_2 |G| = \log_2(m+1) = O(\log(1/\Delta)).
$$

### B2. A Positive Margin From Separation

**Problem.** View thresholds as linear predictors by choosing a feature map
$\phi : [0,1] \to \mathbf{R}^d$ and a unit vector $u^*$ depending on
$\theta^*$. Prove that every $\Delta$-separated threshold-realizable sequence
is linearly separable with margin at least $c\Delta$ for some absolute constant
$c > 0$ under your representation, while $\|\phi(x)\| \le R$ for all
$x \in [0,1]$ for some absolute constant $R$. Then use the Perceptron theorem
to derive an explicit mistake bound of order $O(1/\Delta^2)$.

**Solution.** Use the feature map

$$
\phi(x) = (x,1) \in \mathbf{R}^2.
$$

Let

$$
w^* = (1,-\theta^*),
$$

and normalize it to a unit vector

$$
u^{*} = \frac{w^{*}}{\|w^{*}\|}
= (
\frac{1}{\sqrt{1+(\theta^{*})^2}},
\frac{-\theta^{*}}{\sqrt{1+(\theta^{*})^2}}
).
$$

Then

$$
\langle u^{*}, \phi(x) \rangle = \frac{x-\theta^{*}}{\sqrt{1+(\theta^{*})^2}}.
$$

Since $y_{t} = \mathrm{sign}(x_{t} - \theta^{*})$, we have

$$
y_{t} \langle u^{*}, \phi(x_t) \rangle
= \frac{|x_{t}-\theta^{*}|}{\sqrt{1+(\theta^{*})^2}}.
$$

Using $|x_{t} - \theta^{*}| \ge \Delta$, it follows that

$$
y_{t} \langle u^{*}, \phi(x_{t}) \rangle
\ge \frac{\Delta}{\sqrt{1+(\theta^{*})^2}}
\ge \frac{\Delta}{\sqrt{2}}.
$$

So the sequence is linearly separable with margin at least

$$
\gamma \ge \frac{\Delta}{\sqrt{2}}.
$$

Also, because $x \in [0,1]$,

$$
\|\phi(x)\| = \sqrt{x^2+1} \le \sqrt{2}.
$$

Thus we can take $R = \sqrt{2}$ and $c = 1/\sqrt{2}$.

By the Perceptron theorem,

$$
M \le \frac{R^2}{\gamma^2}
\le \frac{2}{\Delta^2/2}
= \frac{4}{\Delta^2}
= O(1/\Delta^2).
$$

### B3. Comparison And Interpretation

**Problem.** Explain why the continuous-threshold impossibility phenomenon from
lecture does not contradict Part 1. Then compare the two mistake bounds from
Parts 1 and 2. Why do they scale differently with $\Delta$? What is each
argument measuring about the problem?

**Solution.**

1. The continuous-threshold impossibility phenomenon occurs when examples can
   be arbitrarily close to the true threshold, so the learner may need to
   distinguish infinitely fine threshold values. That does not contradict Part 1
   because here the sequence is $\Delta$-separated: every example stays at least
   $\Delta$ away from $\theta^*$. This spacing lets us replace the continuous class
   by a finite grid without changing any labels on the observed sequence.

2. The two mistake bounds scale differently because they come from different
   kinds of complexity:

   - Part 1 uses the Halving algorithm on a finite hypothesis class of size
     about $1/\Delta$, so the mistake bound is logarithmic:
     $O(\log(1/\Delta))$.
   - Part 2 uses the Perceptron theorem, where the bound depends on the inverse
     squared margin. Since the margin is at least a constant times $\Delta$, this
     gives the larger bound $O(1/\Delta^2)$.

   In other words, Part 1 measures cardinality complexity after discretizing the
   threshold class, while Part 2 measures geometric complexity through the
   margin of a linear representation.

### B4. Optional Strengthening: Audit An AI Proof

**Problem.** An AI assistant gives the following argument:

> Because every example is at least $\Delta$ away from the true threshold,
> continuous thresholds effectively form a class of size $O(1/\Delta)$.
> Therefore any online learner, including Perceptron, must make at most
> $O(\log(1/\Delta))$ mistakes on every $\Delta$-separated
> threshold-realizable sequence.

Identify at least two mathematical problems with this argument. Then write a
corrected statement that is true and prove it.

**Solution.** There are at least two mathematical problems with the argument.

1. The statement "continuous thresholds form a class of size $O(1/\Delta)$" is
   not literally true. The threshold class on $[0,1]$ is still infinite. What
   is true is weaker: for a fixed $\Delta$-separated realizable sequence, one
   can choose a finite grid so that some grid threshold agrees with the true
   threshold on that particular sequence. This does not turn the original
   continuous class itself into a finite class.

2. Even if we have a finite reference class of size $O(1/\Delta)$, it does not
   follow that **any** online learner has a mistake bound of
   $O(\log(1/\Delta))$. The Halving theorem gives this guarantee only for a
   specific algorithm, namely the Halving algorithm, running on a finite
   hypothesis class. It is an upper bound for that learner, not for all online
   learners.

3. In particular, the conclusion about Perceptron is unsupported. From Part 2,
   Perceptron only gets the margin-based guarantee
   $M \le O(1/\Delta^2)$ under the feature map $\phi(x) = (x,1)$. Nothing in
   the AI argument proves that Perceptron must satisfy the stronger
   $O(\log(1/\Delta))$ bound.

A corrected statement that is true is the following:

**Corrected statement.** There exists an explicit online learner, namely the
Halving algorithm run on a grid
$G = \{0, 1/m, 2/m, \dots, 1\}$ with $m = \lceil 1/\Delta \rceil$, that makes
at most $O(\log(1/\Delta))$ mistakes on every $\Delta$-separated
threshold-realizable sequence.

**Justification.** This is exactly the construction proved in Part B1: the
grid with spacing at most $\Delta$ contains a threshold that agrees with the
true threshold on the whole sequence, and then the Halving theorem gives the
mistake bound $O(\log(1/\Delta))$. So there is no need to re-prove it here.

So the right conclusion is existential and algorithm-specific: there exists a
finite-class learner with mistake bound $O(\log(1/\Delta))$. One cannot infer
from this that every online learner, or Perceptron in particular, enjoys the
same bound.

## Part C: Perceptron

This folder contains a minimal Python implementation for Part C and a short
discussion of the experimental results.

## Files

- `perceptron_experiments.py`: Perceptron implementation, synthetic data
  generator, and experiment helpers.
- `run_part_c.py`: Runs the experiments, saves plots, and prints summary
  statistics.
- `mistakes_vs_inv_gamma_sq.png`: Mistakes as a function of $1/\gamma^2$.
- `mistakes_vs_dimension.png`: Mistakes as a function of dimension $d$.
- `mistakes_vs_small_gamma.png`: Behavior as $\gamma \to 0$.

## How The Data Is Generated

To know the margin $\gamma$ and the norm bound $R$, I generate a unit separator
$u$ and then create examples of the form

$$
x = y \gamma u + \sqrt{R^2 - \gamma^2}\, v
$$

where:

- $y \in \{-1,+1\}$ is the label,
- $u$ is a random unit vector,
- $v$ is a random unit vector orthogonal to $u$.

This guarantees:

- $\|x\| = R$ for every point, so the norm bound is exactly known,
- $y \langle u, x \rangle = \gamma$, so the data is linearly separable with a
  known margin $\gamma$ with respect to a unit vector.

The main design choices are:

- fix $R$ and vary $\gamma$ to control difficulty,
- keep the separator unit norm so the geometric margin is easy to interpret,
- use dimensions $d \ge 2$ so there is room for an orthogonal component.

## Short Discussion

### 1. How do we generate data where $\gamma$ and $R$ are known?

Use a unit separator $u$, force each point to have a component $y \gamma u$
along the separator, and put the remaining mass in an orthogonal direction so
that the total norm is exactly $R$. This requires choosing $R > \gamma$, a unit
separator, and an orthogonal noise direction.

### 2. How does the number of mistakes scale with $1/\gamma^2$?

In the experiments, the number of mistakes increases as $\gamma$ gets smaller,
and the trend is roughly increasing with $1/\gamma^2$, which is consistent
with the theorem. For example, when $\gamma$ decreases from $0.5$ to $0.05$,
$1/\gamma^2$ grows from $4$ to $400$, while the average mistake count grows
from about $3.0$ to about $171.6$. The saved plot
`mistakes_vs_inv_gamma_sq.png` shows this relationship directly.

### 3. Is the theoretical bound $R^2/\gamma^2$ tight?

The experiments show that the bound is usually quite loose. The Perceptron makes
substantially fewer mistakes than $R^2/\gamma^2$ on these synthetic datasets.
For example:

- at $\gamma = 0.2$, the bound is $25$ while the average observed mistakes are
  about `13.8`,
- at $\gamma = 0.05$, the bound is $400$ while the average observed mistakes are
  about `171.6`.

So the theorem is a valid worst-case upper bound, but it is not tight in these
typical random instances.

### 4. Is the behavior independent of the dimension $d$?

The theorem does not depend on $d$, and the experiments mostly agree: once $R$,
$\gamma$, and the number of points are fixed, changing $d$ does not create a
strong systematic increase in mistakes. In my run, the average mistakes were
about $11.4$ at $d = 5$, $13.8$ at $d = 10$, $14.4$ at $d = 20$, $14.4$ at
$d = 50$, and $11.8$ at $d = 100$. There is some random variation, but no
clear growth trend comparable to changing $\gamma$.

### 5. What happens as $\gamma \to 0$?

As $\gamma$ becomes very small, the classes become nearly inseparable in a
numerical sense, and the number of updates grows quickly. This matches the
lecture intuition: when the margin approaches zero, the Perceptron guarantee
becomes very weak, and convergence can require many updates. In the small-margin
experiment, the average mistakes increased from about $13.8$ at $\gamma = 0.2$
to about $3649.8$ at $\gamma = 0.01$.

### 6. How was correctness checked?

I checked correctness in three ways:

- verified after generation that every example satisfies $\|x\| \le R$ and
  $y \langle u, x \rangle \ge \gamma$,
- tested on a tiny hand-checkable separable dataset where the Perceptron must
  converge quickly,
- compared empirical mistakes against the theorem to make sure the measured
  counts stay below the theoretical upper bound in the controlled experiments.

Checks that would catch subtle bugs:

- a sign mistake in the update rule would usually break convergence even on the
  tiny sanity-check dataset,
- a bug in the generator would be caught by directly measuring the actual margin
  and the largest norm before training,
- forgetting to normalize the separator would make the claimed margin invalid.

## Running

From the repository root:

```bash
python3 hw1/run_part_c.py
```

This will save the plots in `hw1/` and print the summary values used in the
discussion above.

## Part D: AI Usage Report

I used AI mainly to help with the implementation and presentation of Part C. In
particular, I used it to structure the Perceptron code, organize the experiment
runner, generate plots, and draft a short discussion of the results. I also used
AI to help convert the write-up into a PDF. I did not rely on AI as a black box
for the final answers; instead, I used it as a coding and writing assistant and
then checked the details myself.

One AI suggestion I accepted was the data-generation method for creating
linearly separable examples with known radius $R$ and margin $\gamma$. The final
generator used a unit separator $u$ and built each point as a sum of a
label-aligned component $y \gamma u$ and an orthogonal component scaled so
that every example had norm exactly $R$. I accepted this suggestion because it
directly matched the theory in the assignment and made it easy to verify both
the norm bound and the margin numerically.

One suggestion I modified was the written discussion of the results. The first
version was too generic and mostly repeated what the theorem says. I revised it
so that it referred to the actual observed numbers from the experiments, such as
the increase in average mistakes as $\gamma$ decreased and the comparison between
the empirical mistakes and the theoretical bound $R^2 / \gamma^2$. I changed it
because I wanted the report to reflect the experiments I actually ran rather
than just restate expectations.

I verified the code and results in several ways. First, I checked that the data
generator really produced points with $\|x\| \le R$ and signed margin at least
$\gamma$ with respect to the planted separator. Second, I ran a small
hand-checkable separable dataset to confirm that the Perceptron update rule
converged correctly. Third, I ran the full experiment script and checked that
the results were qualitatively consistent with theory: mistakes increased as the
margin got smaller, the bound was usually loose in practice, and there was no
strong systematic dependence on dimension once $R$ and $\gamma$ were fixed. These
checks would catch subtle bugs such as a sign error in the update rule or an
incorrectly normalized separator in the data generator.
