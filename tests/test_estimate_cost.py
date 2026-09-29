import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "estimate_cost.py"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import estimate_cost as ec


def test_token_cost_scales_with_tokens():
    small = ec.token_cost("sonnet-5-5", "high", 1000, 1000)
    big = ec.token_cost("sonnet-5-5", "high", 2000, 2000)
    assert big == 2 * small


def test_token_cost_matches_list_price_at_high_effort():
    # Sonnet 5.5 high effort has multiplier 1.0, so cost should equal
    # plain list price: $2/M in, $10/M out.
    cost = ec.token_cost("sonnet-5-5", "high", 1_000_000, 1_000_000)
    assert abs(cost - (2.0 + 10.0)) < 1e-9


def test_effort_multiplier_orders_low_below_high_below_max():
    low = ec.token_cost("opus-5-5", "low", 10_000, 10_000)
    high = ec.token_cost("opus-5-5", "high", 10_000, 10_000)
    xhigh = ec.token_cost("opus-5-5", "xhigh", 10_000, 10_000)
    maxc = ec.token_cost("opus-5-5", "max", 10_000, 10_000)
    assert low < high < xhigh < maxc


def test_unknown_model_raises():
    try:
        ec.token_cost("not-a-model", "medium", 100, 100)
        assert False, "expected ValueError"
    except ValueError as e:
        assert "not-a-model" in str(e)


def test_unknown_effort_raises():
    try:
        ec.token_cost("sonnet-5-5", "not-an-effort", 100, 100)
        assert False, "expected ValueError"
    except ValueError as e:
        assert "not-an-effort" in str(e)


def test_task_cost_returns_known_value():
    cost, derived = ec.task_cost("opus-5-5", "high")
    assert cost == 1.82
    assert derived is False


def test_task_cost_flags_derived_cells():
    cost, derived = ec.task_cost("sonnet-5-5", "low")
    assert derived is True
    assert cost > 0


def test_task_cost_unknown_combination_raises():
    try:
        ec.task_cost("gemini-3-8-flash", "medium")
        assert False, "expected ValueError"
    except ValueError:
        pass


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, check=False,
    )


def test_cli_token_mode_json():
    r = run_cli("--model", "sonnet-5-5", "--effort", "medium",
                "--input-tokens", "1000", "--output-tokens", "500", "--json")
    assert r.returncode == 0
    payload = json.loads(r.stdout)
    assert payload["mode"] == "tokens"
    assert payload["usd"] > 0


def test_cli_task_mode_json():
    r = run_cli("--task", "--model", "opus-5-5", "--effort", "high", "--json")
    assert r.returncode == 0
    payload = json.loads(r.stdout)
    assert payload["usd"] == 1.82
    assert payload["derived"] is False


def test_cli_missing_tokens_errors_cleanly():
    r = run_cli("--model", "sonnet-5-5", "--effort", "medium")
    assert r.returncode == 2
    assert "required" in r.stderr


def test_cli_bad_model_errors_cleanly():
    r = run_cli("--model", "nope", "--effort", "medium",
                "--input-tokens", "1", "--output-tokens", "1")
    assert r.returncode == 1
    assert "unknown model" in r.stderr


def test_cli_help_works():
    r = run_cli("--help")
    assert r.returncode == 0
    assert "--model" in r.stdout
