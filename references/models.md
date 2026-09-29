# Model landscape

Snapshot date: 2026-09-30. Prices are USD per million tokens, input / output,
standard tier, unless noted. AA = Artificial Analysis Intelligence Index.
"$/task" is AA's cost per index task at that effort level. Every row keeps
its source key (see references/evidence.md for the full URL and fetch date
behind each key). Run `scripts/refresh_models.py` before trusting a price
you are about to quote to a user: this file goes stale, on purpose it is
not embedded in SKILL.md.

## Contents

- [How to read this file](#how-to-read-this-file)
- [Anthropic](#anthropic)
- [OpenAI](#openai)
- [Google](#google)
- [Other frontier and open-weight](#other-frontier-and-open-weight)
- [Small typed-decision models](#small-typed-decision-models)
- [Leaderboard status](#leaderboard-status)
- [Old patterns](#old-patterns)

## How to read this file

Each row is one model. "Effort control" lists the levels that model
actually accepts, not the full ladder shiftgear supports elsewhere: a
Haiku row with no effort levels means the API gives you no lever there,
full stop. "Headline numbers" are the benchmark results worth quoting in
an apply message. Do not invent numbers that are not in this table or in
references/evidence.md.

## Anthropic

| Model (ID) | Released | Price in/out | Context / max out | Effort control | Headline numbers | Source |
|---|---|---|---|---|---|---|
| Claude Fable 5.1 `claude-fable-5-1` | 2026-09-01 | $10 / $50, cache read $0.25 | 1M / 128K | adaptive always on: low, medium, high, xhigh, max, default high | AA 53 (max $7.63/task, xhigh 53 at $5.98, high 51 at $3.91, medium 49 at $2.98, low 47 at $2.37). Terminal-Bench 4.0 55.8%, Mythos 5.1 60.9. Arena text 1501, rank 5 | S1, S2, S3, S5, S13, S14 (2026-09-29/30) |
| Claude Opus 5.5 `claude-opus-5-5` | 2026-09-22 | $4 / $20, cache read $0.20, fast mode $8 / $40 | 1M / 128K | adaptive always on: low, medium, high, xhigh, max, default medium | AA 58, rank 1 (max $5.98, xhigh 56 at $3.46, high 54 at $1.82, medium 51 at $1.34). TB4.0 66.4, FrontierCode 54.4, OSWorld 2.1 81.8. Arena text 1509, rank 1. "40% less than Opus 5 on typical workloads," "over 30% faster" | S1, S2, S3, S4, S13, S14 (2026-09-29/30) |
| Claude Sonnet 5.5 `claude-sonnet-5-5` | 2026-09-28 | $2 / $10 | 1M / 128K | adaptive: low, medium, high, xhigh, max. API default high, Claude Code default medium. `between_tools` uses the lowest thinking level | AA 56, rank 3 (max $7.60/task at ~193k output tokens/task, xhigh 52 at $2.74, high 47 at $1.08). TB4.0 70.6 vendor harness, 63.6 AA harness (AA's top TB4.0 score). 136 tokens/second | S1, S2, S3, S6, S13, S21, S24 (2026-09-28/30) |
| Claude Haiku 4.5 `claude-haiku-4-5-20251001` | 2025-10-15 | $1 / $5 | 200K / 64K | manual extended thinking via `budget_tokens` only, no effort param. Retirement not sooner than 2026-10-15 | SWE-bench Pro 39.45 | S3, S16 |
| Legacy: Opus 5, 4.8, 4.7, 4.6 | | $5/$25 | | Opus 4.6 lacks xhigh | Opus 5 TB4.0 52.3 | S2, S4, S21 |
| Legacy: Sonnet 5 | | $2/$10 | | | | S2 |
| Legacy: Sonnet 4.6 | | $3/$15 | | lacks xhigh | | S2, S21 |

## OpenAI

| Model (ID) | Released | Price in/out | Context / max out | Effort control | Headline numbers | Source |
|---|---|---|---|---|---|---|
| GPT-6 Astra `gpt-6-astra` | 2026-09-03 | $10 / $1 cached / $50, above 272K input: 2x input, 1.5x output | 1.05M (922K input) / 128K | low, medium, high, xhigh, max, no `none`, default medium. `reasoning.mode` standard or pro | AA 53 (max $3.26, xhigh 52 at $2.31, high 51 at $1.73, medium 50 at $1.54, low 46 at $0.82). TB4.0 57.9, TB-Science 64.6 | S7, S8, S9, S4, S13 |
| GPT-6 Sol `gpt-6-sol` | 2026-09-22 | $2 / $0.20 cached / $10 | 1.05M / 128K | none, low, medium, high, xhigh, max, default medium | AA 48 (max $1.05/task). Simon Willison's new default alongside Opus 5.5 | S8, S20, S13 |
| GPT-6 Luna `gpt-6-luna` | 2026-09-22 | $0.10 / $0.01 cached / $0.50 | 1.05M / 128K | none to max, Codex docs say start High | AA 37, 148 tokens/second. "Fast and competent" in Simon Willison's agent demo | S8, S25, S13, S20 |
| GPT-5.6 Sol, Terra, Luna | GA 2026-07-09 | $4/$20, $2/$12, $0.20/$1.20 | 1.05M / 128K | same ladder as 6-series | GPT-5.6 Sol TB4.0 37.3. Arena `gpt-5.6-sol-xhigh` 1483 | S18, S8, S4, S14 |
| GPT-5.5, 5.4, 5.3-codex, o3, o4-mini | | $5/$30, $2.50/$15, $1.75/$14, $2/$8, $1.10/$4.40 | | | GPT-5.4 xhigh 59.1 SWE-bench Pro. GPT-5.5 retires 2026-10-14 in Codex | S8, S16, S25 |

## Google

| Model (ID) | Released | Price in/out | Context / max out | Effort control | Headline numbers | Source |
|---|---|---|---|---|---|---|
| Gemini 3.8 Flash `gemini-3.8-flash` | 2026-09-02 | $0.75 / $3.75 until 2026-12-31, then $1.50 / $7.50 | 1M / 64K | `thinking_level` low, medium, high, default medium | AA 41, 242 tokens/second. HLE-Verified 54.9, DeepSWE above 70, CWE-Bench 47.2. Arena 1492, rank 10 | S10, S11, S12, S38, S13, S14 |
| Gemini 3.7 / 3.6 Flash | 2026-08-13 / 07-21 | $0.75/$3.75 | 1M / 64K | 3.6 Flash adds `minimal` | | S18, S10 |
| Gemini 3.5 Flash | 2026-05-19 | $1.50/$9 | 1M / 64K | | | S18, S10 |
| Gemini 3.5 Flash-Lite | 2026-07-21 | $0.30/$2.50 | 1M / 64K | adds `minimal`, default minimal | | S18, S10, S11 |
| Gemini 3.1 Pro Preview | 2026-02-19 | $2/$12 up to 200K, $4/$18 above | 1M / 64K | low, medium, high, default high | SWE-bench Pro 46.1. Google's only Pro on the API price list | S10, S16 |

## Other frontier and open-weight

| Model | Released | Price in/out | Notes | Headline numbers | Source |
|---|---|---|---|---|---|
| Muse Spark 1.3 (Meta, proprietary) | 2026-09-02 | $1.25 / $4.25, 1M context | max and xhigh variants | AA 48 ($1.60/task), 177 tokens/second. Muse Spark 1.1 tops SWE-bench Pro public at 61.5 | S19, S13, S16 |
| Grok 4.7 (xAI) | 2026-09-21 | $2 / $6, 500K context | xhigh, high | AA 46 | S18, S20, S13 |
| Qwen3.8 Max `0902` | 2026-09-03 | $2/$6, proprietary, 984K context | thinking on by default | AA 45 ($5.41/task) | S13, S18 |
| Qwen3.8 27B (Apache-2.0) | 2026-08-14 | open weights | 262K native, 1M extended | Self-reported SWE-bench Pro 61.7 in Claude Code harness, TB2.1 73.0, LCB v6 90.3, GPQA 89.2. HN: locally "competes with Opus 4.8 on programming" but verbose reasoning | S19, S32 |
| Qwen3.8 Flash-Next | 2026-08-27 | $0.15/$0.47 | | | S18, S19 |
| GLM-5.3 (Z.ai, open weights) | API 2026-08-18, weights 09-04 | $1.40/$4.40 AA, or $0.19/$4.00 OpenRouter | 1M to 1.3M, 753B total / 40B active | AA 45, rank 2 open ($2.01/task). TB2.1 88.2, TB3.0 28.3, DeepSWE 66.9 | S13, S18, S19 |
| GLM-5.3-Flash | | $0.15/$0.50 | | | S18 |
| DeepSeek V4.1 Flash (MIT) | 2026-09-10 | $0.30 / $1.20 | 1M, 552B total / 16B active | AA 39, $0.27/task, 215 tokens/second. GPQA 90.9, DeepSWE 74.2, TB4.0 31.2. Rank 1 by weekly OpenRouter tokens | S13, S19, S18 |
| Kimi K3 (Moonshot) | 2026-07-16, weights 07-27 | $3 / $15, cache hit $0.30 | 1M, 2.8T total / 104B active | AA 44. GPQA 93.5, DeepSWE 67.5, TB2.1 88.3. Arena `kimi-k3-max` 1488 | S19, S14 |
| MiMo-V2.6-Pro / Flash (Xiaomi, MIT) | 2026-09-21 | $0.43/$0.87, $0.14/$0.28 | 1M, 1.0T total / 42B active | AA 46, rank 1 open-weight, $0.13/task. HN: "new meta: Astra-6-Max for orchestration, MiMo for grunt work" | S13, S18, S32 |
| Llama 4, Mistral Large 3 / Medium 3.5 | 2025-04, 2026-07 | Devstral 2512 $0.40/$2 | | Not in any 2026 coding top list | S18 |

## Small typed-decision models

| Model | Released | Price | Output | Notes | Source |
|---|---|---|---|---|---|
| Jev (TypeSafe, closed API) | September 2026 | $0.042/M input, output free | typed choice, score, yes/no, not free text | ~0.4s/decision, 67.8% agreement vs GPT-5.6 Terra at 67.9% at 76x the cost | S37 |
| Laya (Convai, Apache-2.0) | September 2026 | | typed | 32.8ms p50 on a T4. Simon Willison: "not great with numbers, dates, or adversarial content" | S37, S20 |

Useful as a sub-second classifier for routing itself, not as a coder. shiftgear does not depend on either: the classifier in SKILL.md is meant to run as a step inside the agent already doing the task, not as a separate paid call.

## Leaderboard status

SWE-bench Verified is stale (newest entries 2026-02-17, top 79.2). SWE-bench
Pro public stops at GPT-5.4 and Opus 4.6. Aider polyglot last updated
October 2025 (`gpt-5` high 88.0). Terminal-Bench 4.0 is what vendors and AA
lead with now. Vendor-reported harness numbers run about 7 points above
AA's own harness. OpenRouter weekly top-by-tokens to 2026-09-28: DeepSeek
V4.1 Flash, Space Bunny Alpha, GLM 5.3 Flash, Hy4 preview, GPT-5.6 Luna,
DeepSeek V4 Flash 0731, MiMo-V2.6-Flash, Nemotron 3 Ultra free, GPT-6 Luna,
DeepSeek V4 Flash 0423. (S13, S15, S16, S17, S18)

## Old patterns

<details>
<summary>Haiku 4.5 retirement (not sooner than 2026-10-15)</summary>

Haiku 4.5 has no effort parameter and a 200K window. Anthropic has said it
will not retire sooner than 2026-10-15. When `scripts/refresh_models.py`
reports today's date past that floor, treat any Haiku 4.5 route in
references/decision-table.md as needing a replacement check against
whatever Haiku generation is current, before routing quota-saver traffic
to it. (S3)
</details>

<details>
<summary>Opus/Sonnet 4.6 effort ladder</summary>

Opus 4.6 and Sonnet 4.6 do not support `xhigh`. If a route in the decision
table names 4.6 explicitly instead of 5.5, drop to the four-level ladder
(low, medium, high, max). (S21)
</details>
