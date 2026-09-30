---
name: shiftgear
description: "Picks which model and which effort or reasoning level to use for the current task, and gives the exact command to apply it, in Claude Code, Codex CLI, Gemini CLI, Cursor, or OpenCode. Use this whenever the user asks which model to use, whether to raise or lower effort/reasoning/thinking level, how to save cost or quota on a task, why a session is burning through the 5-hour or weekly limit, or how to route a long unattended job, a refactor, a security review, a migration, or a batch of repetitive edits. Also trigger before starting any task where the model or effort has not been chosen yet: a fresh architecture decision, a hard bug, a large refactor, bulk mechanical edits, or a run expected to take over 30 minutes unattended. Do not trigger for a question that has nothing to do with model, effort, cost, or quota, for a task already mid-flight on a model the user explicitly picked and did not ask to reconsider, or for a one-line factual question a small model would answer in one turn without agentic work."
license: MIT
metadata:
  author: Arthur031221
  version: "1.0.0"
compatibility: Works standalone with judgment in any agent that reads Markdown skills. scripts/estimate_cost.py and scripts/refresh_models.py need Python 3.9+, scripts/quota_state.sh needs bash and jq if available (falls back to python3, then to "unknown").
---

# shiftgear

Pick a model and an effort level for the task in front of you, say why in
one line, and give the exact command to apply it. Do this before writing
code, not after. Re-run the classifier when the task actually changes
(a new `/clear`, a new conversation, or the ask now clearly belongs to a
different row of the table), not on every turn.

## 1. When this fires, and when it must not

Fires on: "which model should I use," "is this worth Opus," "why did I
burn through my weekly limit," "route this migration," "set effort for a
9-file refactor," starting any task in the categories below with no model
or effort chosen yet.

Does not fire on: a task already running on a model the user explicitly
picked and did not ask to reconsider (never downshift mid-conversation,
see Hard rules), a plain factual question with no agentic work attached,
or anything unrelated to model/effort/cost/quota. If in doubt, and the
task is trivial enough to answer directly, just answer it. Routing has a
cost too: do not spend a turn on ceremony for a one-line fix.

## 2. The 30-second classifier

Work through these in order. Stop at the first thing that applies.

1. **Capability floor** = the max of: reasoning depth needed, stakes, loop
   length, ambiguity. A task that is deep OR risky OR long OR ambiguous
   gets the floor of whichever is worst, not an average.
2. **Cost exposure** = the sum of: context size, expected output volume,
   loop length. This tells you how much a wrong guess costs, separate
   from how hard the task is.
3. **Hard floors, checked first, they override everything below:**
   - Risk words in the task (prod, delete, migration, auth, payment,
     security) never route below Sonnet-class or Sol-class. No exceptions
     for "just checking."
   - Context over 180K tokens: never Haiku-class.
   - Visual input involved: Opus 5.5-class, full stop.
   - Expected to run unattended over 30 minutes: needs an xhigh-capable
     model, not a fixed-budget one.
4. **Match the task to a row** in references/decision-table.md (also
   assets/decision-table.csv). 18 rows cover trivial edits through quota
   exhaustion. If nothing matches cleanly, treat it as the closest
   neighbor and say so in the Why line.
5. **Effort ladder**, once the model is picked:
   - Default medium.
   - Drop to low only if the diff is describable in one sentence AND a
     test or build can verify it.
   - Go high when verification matters or edge cases are likely.
   - xhigh only for a measured gain you can point to, not by default.
   - Never use max without also setting `max_tokens` to 128K and giving
     the model a stop-rule prompt: max without a ceiling is how both
     Opus 5.5 and Sonnet 5.5 have been observed burning the full output
     window and still failing (references/effort-controls.md).
   - For anything checkable (tests pass, build succeeds, lint is clean),
     prefer low effort first, then re-run only the failures at high. This
     is not a minor optimization: Anthropic's own measurement has this
     beating flat high-effort on both cost and pass rate (see section 7).

## 3. Budget mode

Three modes: **max-quality**, **balanced** (default), **quota-saver**.

Auto-switch to quota-saver when `scripts/quota_state.sh` reports the
5-hour window over 80% consumed, or the weekly window over 60% consumed
with more than 2 days left in it. Otherwise stay in balanced unless the
user names a mode. Max-quality is opt-in only: use it when the user says
"I don't care about cost" or the task is a hard floor (security review,
architecture-defining decision).

## 4. Output template

One block, then act. Do not skip the Escalate line, it is the whole point
of routing cheap first.

```
Route: Sonnet 5.5 at medium. Mode: balanced. Why: well-specified 3-file refactor with tests. Cheaper: Sonnet 5.5 at low, rerun failures at high. Escalate if: tests still fail after 2 attempts, then Opus 5.5 at high. Quota: 5h 42% used, resets 15:40. Apply: /model sonnet then /effort medium
```

If `scripts/quota_state.sh` returns unknown, say `Quota: unknown` and move
on, do not block on it.

## 5. Per-agent apply instructions

Confirmed against each tool's own docs on 2026-09-30. Full syntax and
env vars in references/effort-controls.md.

- **Claude Code**: `/model <alias>` then `/effort <level>`, or
  `claude --model <alias> --effort <level>`. Aliases: `sonnet`, `opus`,
  `haiku`, `fable`, `opusplan` (Opus plans, Sonnet executes). Levels:
  `low medium high xhigh max`. Skill/subagent frontmatter takes
  `model:` and `effort:` directly.
- **Codex CLI**: `model = "gpt-6-sol"` and
  `model_reasoning_effort = "medium"` in `config.toml`, or the `/model`
  slash command interactively. Levels: `none low medium high xhigh max`
  (model-dependent). `plan_mode_reasoning_effort` overrides for plan mode
  specifically.
- **Gemini CLI**: `/model` for the picker (Auto, or Manual with
  `gemini-3-pro-preview` / `gemini-3-flash-preview`), or `--model` at
  startup. Thinking level via `thinkingConfig.thinkingBudget` in
  `settings.json` or `thinking_level` on the 3.x API (`low medium high`).
- **Cursor**: the model picker, or Auto (Cost / Balance / Intelligence).
  Max Mode for extended context, legacy request plans only.
- **OpenCode**: `/models` to switch, or the `variant_cycle` keybind to
  step through preset variants (Anthropic: high default and max, OpenAI:
  none through xhigh, Google: low and high).

## 6. Hard rules

- Never downshift a model mid-conversation just to save money. Reclassify
  only at a `/clear`, a new session, or a genuine cache-cold boundary.
  Switching model mid-session also invalidates the prompt cache, so a
  downshift usually costs more than it saves on that turn alone.
- Never route a risk-word task (prod, delete, migration, auth, payment,
  security) below Sonnet-class or Sol-class, regardless of mode.
- Never set effort to max without also setting an output token ceiling
  and a stop-rule prompt.
- A reviewer subagent runs in a fresh context, never the implementer's
  own thread: self-review misses what the implementer already missed.
- If the user's plan mode diff is describable in one sentence, skip plan
  mode, do not spend a turn planning what you can just do.

## 7. Failure-mode checklist

Before you commit to a route, check whether you are about to repeat one
of these (all measured, sources in references/effort-controls.md):

- Max-effort token exhaustion: both Opus 5.5 and Sonnet 5.5 have hit the
  128K output ceiling and failed outright at max effort with no ceiling
  set.
- Undersized `max_tokens`: a 16,384 ceiling cut off 25% of Opus 5.5
  attempts and 43% of Fable 5.1 attempts before they finished, not
  because the model was wrong, because it ran out of room.
- Low effort skipping verification: Sonnet 5.5 at low can stop without
  double-checking unless the prompt says to check.
- Tool-call flakiness even on frontier models: watch for a model calling
  the wrong tool name under load.
- Context blow-ups from a session that never got `/clear`ed, plus a
  1-hour prompt-cache expiry working against you.
- Quota burn from parallel agent teams: one reported case burned a 20x
  weekly Opus limit in 2.5 days running a team at medium effort.
- Open-weight small models collapsing on long terminal tasks: fine for
  bulk mechanical work, weak on anything requiring a long tool-use chain.

## 8. Update cadence

Run `scripts/refresh_models.py` monthly and whenever a new model gets
mentioned in a session. It pulls openrouter.ai/api/v1/models, diffs
against references/models.md, and prints a dated STALE banner once the
references are over 30 days old. Prices and levels live only in
references/, never in this file, so this file does not go stale just
because a price changed. Haiku 4.5's retirement floor is 2026-10-15: once
past that date, treat any quota-saver route naming Haiku 4.5 by name as
needing a replacement check (references/models.md, "Old patterns").

## Reference files

- **references/models.md**: the model landscape, prices, context
  windows, effort ladders per model, headline benchmarks. Read this
  before quoting a price or a score to a user.
- **references/effort-controls.md**: exact syntax per tool plus every
  measured effort-vs-cost-vs-quality number this skill relies on.
- **references/quotas.md**: subscription plan mechanics and what
  community measurement exists for each.
- **references/decision-table.md**: the full 18-row table behind
  section 2 step 4, with rationale and sources per row.
- **references/evidence.md**: every source key used anywhere in this
  skill, one place, so a claim can always be checked.
- **assets/decision-table.csv**: machine-readable copy of the same
  table, for anyone scripting against it.
