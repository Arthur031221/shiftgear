# Effort and reasoning controls, per tool

Snapshot date: 2026-09-30. This file lists the exact control names for each
tool, confirmed against each vendor's own docs page on 2026-09-30 (URLs in
references/evidence.md), plus the measured effect of effort level on
quality and cost where a vendor or a careful community source has actually
published a number. Do not add a claim here without a source key.

## Contents

- [Claude Code](#claude-code)
- [Claude API](#claude-api)
- [Measured effort curves](#measured-effort-curves)
- [Codex CLI](#codex-cli)
- [Gemini API and CLI](#gemini-api-and-cli)
- [Cursor](#cursor)
- [OpenCode](#opencode)

## Claude Code

Confirmed against code.claude.com/docs/en/model-config on 2026-09-30 (S21).

**Model selection**

```
/model                    # interactive picker
/model <alias|name>       # switch and save as default
/model <alias|name> s     # switch for this session only (picker option)
```

Aliases: `default`, `best` (Fable if available, else Opus), `fable`,
`sonnet`, `opus`, `haiku`, `sonnet[1m]`, `opus[1m]`, `opusplan` (Opus while
planning, Sonnet for execution), `opusplan[1m]`.

CLI flag: `claude --model <alias|name>`. Env vars: `ANTHROPIC_MODEL`,
`ANTHROPIC_DEFAULT_MODEL`, `ANTHROPIC_DEFAULT_OPUS_MODEL`,
`ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`,
`ANTHROPIC_DEFAULT_FABLE_MODEL`, `CLAUDE_CODE_SUBAGENT_MODEL`.
`settings.json`: `"model"`, `"fallbackModel"`, `"availableModels"`,
`"modelSettings"`.

**Effort selection**

```
/effort                   # interactive slider
/effort <level>           # low | medium | high | xhigh | max
/effort auto              # clear saved level for the active model
/effort ultracode          # turn on ultracode (dynamic workflows at xhigh)
```

CLI flag: `claude --effort <level>`. Env var: `CLAUDE_CODE_EFFORT_LEVEL`
(note: `ultracode` is not a valid env var value, session/slash only).
`settings.json`: `"effortLevel"`, `"modelSettings.<model>.effort"`.

Skill and subagent frontmatter both accept `model:` (alias, full name, or
`inherit` for subagents) and `effort:` (`low|medium|high|xhigh|max`, no
`ultracode` in frontmatter).

Level support: Fable 5.1, Fable 5, Opus 5.5, Sonnet 5.5, Opus 5, Sonnet 5,
Opus 4.8, Opus 4.7 all take low/medium/high/xhigh/max. Opus 4.6 and
Sonnet 4.6 stop at max (no xhigh). Defaults: Opus 5.5 and Sonnet 5.5 default
to medium, Opus 4.7 defaults to xhigh, everything else that supports effort
defaults to high. Thinking cannot be turned off on 5.5 or Fable models.
`MAX_THINKING_TOKENS` only affects fixed-budget (non-adaptive) models.
`ultrathink` in a prompt raises reasoning for that one turn without
touching the session's saved effort level. (S21)

Anthropic's own framing: "Opus 5.5 at medium matches or exceeds Opus 5 at
high." (S21, S24)

## Claude API

`output_config.effort`. A per-message effort override (beta header
`mid-conversation-output-config-2026-07-01`) preserves the prompt cache. A
top-level change invalidates it. Effort "affects all tokens, tool calls,
thinking." Lower effort means "fewer and terser tool calls." `xhigh` is
described for "long-running agentic and coding tasks (over 30 minutes) with
token budgets in the millions." The Opus 4.7 docs warn that `max` "can lead
to overthinking." (S22)

## Measured effort curves

All numbers below are as published, not shiftgear's own measurements.

- Opus 5.5 on SWE-bench Pro: medium is -2.5 points at ~70% of high's cost,
  low is -8 points at ~33% of high's cost, xhigh is +1.4 points at 2.5x
  cost. "Run all at low, re-run failures at high" reaches ~97% pass for
  $0.17/task versus all-high's 95.3% for $0.29/task. (S23)
- Fable 5.1 on DeepResearch Bench II: low, medium, and high scored the
  same. Cost ranged $4.66 to $7.12. (S23)
- Fable 5 research suite: medium matched the default result at 70-87% of
  the cost, low cost -1 to -3 points for 33-50% off. (S23)
- `max_tokens` of 16,384 cut off 25% of Opus 5.5 attempts and 43% of
  Fable 5.1 attempts before they finished. (S23)
- Simon Willison: Sonnet 5.5 at max spent 128K tokens ($1.28) and failed.
  Xhigh succeeded in 41 seconds for 5.7 cents. Opus 5.5 at max failed
  twice, $2.56 total, ~20 minutes. (S20)
- Sonnet 5.5 at max self-launches reviewer subagents. A stop instruction
  "cut session cost by about a third, with no change in quality." (S24)
- A stronger model at low effort can beat a weaker model at high effort on
  cost per solved task: Fable 5.1 low 88.6% at $0.54 versus Sonnet 5
  default 77.4% at $0.84. Opus 5.5 medium 92.8% at $0.22 versus Fable 5.1
  default 92.3% at $1.19. (S23)
- Orchestrator-plus-cheap-workers roughly halves cost but scores 10-12
  points lower. The advisor pattern (cheap model drafts, strong model
  reviews) only pays off when the executor actually consults the advisor.
  (S23)

Anthropic's July 2026 blog: use a smaller model for "edits you can
describe precisely, mechanical changes, questions about code that's
already in context," a larger model for "subtle bugs, unfamiliar domains,
architecture decisions." Raise effort when Claude "skipped a file, not
running the tests, or not double-checking." Upgrade model when it "did not
know enough." "Tuning effort is often a better lever than switching
models." Escalate to Fable only "if your evals at xhigh or max effort
still fall short." (S31)

## Codex CLI

Confirmed against learn.chatgpt.com/docs/config-file/config-reference.md
on 2026-09-30 (S25).

`config.toml` keys:

- `model` (string): model to use, e.g. `gpt-6-sol`.
- `model_provider`: provider id from `model_providers`, defaults to
  `openai`.
- `model_reasoning_effort`: `low | medium | high | xhigh | max | ultra`
  (availability depends on the model).
- `plan_mode_reasoning_effort`: plan-mode-only override.
- `model_reasoning_summary`: `auto | concise | detailed | none`.
- `model_verbosity`: `low | medium | high` (GPT-5-series Responses API).
- `service_tier`: `fast` or a model-advertised alternative.
- `review_model`: override model used only by `/review`.

Slash commands: `/model`, `/fast` (these adjust the config keys above
interactively, they are not config keys themselves).

API ladder: `none, minimal, low, medium, high, xhigh, max`. GPT-5.6 and
GPT-6 default to medium. Astra rejects `none`. Codex docs: Astra "begin
with Light/Low," Sol "start with Medium," Luna "start with High." OpenAI
publishes no per-level quality numbers: "keep the lightest setting that
meets your quality bar." Fast mode: 1.5x speed, 2.5x credit burn on
GPT-6/5.6/5.5, 2x on GPT-5.4. API priority tier is 2x price. Codex's
5-hour usage limit returned around 2026-07-30. (S25, S9, S32)

## Gemini API and CLI

Confirmed against geminicli.com/docs/cli/model on 2026-09-30 for the
`/model` command and `--model` flag. The settings.json and env var details
below are from the research brief's earlier fetch of ai.google.dev and
geminicli.com docs (S11, S26) since the live fetch on 2026-09-30 did not
surface those sections.

`/model` opens a picker: Auto (Gemini 3), Auto (Gemini 2.5), or Manual.
Google's own guidance: "Default to Auto... automatically selecting the
correct model based on the complexity of the task." `--model` sets a
specific model at startup. Documented model names as of the live fetch:
`gemini-3-pro-preview`, `gemini-3-flash-preview`, `gemini-2.5-pro`,
`gemini-2.5-flash`.

Reasoning control: `thinking_level` on the 3.x API, `thinking_budget` on
2.5. In the CLI, `settings.json` sets `thinkingConfig.thinkingBudget`.
Precedence for model choice: `--model` flag, then `GEMINI_MODEL` env var,
then `model.name` in settings, then a local Gemma fallback, then auto. The
CLI falls back to another model on quota or server errors. 3.8 and 3.7
Flash take `low | medium | high`, default medium. 3.6 Flash and 3.5
Flash-Lite add `minimal`, and Lite defaults to it. 3.1 Pro defaults to
high. Thinking tokens are billed as output tokens. Google's own guidance:
"Lower `thinking_level` instead of setting a small `max_output_tokens`."
Docs map minimal/low to retrieval and classification, high to "advanced
coding, math, multi-step planning." No vendor numbers per level. (S11, S26)

## Cursor

Model picker, plus Auto (Cost, Balance, Intelligence), which bills at the
routed model's list price plus a $0.25/M "Cursor Token Rate" for
third-party models. Max Mode is only on legacy request plans, adds 20%,
and extends context. Two monthly pools: Cursor Models (Grok 4.7 $2/$6,
Composer 2.5 $0.5/$2.5) and Other Models at API rates. Cursor's own
estimate: "Daily Agent users: $60 to $100 per month, power users $200
plus." (S27)

## OpenCode

`provider.<id>.models.<model>.options.reasoningEffort`, `/models` to
switch, `variant_cycle` keybind to cycle preset variants. Built-in
variants: Anthropic `high` (default) and `max`, OpenAI `none` through
`xhigh`, Google `low` and `high`. (S28)
