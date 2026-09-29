# shiftgear

Tells your coding agent which model and which effort level to use, before
it starts, across Claude Code, Codex CLI, Gemini CLI, Cursor, and
OpenCode.

On the 31 real prompts pulled from this machine's own Claude Code history,
shiftgear's balanced-mode routing came out an estimated 38.6% cheaper than
running everything on Opus 5.5 at high effort, using published cost
ladders rather than a stopwatch.[^bench] That number is small-sample and
estimated, not a measured pass rate, and the method and every number
behind it are in [bench/results.md](bench/results.md).

[^bench]: n=31 real, distinct, non-meta user prompts from every
`~/.claude/projects/**/*.jsonl` file on one MacBook Air M5 (24 GB), sampled
and hand-labeled 2026-09-30. Cost estimate is the Artificial Analysis
cost-per-task ladder (references/models.md, source S13) applied per task
category via references/decision-table.md's balanced-mode column, against
Opus 5.5 at high effort for every task. Full method, category counts, and
classifier agreement (77.4% overall, 100% on English-language prompts) in
bench/results.md. No tasks were re-run under different models: this is a
routing-cost estimate, not a benchmark of output quality.

[![CI](https://github.com/Arthur031221/shiftgear/actions/workflows/ci.yml/badge.svg)](https://github.com/Arthur031221/shiftgear/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

![shiftgear demo: reading the output template, estimating task cost, checking quota state, checking staleness, and running the test suite](demo/demo.gif)

## Why

Every agent session starts with a choice nobody writes down: which model,
and how hard should it think. Most people leave both on the default and
either overpay on a typo fix or underpay on a hard bug that then needs
three more turns to fix properly. The five tools that matter right now
each spell this differently, `/effort` in Claude Code, `model_reasoning_effort`
in Codex, `thinking_level` in Gemini, a picker in Cursor, `variant_cycle`
in OpenCode, so the rule of thumb you learned on one tool does not carry
to the next one. And the knobs are per-session: your Claude Pro or Max
plan burns through a shared 5-hour and weekly quota regardless of which
model you picked, so the right answer also depends on how much of this
week's budget is already gone.

## Install

```
npx skills add Arthur031221/shiftgear
```

Or copy it by hand:

```
git clone https://github.com/Arthur031221/shiftgear ~/tmp/shiftgear
cp -r ~/tmp/shiftgear ~/.claude/skills/shiftgear
```

For Codex, Cursor, or OpenCode, copy `AGENTS.md` (and, if the tool supports
it, the rest of the repository) to wherever that tool reads project or
global agent instructions.

## Quick start

Ask your agent something that needs a model decision:

> "I need to refactor this 6-file auth module, there are tests already.
> Which model should I use?"

With shiftgear installed, the agent reads SKILL.md, classifies the task,
and replies with one block before touching anything:

```
Route: Sonnet 5.5 at medium. Mode: balanced. Why: well-specified 3-file refactor with tests. Cheaper: Sonnet 5.5 at low, rerun failures at high. Escalate if: tests still fail after 2 attempts, then Opus 5.5 at high. Quota: 5h 42% used, resets 15:40. Apply: /model sonnet then /effort medium
```

You can also run the pieces standalone:

```
python3 scripts/estimate_cost.py --task --model opus-5-5 --effort high
bash scripts/quota_state.sh
python3 scripts/refresh_models.py
```

## How it works

`SKILL.md` (under 300 lines, no prices in it on purpose) holds a 30-second
classifier: work out the capability floor and the cost exposure of the
task, check four hard floors that override everything else (risk words,
context size, visual input, unattended runtime), match the task against
an 18-row decision table, then pick an effort level with a bias toward
"cheap first, escalate on failure" for anything checkable. `references/`
holds the facts that back every one of those rules: the model landscape,
each tool's exact control syntax, subscription quota mechanics, the full
decision table, and a numbered evidence list, every row source-cited and
dated so the skill can be checked and refreshed instead of trusted blind.
`scripts/refresh_models.py` pulls the live OpenRouter model list and
diffs it against what's in `references/models.md`, and prints a dated
STALE banner once that file is over 30 days old.

The classifier itself is applied by whichever agent reads SKILL.md,
using judgment, in whatever language the task was written in.
`bench/classify.py` is a separate, much simpler regex-based proxy built
only to make the benchmark in `bench/results.md` reproducible by a third
party without an LLM in the loop. It is not what runs in production, and
it is explicitly worse at non-English prompts than a real agent would be.

## Comparison

What shiftgear does that the closest existing tools do not: cover five
tools' actual command syntax in one place, cite a source and a date for
every price and every benchmark number, and route the same content
differently depending on remaining subscription quota, not just task
type.

| Project | Stars[^stars] | What it does | What it lacks |
|---|---|---|---|
| [musistudio/claude-code-router](https://github.com/musistudio/claude-code-router) | 37.5k | A proxy control plane that reroutes Claude Code traffic to other providers. | No task-level effort routing at all, it is a transport layer, not a decision rule. |
| [workweave/router](https://github.com/workweave/router) | 5.4k | An embedding-based proxy router, claims 40-70% savings. | Savings claim has no stated method. No per-tool apply syntax. No quota awareness. |
| [kerpopule/hermes-jev-skills](https://github.com/kerpopule/hermes-jev-skills) | 907 | Per-turn routing using a small typed-decision model (Jev), risk-word rules. | No stated routing accuracy. Jev is a paid external API call on every turn (0.4-12s added latency). Claude Code only. |
| [modu-ai/moai-adk](https://github.com/modu-ai/moai-adk) | 1.2k | Three-tier profiles (high/medium/low), a "No-Haiku" policy, claims 60-70% savings. | Savings claim has no stated method. Three tiers only, no effort ladder within a model. Claude-only. |
| Small rubric repos (EchoBird, hussi9/skill-router, senda-labs/DQIII8, Rishav1996/model-router, frankchu91/coding-agent-router, AndrewStifora/model-grade, marcoaiwithfefe-hub/effort-pick) | 0-26 | Quota tracking, capability rubrics, or a "cannot change the session's own model" honesty note. | Each covers at most one or two tools. None cites a source or date for a price or a benchmark number. None has a replay or cost benchmark at all. Rishav1996's own README admits its pricing goes stale. |
| **shiftgear** | new | Five tools' exact apply syntax, source-and-date on every reference number, a refresh script, a real cost benchmark on real local prompts. | Single-machine benchmark so far (n=31). No headless pass-rate replay yet (Option B in the build brief, not run to preserve quota). Classifier proxy for the benchmark is English-keyword-first (the real skill has no such limit, since an LLM reads it). |

[^stars]: Star counts as reported in the research this project was built
from (research/brief-model-router.md, source S36, fetched 2026-09-29),
not independently re-verified for this README. Check the repos directly
for current counts.

None of the studied competitors close all of these gaps at once: no
skill covers Claude Code, Codex, Gemini CLI, Cursor, and OpenCode with
each tool's actual control names. None reads subscription quota state
into the routing decision, though Claude Code exposes it. None cites
vendor-measured effort curves or a leaderboard's per-level cost ladder.
None with a rubric has a replay or cost benchmark at equal footing. Three
admit stale pricing with no refresh script. The Jev-based routers add
external latency and a paid API key most people would rather not manage
for a routing decision.

## Reference

- `SKILL.md`: the full classifier, budget modes, output template,
  per-agent apply syntax, hard rules, failure-mode checklist.
- `references/models.md`: prices, context windows, effort ladders,
  headline benchmarks, per model, source-cited and dated.
- `references/effort-controls.md`: exact `/model` and `/effort` (and
  equivalents) syntax per tool, plus every measured effort-vs-cost number
  this skill relies on.
- `references/quotas.md`: subscription plan mechanics.
- `references/decision-table.md` / `assets/decision-table.csv`: the
  18-row task-to-route table.
- `references/evidence.md`: every source cited anywhere, in one place.
- `scripts/estimate_cost.py --model <id> --effort <level> [--input-tokens N --output-tokens N | --task] [--json]`
- `scripts/quota_state.sh [--pretty]`
- `scripts/refresh_models.py [--offline] [--json]`
- `AGENTS.md`: the same routing logic, condensed, for tools that read
  AGENTS.md instead of SKILL.md.

## Limits and FAQ

**Does this call any API or hold any key?** No. It reads local files and
one public, unauthenticated endpoint (`openrouter.ai/api/v1/models`, only
inside `refresh_models.py`, only when you run it). It does not proxy your
traffic and cannot see your prompts.

**Does it change the model for me?** No. It tells you the exact command.
Your agent (or you) runs it. shiftgear cannot reach into a running
session and switch its own model.

**What if `quota_state.sh` cannot read anything?** It prints
`{"status":"unknown", ...}` and exits 0. SKILL.md is written to print
`Quota: unknown` and route on task merits alone rather than block.

**How current are the prices?** As current as the last time someone ran
`scripts/refresh_models.py` and updated `references/`. Prices live only
in `references/`, never in `SKILL.md`, specifically so a stale price
does not require touching the routing logic.

**Does it work in a language other than English?** The skill itself,
yes: an agent reading SKILL.md classifies the task with ordinary
judgment, in whatever language the task was written in. The benchmark's
proxy classifier (`bench/classify.py`) does not: it is English-keyword
based and was built only to make the benchmark reproducible without an
LLM in the loop. See bench/results.md for the measured gap.

**Is the benchmark representative of general agent usage?** Not proven to
be. It is 31 real prompts from one person's one week of usage on one
machine, reported in full rather than padded to a rounder number. See
bench/results.md for exactly what it does and does not show.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Short version: every changed
number needs a source URL and a date.

## License

MIT, see [LICENSE](LICENSE).
