#!/usr/bin/env python3
"""Reference implementation of the shiftgear task classifier.

This mirrors the ordered rules in SKILL.md and references/decision-table.md:
it looks at a task description and returns one of the task categories from
the decision table, using keyword and phrase matching. It exists so the
benchmark in bench/results.md can be reproduced by a third party, and so
the labeling rubric is checked into the repository instead of living only
in a person's head.

This is intentionally a simple heuristic, not a model. The skill itself
expects the agent reading SKILL.md to classify tasks using judgment; this
script is a cheap, deterministic stand-in used to measure agreement between
"an explicit rule" and "a human reading the same prompt," on real prompts.

Usage:
    python3 classify.py "refactor the auth module to use the new client"
    echo "some task text" | python3 classify.py -
"""
import re
import sys

# Two tiers of rules, checked in this order:
#   1. STRONG rules: multi-word phrases specific enough that a match almost
#      never happens by accident, even buried in a long prompt. Checked
#      against the FULL text.
#   2. WEAK rules: shorter, more generic keywords that do occur by accident
#      in long prompts (a project brief that mentions "run the tests" or
#      "profile it later" is not, on the whole, a testing or performance
#      task). Checked only against the FRAMING WINDOW: the first part of
#      the prompt, where a person states what they actually want. This is
#      the single biggest lesson from bench/results.md: keyword rules that
#      scan an entire long prompt false-positive constantly; keyword rules
#      that scan only the framing window do much better.
# Keep this list in sync with references/decision-table.md.
FRAMING_WINDOW_CHARS = 500

STRONG_RULES = [
    ("architecture_design", [
        r"\bbuilding a complete open-source project\b",
        r"\bwork directory\b.*\bcreate it\b",
        r"\bnew repo\b", r"\b開新的repo\b",
        r"\bscaffold (the|a new) project\b",
        r"\bdeploy(ed)? (it |this )?(fully |completely )?to (local|production)\b",
    ]),
    ("research_reading", [
        r"\byou are a market (researcher|analyst)\b",
        r"\byou are researching\b",
        r"\bmust use websearch\b", r"\bwebsearch.{0,20}webfetch\b",
        r"\b調研\b", r"\bcite (sources|urls) (and|with) dates?\b",
    ]),
    ("security_review", [
        r"\bsecurity (review|audit)\b", r"\bvulnerabilit", r"\bpenetration test",
        r"\bcve-\d", r"\b(find|scan for) exploits?\b",
    ]),
    ("migration", [
        r"\bmigrat(e|ion) (all|every|the)\b", r"\bmodel deprecat",
        r"\bretir(e|ing|ed|ement)\b.{0,20}\b(model|endpoint|api)\b",
        r"\brename .* across (the|every) (repo|codebase)\b",
    ]),
    ("specs_interviews", [
        r"\bevery day.{0,20}(different|vary|same)\b",
        r"\bquestion (bank|variety)\b",
        r"\b面試题目\b", r"\b不一樣主題\b",
        r"\bwrite (a |the )?spec(ification)?\b",
    ]),
    ("repetitive_transforms", [
        r"\brename all\b", r"\bacross (hundreds|every) (of )?files\b",
        r"\bbulk (edit|rename|transform)\b",
    ]),
]

WEAK_RULES = [
    ("hard_debugging", [
        r"\bdebug", r"\broot cause\b", r"\bcrash(es|ing)?\b", r"\bstack trace\b",
        r"\bnot work(ing)?\b", r"\b壞掉\b", r"\b錯誤\b",
    ]),
    ("code_review", [
        r"\bcode review\b", r"\breview (this|my|the) (diff|pr|code|pull request)\b",
    ]),
    ("performance_work", [
        r"\bprofil(e|ing)\b", r"\boptimi[sz]e\b", r"\blatency\b", r"\bspeed up\b",
        r"\btoo slow\b",
    ]),
    ("writing_tests", [
        r"\bwrite (unit |integration )?tests?\b", r"\badd tests\b",
    ]),
    ("data_analysis", [
        r"\banaly[sz]e (this )?data\b", r"\bspreadsheet\b", r"\bpivot table\b",
    ]),
    ("ui_work", [
        r"\bfrontend\b", r"\bdesign the (page|ui)\b",
    ]),
    ("documentation", [
        r"\bwrite (the )?docs?\b", r"\breadme\b",
    ]),
    ("boilerplate_scaffolding", [
        r"\bboilerplate\b", r"\bstarter (project|template)\b", r"\bproject skeleton\b",
    ]),
    ("trivial_edit", [
        r"\btypo\b", r"\bone.line (change|fix)\b", r"\bsmall edit\b",
        r"\bcreate [a-z]\.txt\b", r"\bgit config\b", r"\bgh auth\b",
    ]),
    ("long_agentic_run", [
        r"\bunattended\b", r"\bovernight\b", r"\brun for hours\b",
        r"\bbackground (agent|task)\b",
    ]),
]

def _compile(rules):
    return [(cat, [re.compile(p, re.IGNORECASE) for p in pats]) for cat, pats in rules]


STRONG_COMPILED = _compile(STRONG_RULES)
WEAK_COMPILED = _compile(WEAK_RULES)


def classify(text: str) -> str:
    """Return the best-matching category, or 'other' if nothing matches.

    'other' covers short questions, status checks, and clarifications that
    are not themselves a coding task, for example "can you see my repo"
    or "what do I need to give you." Those never reach the routing table:
    shiftgear only routes actual work.
    """
    for category, patterns in STRONG_COMPILED:
        for pat in patterns:
            if pat.search(text):
                return category
    window = text[:FRAMING_WINDOW_CHARS]
    for category, patterns in WEAK_COMPILED:
        for pat in patterns:
            if pat.search(window):
                return category
    return "other"


def main():
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        text = " ".join(sys.argv[1:])
    else:
        text = sys.stdin.read()
    print(classify(text))


if __name__ == "__main__":
    main()
