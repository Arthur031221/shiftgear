# Decision table

Snapshot date: 2026-09-30. This is the table SKILL.md's classifier routes
into. The machine-readable copy is assets/decision-table.csv, kept in sync
by hand (both are small enough that a script would be more code than the
table itself).

## Contents

- [Legend](#legend)
- [The table](#the-table)
- [Reading the fallback column](#reading-the-fallback-column)

## Legend

F = Fable 5.1, O = Opus 5.5, S = Sonnet 5.5, H = Haiku 4.5, Astra / Sol /
Luna = GPT-6 family, G = Gemini 3.8 Flash, L = local or open-weight (Qwen
3.8-27B, GLM-5.3-Flash, MiMo-V2.6, DeepSeek V4.1 Flash). Fallback is what
to do when the Claude 5-hour or model-family limit hits mid-task.

## The table

| Task | Max quality | Balanced | Quota saver | Fallback at limit | Rationale | Source |
|---|---|---|---|---|---|---|
| Trivial edit (rename, typo, log line) | O low | S low | H, Luna low, or L | H or Luna | Smaller model for precisely describable edits. Luna + Low is built for "fine-grained edits". Skip plan mode | S31, S25, S30 |
| Boilerplate and scaffolding | S medium | S low | Luna medium, G low, or L | Luna | Luna + Medium is built for "creating from clear briefs". Sonnet is Claude Code's own default for daily coding | S25, S21 |
| Writing tests | O medium | S medium | S low with "run a real check" prompt | Sol medium | Sonnet 5.5 at low skips verification unless explicitly told to check | S24 |
| Refactor (well specified, multi-file) | O medium | S medium then high | S low, rerun failures at high | Sol medium | Sonnet 5.5 guidance: medium for well specified, high for longer. Low-then-rerun matches all-high pass rate at about half the cost | S24, S23 |
| Hard debugging and root cause | O high, xhigh only if measured gain | O medium | O low, escalate on failure | Astra high or Sol xhigh | Opus 5.5 medium is at or above Opus 5 high, and xhigh is only +1.4 points at 2.5x cost. OpenAI's own guide maps "hard reasoning, complex debugging" to high | S24, S23, S9 |
| Architecture and design | F high or O xhigh | O medium in plan mode, then S | O low plan, S execute (`opusplan`) | Astra medium | `opusplan` exists specifically for this split. Astra + Medium is built for "ambitious projects" | S21, S25 |
| Code review | O medium in a fresh subagent | S high | S medium | Sol xhigh | Opus 5.5 catches more bugs with fewer false alarms. Sol + Extra High is built for code review. A reviewer must run in a fresh context, not the implementer's | S24, S25, S30 |
| Security review | O max with `max_tokens` 128K | O high | O medium | Astra high | `max` is named for "finding security vulnerabilities". Cheap tiers are forbidden on risk words by every serious router studied | S21, S36 |
| Migration (many files, mechanical) | O medium orchestrator + S workers | S medium via batch | L or Luna workers, S reviews | Luna workers | Orchestrator pattern roughly halves cost. Fan out with `claude -p`. Migration is a hard-floor risk word, never route it to the cheapest tier | S23, S30, S36 |
| Documentation | S medium | S low | Luna or G low | Luna | Sol + Low is built for "focused writing and editing" | S25 |
| Data analysis | O medium plus code execution | S medium | G medium or Luna medium | Sol medium | Files through code execution: 25/25 solved at $0.40 versus 6/25 for pasted data | S23 |
| Research and reading papers | F low for long loops | O medium | S medium | Sol medium | Fable 5.1 scored equally at low, medium, and high on DeepResearch Bench II | S23 |
| Long agentic run, over 30 minutes unattended | F high or O xhigh plus a task budget | O medium plus a continuation prompt | O low, rerun failures | Wait and auto-continue, or Astra medium | `xhigh` is defined for exactly this case. Task budgets cost -44% for -3 points. Claude Code auto-continues after a quota reset | S22, S23, S30 |
| Repetitive transforms (hundreds of files) | S low | H or Luna low | L (Qwen3.8-27B, GLM-5.3-Flash) | L | Luna gives 350-3,000 messages per 5-hour window on Plus versus Astra's 5-45. Open-weight models handle bulk work at near-zero marginal cost | S25, S32 |
| UI work | O medium with a named anti-pattern list | S medium | G medium | Sol medium | Opus 5.5's frontend defaults need an explicit list of patterns to avoid. Gemini 3.8 Flash sits at Arena rank 10 for a fraction of the price | S24, S14 |
| Performance work (profiling, hot loops) | O high | O medium | S high | Astra high | This needs a verification loop more than raw model strength. Effort matters more than model choice here | S30 |
| Writing specs and interviews | O medium with the question tool | S medium | S low | Sol medium | Interview-then-fresh-session is Claude Code's own documented pattern. Sol + Medium targets "workflows that need judgment" | S30, S25 |
| Quota exhausted, any task | | Sonnet family (survives an Opus-family limit) | Luna via Codex or L | Usage credits at API rates | Model-family limits are separate from each other. Session and weekly caps are not | S30 |

## Reading the fallback column

"Fallback at limit" is what to switch to when the active tool's quota is
gone mid-task, not a general second choice. It assumes you are staying
inside the same conversation if at all possible: switching models
mid-session resets the prompt cache and forces a full re-read of the
conversation, so a fallback is worth it only when the alternative is
actually blocked, not merely more expensive. (S30)
