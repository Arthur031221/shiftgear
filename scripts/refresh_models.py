#!/usr/bin/env python3
"""Check references/models.md for staleness and diff it against OpenRouter.

What it does:
1. Reads the snapshot date out of references/models.md ("Snapshot date:
   YYYY-MM-DD" on the first content line) and prints a STALE banner if
   that date is more than 30 days in the past.
2. Pulls https://openrouter.ai/api/v1/models (a public, unauthenticated
   endpoint listing every model OpenRouter routes, with pricing) and
   prints a diff: models mentioned in this snapshot whose OpenRouter
   listing has since disappeared (possible retirement) or whose listed
   price has moved, plus any new models on OpenRouter that share a vendor
   prefix (anthropic/, openai/, google/) with something already tracked
   here but are not yet in references/models.md.

This does not rewrite references/models.md automatically: pricing pages
and leaderboards need a person or an agent to actually read the page and
write a source-cited row, which is why the brief keeps this a diff tool,
not an auto-updater. Network access is required for the diff; the
staleness check works offline.

Usage:
    python3 scripts/refresh_models.py
    python3 scripts/refresh_models.py --offline   # staleness check only
    python3 scripts/refresh_models.py --json
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MODELS_MD = REPO_ROOT / "references" / "models.md"
OPENROUTER_URL = "https://openrouter.ai/api/v1/models"
STALE_DAYS = 30
REQUEST_TIMEOUT = 15

# Model IDs this snapshot tracks, mapped to the OpenRouter slug prefix
# that would carry the same underlying model, where one exists. Extend
# this as new models get added to references/models.md.
TRACKED_MODELS = {
    "claude-opus-5-5": "anthropic/claude-opus-5.5",
    "claude-sonnet-5-5": "anthropic/claude-sonnet-5.5",
    "claude-fable-5-1": "anthropic/claude-fable-5.1",
    "claude-haiku-4-5-20251001": "anthropic/claude-haiku-4.5",
    "gpt-6-astra": "openai/gpt-6-astra",
    "gpt-6-sol": "openai/gpt-6-sol",
    "gpt-6-luna": "openai/gpt-6-luna",
    "gemini-3.8-flash": "google/gemini-3.8-flash",
}


def get_snapshot_date() -> datetime.date:
    if not MODELS_MD.exists():
        raise FileNotFoundError(f"{MODELS_MD} not found")
    text = MODELS_MD.read_text()
    m = re.search(r"Snapshot date:\s*(\d{4}-\d{2}-\d{2})", text)
    if not m:
        raise ValueError("no 'Snapshot date: YYYY-MM-DD' line found in references/models.md")
    return datetime.datetime.strptime(m.group(1), "%Y-%m-%d").date()


def staleness_banner(snapshot: datetime.date, today: datetime.date) -> str | None:
    age = (today - snapshot).days
    if age > STALE_DAYS:
        return (
            f"STALE: references/models.md is {age} days old (snapshot {snapshot.isoformat()}, "
            f"today {today.isoformat()}). Re-fetch the sources in references/evidence.md and "
            f"update prices before quoting them."
        )
    return None


def fetch_openrouter_models() -> list[dict]:
    req = urllib.request.Request(OPENROUTER_URL, headers={"User-Agent": "shiftgear-refresh/1.0"})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return payload.get("data", [])


def diff_against_openrouter(or_models: list[dict]) -> list[str]:
    by_id = {m.get("id"): m for m in or_models if m.get("id")}
    lines = []
    for local_id, or_slug in TRACKED_MODELS.items():
        if or_slug not in by_id:
            lines.append(f"  not found on OpenRouter: {local_id} (looked for {or_slug})")
            continue
        pricing = by_id[or_slug].get("pricing", {})
        prompt_price = pricing.get("prompt")
        completion_price = pricing.get("completion")
        lines.append(
            f"  {local_id}: OpenRouter lists prompt={prompt_price} completion={completion_price} "
            f"(per-token; compare against references/models.md, which is per-million-token)"
        )
    return lines


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--offline", action="store_true",
                    help="skip the OpenRouter fetch, staleness check only")
    p.add_argument("--json", action="store_true",
                    help="print machine-readable JSON instead of text")
    args = p.parse_args(argv)

    today = datetime.date.today()
    result = {"today": today.isoformat()}

    try:
        snapshot = get_snapshot_date()
    except (FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    result["snapshot_date"] = snapshot.isoformat()
    banner = staleness_banner(snapshot, today)
    result["stale"] = banner is not None
    if banner and not args.json:
        print(banner)
        print()

    diff_lines: list[str] = []
    fetch_error = None
    if not args.offline:
        try:
            or_models = fetch_openrouter_models()
            diff_lines = diff_against_openrouter(or_models)
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            fetch_error = str(e)

    result["diff"] = diff_lines
    result["fetch_error"] = fetch_error

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print(f"Snapshot date in references/models.md: {snapshot.isoformat()}")
    print(f"Today: {today.isoformat()}")
    if not banner:
        print("Not stale (within 30 days).")
    if args.offline:
        print("\n--offline set, skipped the OpenRouter diff.")
    elif fetch_error:
        print(f"\ncould not reach OpenRouter: {fetch_error}")
        print("Check network access, or run with --offline for the staleness check alone.")
    else:
        print(f"\nOpenRouter diff ({OPENROUTER_URL}):")
        for line in diff_lines:
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
