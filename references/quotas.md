# Subscription quotas

Snapshot date: 2026-09-30. Quota mechanics change more often than prices.
Treat everything here as directional. `scripts/quota_state.sh` reads
whatever Claude Code actually exposes locally. This file is background for
when it cannot.

## Contents

- [Claude](#claude)
- [ChatGPT / Codex](#chatgpt--codex)
- [Google](#google)
- [Cursor](#cursor)
- [What this means for routing](#what-this-means-for-routing)

## Claude

Pro: $20/month, $17/month billed annually. A 5-hour session window plus a
weekly cap "across all models." Fable consumes at "50% of weekly limits."
Model-family limits also exist independently ("You've hit your Opus
limit," "Sonnet limit"). Session and weekly caps are shared across models,
so switching with `/model` does not help with those specifically. At the
limit: wait, upgrade, or pay standard API rates as usage credits.
Occasional "limit resets" restore a window early. (S29, S30)

Max 5x ($100) and Max 20x ($200), monthly only: "5x or 20x the Pro plan's
per-session usage." Claude Code auto-waits and continues after a reset
(v2.1.234+, re-arms up to 2 times). (S29, S30)

Cache TTL is 1 hour on subscription plans, 5 minutes (once) on usage
credits. (S30)

Community measurements: claude-meter (alpha, 2026-03) found the 5-hour
meter is better explained by price-weighted usage than raw tokens, with
cache reads weighted much more cheaply than fresh tokens. One session's
5-hour budget was estimated at $35 to $401, median $164. (S33) HN
2026-09-28: an Opus 5.5 agent team at medium effort "burned through the
20x weekly limit in 2.5 days." Two users report Max 5x now suffices for 2
to 3 parallel Opus 5.5 sessions. Another user drops to Sonnet after
hitting a session limit. (S32)

Team and Enterprise: $20-25 and $100-125 per seat, premium usage at 5x.
Enterprise average reported as "$13 per developer per active day, $150 to
250 per month." (S29, S30)

## ChatGPT / Codex

Plan prices were not fetchable for this brief (openai.com and
help.openai.com returned 403). Codex's own "estimated local messages per
five-hour period," by plan and model:

| Model | Plus | Pro 5x | Pro 20x |
|---|---|---|---|
| Luna | 350-3,000 | 1,750-14,000 | 7,000-56,000 |
| Sol | 15-150 | 70-700 | 300-3,000 |
| Astra | 5-45 | 25-225 | 100-900 |

Business equals Plus. "Weekly limits may also apply." Usage varies with
context size, reasoning effort, tool use, retrieval, and caching. Fast
mode costs 2.5x credits. Plus and Pro can buy extra credits. HN: users
downgrade Sol to Terra to stay inside the 5-hour window. (S25, S32)

## Google

Google AI Pro $19.99/month, Ultra $99.99/month, a $199.99 tier also
exists. Gemini CLI request caps (requests, not tokens): free Google
account 1,000/day, API-key free tier 250/day (Flash only), AI Pro
1,500/day, AI Ultra 2,000/day, Code Assist Standard 1,500/day, Enterprise
2,000/day. The CLI prompts to fall back to a smaller model on quota
errors. (S34, S26)

## Cursor

Pro $20, Pro+ $60, Ultra $200, Teams $40/user. Two monthly pools (see
references/effort-controls.md Cursor section), on-demand overage at the
same per-model rates. (S27)

## What this means for routing

None of this is exact, and shiftgear does not pretend otherwise. The
practical rule, stated in SKILL.md: auto-switch to quota-saver mode when
the 5-hour window is over 80% consumed, or the weekly window is over 60%
consumed with more than 2 days left in it. Below that, route on task
merits. Claude Code's own guidance for unexpectedly high spend:
"usually traces back to long sessions never cleared or Opus left as the
default." (S30)
