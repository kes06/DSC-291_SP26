# Part D: AI Usage Report

I used AI mainly to help with the implementation and presentation of Part C. In
particular, I used it to structure the Perceptron code, organize the experiment
runner, generate plots, and draft a short discussion of the results. I also used
AI to help convert the write-up into a PDF. I did not rely on AI as a black box
for the final answers; instead, I used it as a coding and writing assistant and
then checked the details myself.

One AI suggestion I accepted was the data-generation method for creating
linearly separable examples with known radius `R` and margin `gamma`. The final
generator used a unit separator `u` and built each point as a sum of a
label-aligned component `y * gamma * u` and an orthogonal component scaled so
that every example had norm exactly `R`. I accepted this suggestion because it
directly matched the theory in the assignment and made it easy to verify both
the norm bound and the margin numerically.

One suggestion I modified was the written discussion of the results. The first
version was too generic and mostly repeated what the theorem says. I revised it
so that it referred to the actual observed numbers from the experiments, such as
the increase in average mistakes as `gamma` decreased and the comparison between
the empirical mistakes and the theoretical bound `R^2 / gamma^2`. I changed it
because I wanted the report to reflect the experiments I actually ran rather
than just restate expectations.

I verified the code and results in several ways. First, I checked that the data
generator really produced points with `||x|| <= R` and signed margin at least
`gamma` with respect to the planted separator. Second, I ran a small
hand-checkable separable dataset to confirm that the Perceptron update rule
converged correctly. Third, I ran the full experiment script and checked that
the results were qualitatively consistent with theory: mistakes increased as the
margin got smaller, the bound was usually loose in practice, and there was no
strong systematic dependence on dimension once `R` and `gamma` were fixed. These
checks would catch subtle bugs such as a sign error in the update rule or an
incorrectly normalized separator in the data generator.
