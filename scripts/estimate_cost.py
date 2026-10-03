#!/usr/bin/env python3
"""Estimate the cost of a task at a given model and effort level.

Two modes:

1. Token mode: you know (or can estimate) input and output token counts.
   Cost = input_tokens * input_price + output_tokens * output_price,
   where price is USD per token (list price / 1,000,000), then scaled by
   the effort multiplier for that model (see EFFORT_MULTIPLIER below).

2. Task mode (--task): no token counts, just "how much does one task like
   this cost at this model and effort," using the Artificial Analysis
   cost-per-task ladder from references/models.md (source S13), with gaps
   filled in from the measured Opus 5.5 SWE-bench Pro effort-cost ratios
   in references/effort-controls.md (source S23): medium is about 70% of
   high's cost, low about 33%, xhigh about 2.5x. Cells filled this way are
   marked as derived in DERIVED_CELLS and the CLI prints a note.

Prices and per-task costs are current as of the 2026-09-30 snapshot in
references/models.md. Re-run scripts/refresh_models.py before trusting
this for a real budget decision on a model released after that date.
"""
import argparse
import sys

# USD per million tokens, (input, output). Source: references/models.md (S2, S8, S10).
PRICES = {
    "opus-5-5": (4.0, 20.0),
    "sonnet-5-5": (2.0, 10.0),
    "fable-5-1": (10.0, 50.0),
    "haiku-4-5": (1.0, 5.0),
    "gpt-6-astra": (10.0, 50.0),
    "gpt-6-sol": (2.0, 10.0),
    "gpt-6-luna": (0.10, 0.50),
    "gemini-3-8-flash": (0.75, 3.75),
}

# Effort multiplier applied to token-mode cost. 1.0 is the model's default
# effort. These are approximations built from the measured Opus 5.5
# SWE-bench Pro ratios (references/effort-controls.md, S23): medium ~0.70x
# high, low ~0.33x high, xhigh ~2.5x high, max further above that. Applied
# uniformly across models because no vendor publishes a fuller cross-model
# table; token mode is meant for a rough estimate, not an invoice.
EFFORT_MULTIPLIER = {
    "low": 0.33,
    "medium": 0.70,
    "high": 1.00,
    "xhigh": 2.50,
    "max": 3.80,
}

# AA cost-per-task ladder, USD, from references/models.md (S13), gaps
# filled per the derivation above and flagged in DERIVED_CELLS.
TASK_COST = {
    ("opus-5-5", "low"): 0.60,
    ("opus-5-5", "medium"): 1.34,
    ("opus-5-5", "high"): 1.82,
    ("opus-5-5", "xhigh"): 3.46,
    ("opus-5-5", "max"): 5.98,
    ("sonnet-5-5", "low"): 0.356,
    ("sonnet-5-5", "medium"): 0.756,
    ("sonnet-5-5", "high"): 1.08,
    ("sonnet-5-5", "xhigh"): 2.74,
    ("sonnet-5-5", "max"): 7.60,
    ("fable-5-1", "low"): 2.37,
    ("fable-5-1", "medium"): 2.98,
    ("fable-5-1", "high"): 3.91,
    ("fable-5-1", "xhigh"): 5.98,
    ("fable-5-1", "max"): 7.63,
    ("gpt-6-astra", "low"): 0.82,
    ("gpt-6-astra", "medium"): 1.54,
    ("gpt-6-astra", "high"): 1.73,
    ("gpt-6-astra", "xhigh"): 2.31,
    ("gpt-6-astra", "max"): 3.26,
    ("haiku-4-5", "low"): 0.178,
}

DERIVED_CELLS = {
    ("opus-5-5", "low"),
    ("sonnet-5-5", "low"),
    ("sonnet-5-5", "medium"),
    ("haiku-4-5", "low"),
}


def format_usd(cost: float) -> str:
    whole, fractional = f"{cost:.8f}".split(".")
    fractional = fractional.rstrip("0").ljust(4, "0")
    return f"${whole}.{fractional}"


def token_cost(model: str, effort: str, input_tokens: int, output_tokens: int) -> float:
    if model not in PRICES:
        raise ValueError(f"unknown model '{model}', choices: {sorted(PRICES)}")
    if effort not in EFFORT_MULTIPLIER:
        raise ValueError(f"unknown effort '{effort}', choices: {sorted(EFFORT_MULTIPLIER)}")
    if input_tokens < 0 or output_tokens < 0:
        raise ValueError("token counts must be non-negative")
    in_price, out_price = PRICES[model]
    base = (input_tokens * in_price + output_tokens * out_price) / 1_000_000
    return base * EFFORT_MULTIPLIER[effort]


def task_cost(model: str, effort: str):
    key = (model, effort)
    if key not in TASK_COST:
        raise ValueError(
            f"no per-task cost for {model} at {effort}. "
            f"Known combinations: {sorted(TASK_COST)}"
        )
    return TASK_COST[key], key in DERIVED_CELLS


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Estimate task cost for a model and effort level.",
        epilog="Examples:\n"
               "  estimate_cost.py --model sonnet-5-5 --effort medium \\\n"
               "      --input-tokens 8000 --output-tokens 2000\n"
               "  estimate_cost.py --task --model opus-5-5 --effort high\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--model", required=True,
                    help=f"one of: {', '.join(sorted(PRICES))}")
    p.add_argument("--effort", required=True,
                    help=f"one of: {', '.join(sorted(EFFORT_MULTIPLIER))}")
    p.add_argument("--input-tokens", type=int, default=None)
    p.add_argument("--output-tokens", type=int, default=None)
    p.add_argument("--task", action="store_true",
                    help="use the AA cost-per-task ladder instead of token counts")
    p.add_argument("--json", action="store_true", help="print JSON instead of text")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.task:
            cost, derived = task_cost(args.model, args.effort)
            result = {
                "mode": "task",
                "model": args.model,
                "effort": args.effort,
                "usd": round(cost, 8),
                "derived": derived,
            }
        else:
            if args.input_tokens is None or args.output_tokens is None:
                print("error: --input-tokens and --output-tokens are required "
                      "unless --task is set", file=sys.stderr)
                return 2
            cost = token_cost(args.model, args.effort, args.input_tokens, args.output_tokens)
            result = {
                "mode": "tokens",
                "model": args.model,
                "effort": args.effort,
                "input_tokens": args.input_tokens,
                "output_tokens": args.output_tokens,
                "usd": round(cost, 8),
            }
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.json:
        import json
        print(json.dumps(result))
    else:
        note = " (derived estimate, not a published figure)" if result.get("derived") else ""
        print(f"{format_usd(result['usd'])}{note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
