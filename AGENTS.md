# AGENTS.md

This repository is for my course assignment submissions.

## General Rules
- Keep files organized by homework folder.
- Do not modify or remove completed work unless asked.
- Keep code and explanations clear and minimal.
- Respect assignment instructions.

## Proof & Math Work
- Always list universally quantified objects vs. adversarial choices before drafting any lower-bound proof.
- Keep numeric constants explicit — do not absorb them into O(·) notation unless explicitly asked.
- Never skip inequality steps; expand all key transitions even if they seem obvious.

## Workflow Rules
- Before generating content, map each assignment bullet to a proposed section and confirm coverage.
- For each major section, log at least one AI suggestion that was rejected or modified, and why.
- Before submission, run a traceability pass: confirm every assignment requirement is explicitly answered in a named subsection.

## AI Workflow Checks
- After any AI-generated proof, run a proof-completeness check: list each inequality/bound step and cite the exact theorem used.
- For multi-step bounds, explicitly track normalization factors and constants through to the final expression; if factors are absorbed into constants, state that explicitly.
- For combinatorial/set-characterization claims, explicitly verify boundary cases (empty sets, all-positive samples, all-negative samples, etc.).
- Use a two-pass AI workflow when needed: first pass for derivation, second pass for interpretation ("what this proves" and "what it does not prove").
- Before finalizing, run a sign/operator audit to confirm all binary operators (\(+, -, \le, \ge\)) are present and correct.

## Notation & Consistency
- Maintain consistent notation across all sections (distributions, risks, hypothesis classes).
- When referencing theorems, cite the standard source (e.g. Hoeffding 1963, McDiarmid 1989).
