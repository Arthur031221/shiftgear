# AGENTS.md

Fallback instructions for coding agents that read `AGENTS.md` instead of
`SKILL.md`: Codex CLI, Cursor, and OpenCode all look for this file. Claude
Code and Gemini CLI (once a skill is installed) read `SKILL.md` directly.
This file exists so the same routing logic applies everywhere.

## What to do

Before starting a task, decide which model and which effort or reasoning
level fits it, state the choice and why in one line, then apply it with
the tool's own model/effort controls before writing code.

Read `SKILL.md` in this repository for the full classifier, the output
template, and the hard rules (never downshift mid-conversation, never use
max effort without an output ceiling, risk words never route below a
mid-tier model). Read `references/decision-table.md` (or
`assets/decision-table.csv`) for the per-task routing table this is built
on.

## Quick version, if you only read this file

1. Classify the task: how deep does the reasoning need to be, how much is
   at stake, how long will the loop run, how ambiguous is the ask. Take
   the worst of those four, not the average.
2. Check the hard floors first: production, delete, migration, auth,
   payment, or security in the task means never the cheapest tier.
   Context over 180K tokens means never the smallest model. Visual input
   means the top-tier model. Unattended runs over 30 minutes need a model
   with a real extra-high reasoning setting, not a fixed-budget one.
3. Pick effort: default medium, drop to low only if the change is a
   one-sentence diff with something that can verify it, go high when
   verification matters, reserve the highest setting for a measured gain
   and always pair it with an output token ceiling.
4. Apply it in your tool's own syntax:
   - **Codex CLI**: `model = "gpt-6-sol"` and
     `model_reasoning_effort = "medium"` in `config.toml`, or `/model`.
   - **Cursor**: the model picker, or Auto (Cost / Balance / Intelligence).
   - **OpenCode**: `/models`, or the `variant_cycle` keybind.
5. Say what you picked and why, in one line, before you start working.
   Use the same template as SKILL.md section 4:

```
Route: <model> at <effort>. Mode: <max-quality|balanced|quota-saver>. Why: <one line>. Cheaper: <alternative>. Escalate if: <condition>, then <fallback>. Quota: <state or "unknown">. Apply: <exact command>
```

For anything not covered here, including the full per-task table, the
measured cost-vs-effort curves, and the quota mechanics behind
quota-saver mode, read `SKILL.md` and `references/` directly. They are
plain Markdown, no special tooling required to read them.
