# Contributing

## Reporting a stale price or a wrong claim

Open an issue with the source URL and the date you checked it. Anything
in `references/` should trace back to a source key in
`references/evidence.md`. If you cannot find the number there, say so.

## Changing a price, a benchmark number, or a model row

1. Run `python3 scripts/refresh_models.py` first, and paste its output in
   the PR description.
2. Every changed cell needs a source URL and the date you fetched it, in
   the PR description at minimum, ideally also as an inline citation in
   the reference file itself.
3. Do not add a number without a source, including a number you are
   confident about from memory. This project exists because stale prices
   in routing skills waste people's money.

## Adding a new model

Add it to the right table in `references/models.md`, add its price to
`scripts/estimate_cost.py` (`PRICES`, and `TASK_COST` if you have a
published per-task cost), and add it to `TRACKED_MODELS` in
`scripts/refresh_models.py` if it is on OpenRouter under a stable slug.

## Adding a new task category to the decision table

Add a row to both `references/decision-table.md` and
`assets/decision-table.csv` (keep them in sync by hand, they are small),
and add a matching entry to `BALANCED_ROUTE` if you also touch
`bench/`. State your rationale and cite a source the same way the
existing rows do.

## Running the tests

```
uv run --with pytest pytest
```

or, with pytest already installed:

```
pytest
```

## Lint

```
uvx ruff check .
```

## Scope

This is a routing skill, not a proxy or a gateway. It tells you what to
run, it does not run your agent for you and it does not hold API keys.
Keep it that way: PRs that turn this into a network service or add a
dependency on a paid backend will be declined.
