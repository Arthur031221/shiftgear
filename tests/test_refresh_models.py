import datetime
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import refresh_models as rm


def test_get_snapshot_date_reads_real_file():
    d = rm.get_snapshot_date()
    assert isinstance(d, datetime.date)


def test_staleness_banner_none_when_fresh():
    snapshot = datetime.date(2026, 9, 1)
    today = datetime.date(2026, 9, 15)
    assert rm.staleness_banner(snapshot, today) is None


def test_staleness_banner_fires_past_30_days():
    snapshot = datetime.date(2026, 1, 1)
    today = datetime.date(2026, 3, 1)
    banner = rm.staleness_banner(snapshot, today)
    assert banner is not None
    assert "STALE" in banner
    assert "2026-01-01" in banner


def test_staleness_banner_boundary_at_30_days():
    snapshot = datetime.date(2026, 1, 1)
    assert rm.staleness_banner(snapshot, snapshot + datetime.timedelta(days=30)) is None
    assert rm.staleness_banner(snapshot, snapshot + datetime.timedelta(days=31)) is not None


def test_diff_against_openrouter_handles_missing_ids():
    fake_payload = [{
        "id": "openai/gpt-6-sol",
        "pricing": {"prompt": "0.000002", "completion": "0.00001"},
    }]
    lines = rm.diff_against_openrouter(fake_payload)
    assert any("gpt-6-sol" in line and "not found" not in line for line in lines)
    assert any("not found on OpenRouter" in line for line in lines if "claude-opus-5-5" in line)


def test_main_offline_does_not_touch_network(capsys):
    rc = rm.main(["--offline"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Snapshot date" in out
    assert "skipped the OpenRouter diff" in out
    assert "openrouter.ai/api" not in out


def test_main_offline_json(capsys):
    rc = rm.main(["--offline", "--json"])
    assert rc == 0
    import json
    payload = json.loads(capsys.readouterr().out)
    assert "snapshot_date" in payload
    assert payload["diff"] == []
