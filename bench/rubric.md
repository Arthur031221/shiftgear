# Labeling rubric

This is the rubric used to hand-label the benchmark sample described in
bench/results.md, and the same categories `bench/classify.py` targets.
Categories are the task rows from references/decision-table.md, plus one
catch-all.

## Contents

- [Categories](#categories)
- [How a prompt gets a category](#how-a-prompt-gets-a-category)
- [The automatic classifier vs the hand label](#the-automatic-classifier-vs-the-hand-label)

## Categories

| Category | What it covers |
|---|---|
| `trivial_edit` | A rename, a typo, a one-line fix, a short mechanical command the user could describe in one sentence. |
| `boilerplate_scaffolding` | Starting a new project or file from a clear brief, no open design questions. |
| `writing_tests` | Writing or extending automated tests. |
| `refactor` | Restructuring existing, working code without changing behavior. |
| `hard_debugging` | Root-causing a failure whose cause is not obvious. |
| `architecture_design` | A new repository, a system design, or a "build this whole thing" brief with real design decisions in it. |
| `code_review` | Reviewing someone else's diff or PR. |
| `security_review` | A review specifically about vulnerabilities, exposure, or exploits. |
| `migration` | Moving many files or call sites off something being retired or renamed. |
| `documentation` | Writing or editing docs, READMEs, or reference material. |
| `data_analysis` | Working with a dataset, spreadsheet, or chart. |
| `research_reading` | Open-ended research: search the web, read sources, synthesize findings, cite dates. |
| `long_agentic_run` | Explicitly unattended, multi-hour, or background work. |
| `repetitive_transforms` | The same mechanical change applied across many files. |
| `ui_work` | Frontend layout, styling, or component work. |
| `performance_work` | Profiling or speeding something up. |
| `specs_interviews` | Gathering requirements, writing a spec, or generating varied question sets (the TOEFL-prep prompts in the real sample fall here: "make the daily questions different every day" is a requirements ask, not a coding task). |
| `other` | A question, a status check, a permission check, or a clarification that is not itself a task shiftgear would route. This is the fail-safe bucket, not a routing target. |

## How a prompt gets a category

For the benchmark, every sampled prompt got two labels:

1. **Hand label**: a person (in this case, the agent building shiftgear)
   read the full prompt and picked the closest category by judgment, the
   same way SKILL.md expects an agent to classify a real task.
2. **Automatic label**: `bench/classify.py` ran the same prompt through
   its ordered regex rules and returned a category with no judgment
   involved.

Agreement between the two is the number reported in bench/results.md.
This measures how well a cheap, deterministic proxy tracks human
judgment, not how good shiftgear's real routing is: the actual skill
expects a full agent to read SKILL.md and classify with judgment, in
whatever language the user wrote in, not to run this regex script.

## The automatic classifier vs the hand label

`bench/classify.py` is deliberately simple: two tiers of regex rules
(strong phrase matches checked against the whole prompt, weaker
single-keyword matches restricted to the first 500 characters, since
keywords buried deep in a long prompt turned out to false-positive
constantly in early testing). It is English-keyword-first. On the real
benchmark sample, it reached 100% agreement with the hand labels on
English-language prompts and 50% on non-English prompts, because a
regex has no notion of Chinese phrasing that an LLM reading the same text
natively would just understand. This is a known, stated limitation of the
proxy script, not of the skill itself.
