# Changelog

## 0.1.0 (2026-09-30)

Initial release.

- SKILL.md: model and effort routing for Claude Code, Codex CLI, Gemini
  CLI, Cursor, and OpenCode, with a 30-second classifier, a budget mode
  (max-quality, balanced, quota-saver), an output template, per-agent
  apply instructions, hard rules, a failure-mode checklist, and an update
  cadence.
- references/: model landscape, effort controls per tool with measured
  cost curves, subscription quotas, the full decision table, and a
  complete evidence list, each source-cited and dated.
- assets/decision-table.csv: machine-readable copy of the decision table.
- scripts/refresh_models.py: staleness check plus a live diff against
  openrouter.ai/api/v1/models.
- scripts/estimate_cost.py: token-mode and task-mode cost estimation,
  with tests.
- scripts/quota_state.sh: reads local Claude Code usage state where
  available, prints `unknown` gracefully otherwise.
- AGENTS.md: fallback routing instructions for tools that read AGENTS.md
  instead of SKILL.md.
- bench/: real-prompt benchmark (n=31, this machine's full local Claude
  Code history after filtering), classifier agreement, and an estimated
  cost comparison against always-Opus-5.5-at-high.
