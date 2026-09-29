import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "bench"))
from classify import classify


def test_architecture_brief_detected():
    text = ("You are building a complete open-source project called foo. "
            "Work directory: /tmp/foo (create it).")
    assert classify(text) == "architecture_design"


def test_market_research_detected():
    text = ("You are a market researcher for open-source software. "
            "You MUST use WebSearch and WebFetch heavily.")
    assert classify(text) == "research_reading"


def test_security_review_detected():
    text = "Run a security review of the auth module and check for vulnerabilities before we ship."
    assert classify(text) == "security_review"


def test_debugging_detected_in_framing_window():
    text = "Please debug why the login page crashes on submit."
    assert classify(text) == "hard_debugging"


def test_weak_keyword_deep_in_long_prompt_does_not_misfire():
    # "tests" appears deep in a long architecture-style brief; the strong
    # architecture_design rule should win because it is checked first and
    # matches against the full text, while the weak writing_tests rule is
    # restricted to the framing window and should not see it.
    filler = "word " * 200
    text = (
        "You are building a complete open-source project called demo. "
        "Work directory: /tmp/demo (create it). " + filler +
        "Also make sure tests actually run and pass before you finish."
    )
    assert classify(text) == "architecture_design"


def test_short_question_falls_back_to_other():
    assert classify("can you see my repo") == "other"


def test_empty_string_falls_back_to_other():
    assert classify("") == "other"
