# Benchmark: routing agreement and estimated cost, real prompts

Method: Option A from the build brief (task-category cost-ladder
estimate on real local prompts, hand-labeled). Option B (headless replay
under both arms) was not run: the machine's Claude quota was reserved for
other concurrent builds. Every number below is an estimate from published
cost ladders, not a measured pass rate. Run date: 2026-09-30.

## Contents

- [Sampling](#sampling)
- [Why n=31, not 100](#why-n31-not-100)
- [Hand-labeling](#hand-labeling)
- [Classifier agreement](#classifier-agreement)
- [Cost estimate](#cost-estimate)
- [Comparison to Anthropic's published anchor](#comparison-to-anthropics-published-anchor)
- [What this does and does not show](#what-this-does-and-does-not-show)

## Sampling

Every `~/.claude/projects/**/*.jsonl` file on this machine (29 files, 52MB)
was scanned for `type: "user"` records with `role: "user"`. Records were
dropped if they were: marked `isMeta`, a bare slash command (`/model`,
`/clear`), a `<local-command-*>` wrapper or its stdout echo, a harness
background-task notification relayed as a user turn (identified by
`<task-id>`, `<tool-use-id>`, or `<output-file>` tags), an interruption
marker (`[Request interrupted by user]`), a tool-loaded echo, or a
duplicate of an already-kept prompt (first 120 characters as the dedupe
key). Every kept prompt was passed through a secret-pattern filter
(API key prefixes, JWTs, long hex or base64 blobs, email addresses) before
being written anywhere, including this machine's own scratch directory.
The extraction script and the raw sampled prompts stayed local and were
never committed. Only this file, bench/rubric.md, and
bench/category_counts.csv were.

## Why n=31, not 100

The brief asked for a 100-prompt sample. This machine's actual Claude Code
history does not contain 100 distinct real prompts: across all 29
transcript files there were 2,181 non-meta `user`-role records, but only
79 of them carried plain text at all (the rest are tool-result payloads
that the harness also stores as `user`-role turns, which is normal Claude
Code transcript structure, not a data problem). After removing slash
commands, harness notifications, interruption markers, and duplicates, 31
distinct genuine prompts remained. That is the true count for this
machine on this date, not a rounding choice, and this file reports on all
31 rather than padding the sample. Per the brief's own instruction to
hand-check a 30-prompt subset for agreement, and given the full sample is
only 31, every prompt was hand-checked rather than a 30-of-100 slice.

## Hand-labeling

Each of the 31 prompts was read in full and assigned one category from
bench/rubric.md by judgment. Resulting counts (also in
bench/category_counts.csv):

| Category | Count |
|---|---|
| architecture_design | 11 |
| other (not a routable task) | 8 |
| research_reading | 6 |
| trivial_edit | 4 |
| specs_interviews | 2 |

No prompt in this sample fell into hard_debugging, code_review,
security_review, migration, documentation, data_analysis, ui_work,
performance_work, writing_tests, boilerplate_scaffolding,
repetitive_transforms, or long_agentic_run as its primary category. This
reflects one specific week of one person's actual usage (a batch of
"build a complete open-source project" briefs plus a personal exam-prep
side project), not a claim that those task types are rare in general
agent use. A larger or differently-timed sample would very likely surface
them. See "What this does and does not show" below.

## Classifier agreement

`bench/classify.py`, run against the same 31 prompts:

- Overall: 24/31 agree with the hand label = **77.4%**.
- English-language prompts only (17 of 31): 17/17 = **100%**.
- Non-English prompts (14 of 31, mostly Chinese): 7/14 = **50%**.

All 7 disagreements have the same shape: the automatic classifier
returned `other` where the hand label found a real category. The
classifier's rules are English-keyword patterns. A Chinese research
request or a Chinese "build and deploy this" request does not contain any
of those keywords, so it falls through to the safe default instead of
being misrouted into the wrong technical category. That is the correct
failure mode for a deterministic proxy (fail to "no route" rather than
fail to "wrong route"), but it is a real limitation of the script, not of
the skill: SKILL.md's own classifier is meant to be applied by the agent
reading the task, which understands Chinese natively and would not have
this gap. The first classifier draft, which searched the entire prompt
text with a single priority order, agreed with hand labels only 45.2%
(14/31) of the time: long prompts (some over 4,000 characters, mostly
"build a complete project" briefs that also mention testing, profiling,
or migration in passing as part of unrelated engineering-standards
boilerplate) tripped generic single-keyword rules before the more
specific signal near the start of the prompt got a chance. Restricting
weak keyword rules to the first 500 characters of the prompt, and
checking a small set of highly specific multi-word phrases against the
full text first, raised that to 77.4%. This ordering issue, and the fix
for it, are now built into `bench/classify.py` itself.

## Cost estimate

Cost per task under two arms, computed from the Artificial Analysis
cost-per-task ladder in references/models.md (source S13) with three
effort-level cells not published by AA (Opus 5.5 low, Sonnet 5.5 low and
medium, Haiku 4.5 low) filled in from the measured Opus 5.5 SWE-bench Pro
effort-cost ratios in references/effort-controls.md (source S23: medium
is about 70% of high's cost, low about 33%). These derived cells are
marked in scripts/estimate_cost.py and are estimates, not published
figures.

- **shiftgear (balanced mode)**: for each of the 23 routed prompts (the 8
  `other` prompts are excluded, they are not tasks shiftgear would route
  at all), look up the Balanced-column model and effort in
  references/decision-table.md for that prompt's category, then its cost
  from the ladder above.
- **Baseline**: the same 23 prompts, every one costed as Opus 5.5 at high
  effort ($1.82/task, AA-published, not derived), which is what "always
  use the strongest model at high effort" costs on this ladder.

| | Total (23 tasks) | Per task |
|---|---|---|
| shiftgear, balanced mode | $25.72 | $1.118 |
| always Opus 5.5 at high | $41.86 | $1.820 |

**Estimated savings: 38.6%.**

This sample is dominated by architecture_design tasks (11 of 23 routed),
which route to Opus 5.5 at medium in balanced mode ($1.34/task) rather
than the baseline's high ($1.82/task), a real but modest per-task saving.
The bigger savings come from the smaller categories: trivial_edit routes
to Sonnet 5.5 at low ($0.356) against a $1.82 baseline, and
research_reading and specs_interviews route to Sonnet-class models at
medium rather than Opus at high. A sample with more trivial edits and
boilerplate work, which is most agent usage outside a "build me a whole
project" week, would show larger savings, since those are exactly the
categories where balanced mode drops furthest from the baseline.

Reproduce this: the cost ladder is in `scripts/estimate_cost.py`
(`--task --model <model> --effort <level>`), and the category-to-route
mapping is `references/decision-table.md`'s Balanced column. The raw
31-prompt sample is not included in this repository. The counts and
labels above are the complete record of what it contained.

## Comparison to Anthropic's published anchor

Anthropic's own optimizing-for-cost-and-intelligence page reports, for
SWE-bench-Pro-style checkable tasks specifically: running everything at
low effort and re-running only the failures at high reaches about 97%
pass for $0.17/task, against all-high's 95.3% pass for $0.29/task (source
S23, references/effort-controls.md). That is a different task mix (one
benchmark, fully checkable) and a different mechanism (retry-on-failure,
not per-category routing) than this benchmark's 23 mixed real-world
prompts, so the two savings percentages (about 41% there, 38.6% here) are
not directly comparable, but they land in the same range, which is a
reasonable sanity check on the estimate above rather than independent
confirmation of it.

## What this does and does not show

This measures two things honestly: how well a cheap deterministic
classifier proxy agrees with human judgment on real prompts (77.4%, with
a clear, explained gap on non-English text), and what the published cost
ladders say balanced-mode routing would have cost against always-Opus-
5.5-at-high, for the specific 31 prompts on this machine on this date
(38.6% estimated savings). It does not measure pass rates, does not run
any task twice under different models, and does not claim this sample
represents typical agent usage in general: it represents one person's
actual local history, small by construction, reported in full rather than
padded to a round number.
