"""Validate SKILL.md frontmatter against the Agent Skills specification
(agentskills.io/specification, fetched 2026-09-30): name and description
constraints, plus the additional reserved-word and XML-tag rules from
Anthropic's skill best-practices page. No PyYAML dependency: the
frontmatter here is flat enough that a small hand-rolled parser is less
risk than adding a dependency for one test file.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD = REPO_ROOT / "SKILL.md"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESERVED_WORDS = {"anthropic", "claude"}


def read_frontmatter() -> str:
    text = SKILL_MD.read_text()
    assert text.startswith("---\n"), "SKILL.md must start with a YAML frontmatter block"
    parts = text.split("---\n", 2)
    assert len(parts) >= 3, "SKILL.md frontmatter block is not closed with '---'"
    return parts[1]


def get_field(frontmatter: str, field: str) -> str:
    """Grab a single top-level scalar field's raw value (one line)."""
    m = re.search(rf"^{field}:\s*(.*)$", frontmatter, re.MULTILINE)
    assert m, f"frontmatter is missing required field '{field}'"
    return m.group(1).strip()


def test_frontmatter_block_exists_and_is_closed():
    fm = read_frontmatter()
    assert fm.strip(), "frontmatter block is empty"


def test_name_field_present_and_valid():
    fm = read_frontmatter()
    name = get_field(fm, "name")
    assert 1 <= len(name) <= 64, "name must be 1-64 characters"
    assert NAME_RE.match(name), (
        "name must be lowercase letters, digits, and hyphens, "
        "no leading/trailing/double hyphen"
    )
    assert "--" not in name, "name must not contain consecutive hyphens"
    assert not name.startswith("-") and not name.endswith("-")
    assert "<" not in name and ">" not in name, "name must not contain XML tags"
    for word in RESERVED_WORDS:
        assert word not in name, f"name must not contain the reserved word '{word}'"


def test_name_matches_parent_directory():
    fm = read_frontmatter()
    name = get_field(fm, "name")
    assert name == REPO_ROOT.name, "name field must match the skill's directory name"


def test_description_field_present_and_within_limits():
    fm = read_frontmatter()
    desc = get_field(fm, "description")
    assert 1 <= len(desc) <= 1024, f"description must be 1-1024 characters, got {len(desc)}"
    assert "<" not in desc and ">" not in desc, "description must not contain XML tags"


def test_description_written_in_third_person():
    fm = read_frontmatter()
    desc = get_field(fm, "description").lower()
    # Best-practices guidance: avoid first- and second-person framing like
    # "I can help you" or "you can use this," which hurts skill discovery.
    for bad_start in ("i can", "i help", "you can use", "you can", "this skill helps you"):
        assert not desc.startswith(bad_start), (
            f"description should not open in first/second person ('{bad_start}')"
        )


def test_description_states_what_and_when():
    fm = read_frontmatter()
    desc = get_field(fm, "description").lower()
    assert "use" in desc or "trigger" in desc, (
        "description should say when to use the skill, not just what it does"
    )


def test_license_field_present():
    fm = read_frontmatter()
    license_value = get_field(fm, "license")
    assert license_value, "license field should not be empty"


def test_metadata_version_present():
    fm = read_frontmatter()
    assert re.search(r"^metadata:\s*$", fm, re.MULTILINE), "expected a metadata: block"
    assert re.search(r'^\s+version:\s*"?[\w.\-]+"?', fm, re.MULTILINE), "expected metadata.version"


def test_compatibility_field_within_limit_if_present():
    fm = read_frontmatter()
    m = re.search(r"^compatibility:\s*(.*)$", fm, re.MULTILINE)
    if m:
        value = m.group(1).strip()
        assert 1 <= len(value) <= 500, "compatibility must be 1-500 characters"


def test_skill_md_body_under_300_lines():
    text = SKILL_MD.read_text()
    lines = text.splitlines()
    assert len(lines) <= 300, f"SKILL.md is {len(lines)} lines, brief requires under 300"


def test_referenced_files_exist():
    text = SKILL_MD.read_text()
    for rel in re.findall(r"references/[\w.\-]+\.md", text):
        assert (REPO_ROOT / rel).exists(), f"SKILL.md references {rel}, which does not exist"
    for rel in re.findall(r"assets/[\w.\-]+\.csv", text):
        assert (REPO_ROOT / rel).exists(), f"SKILL.md references {rel}, which does not exist"
    for rel in re.findall(r"scripts/[\w.\-]+\.(?:py|sh)", text):
        assert (REPO_ROOT / rel).exists(), f"SKILL.md references {rel}, which does not exist"
