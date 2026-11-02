#!/usr/bin/env python3
"""Dependency-free, deliberately limited structural checks for Tech-Me.

This does not replace the upstream `skills-ref` validator or evaluate LLM behavior.
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "tech-me"
SCENARIOS_PATH = "evals/scenarios.json"
RESULTS_PATH = "evals/RESULTS.md"
CATEGORIES = {
    "discovery", "stopping", "bias", "unknowns", "feasibility", "existing-project",
    "overengineering", "evolution", "evidence", "risk", "communication",
    "permissions", "activation",
}
ALLOWED_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LOCAL_LINK_RE = re.compile(r"\]\(([^)]+)\)")
SUMMARY_HEADING = "### Aggregate Score Summary"
COVERAGE_CLAIM_RE = re.compile(r"\*\*Scenario coverage:\*\*\s+(\d+)\s+of\s+(\d+)\s+fixture scenarios")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")


def parse_simple_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    """Validate our own flat, scalar-only frontmatter; not a general YAML parser."""
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["SKILL.md must begin with YAML frontmatter (---)."]
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, ["SKILL.md frontmatter has no closing --- delimiter."]
    raw = text[4:end]
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) or ":" not in line:
            errors.append(f"Unexpected frontmatter syntax: {line[:80]}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key in fields:
            errors.append(f"Duplicate frontmatter field: {key}")
        if key not in ALLOWED_FIELDS:
            errors.append(f"Unsupported frontmatter field: {key}")
        fields[key] = value
    return fields, errors


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"Missing {skill_file}"]
    text = skill_file.read_text(encoding="utf-8")
    fields, errors = parse_simple_frontmatter(text)
    for key in ("name", "description"):
        if not fields.get(key):
            errors.append(f"Required field {key} is empty or missing.")
    name = fields.get("name", "")
    if not SLUG_RE.fullmatch(name) or len(name) > 64:
        errors.append("name must be a lowercase hyphenated slug of at most 64 characters.")
    if name != skill_dir.name:
        errors.append(f"name {name!r} must match directory {skill_dir.name!r}.")
    if len(fields.get("description", "")) > 1024:
        errors.append("description exceeds 1024 characters.")
    if len(fields.get("compatibility", "")) > 500:
        errors.append("compatibility exceeds 500 characters.")
    if not text.split("\n---\n", 1)[-1].strip():
        errors.append("Skill instructions are missing.")
    if len(text.splitlines()) > 500:
        errors.append("SKILL.md exceeds the recommended 500-line readability limit.")
    for target in LOCAL_LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        dest = (skill_dir / target.split("#", 1)[0]).resolve()
        if not dest.is_relative_to(skill_dir.resolve()):
            errors.append(f"SKILL.md link escapes skill directory: {target}")
        elif not dest.is_file():
            errors.append(f"SKILL.md link not found: {target}")
    return errors


def validate_scenarios(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"Missing evaluation scenarios: {path}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeError) as exc:
        return [f"Invalid scenarios JSON: {exc}"]
    if data.get("schema_version") != 1:
        errors.append("Expected eval schema_version 1.")
    scenarios = data.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        return errors + ["scenarios must be a non-empty list."]
    ids = set()
    seen_categories = set()
    required = ("id", "category", "user_prompt", "context", "expected_behaviors", "failure_signals")
    for idx, item in enumerate(scenarios, 1):
        label = f"scenarios[{idx}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object.")
            continue
        for field in required:
            if field not in item:
                errors.append(f"{label} missing {field}.")
        ident = item.get("id")
        if not isinstance(ident, str) or not SLUG_RE.fullmatch(ident):
            errors.append(f"{label} has invalid id.")
        elif ident in ids:
            errors.append(f"Duplicate scenario id: {ident}")
        ids.add(ident)
        cat = item.get("category")
        if cat not in CATEGORIES:
            errors.append(f"{label} has invalid category: {cat!r}")
        else:
            seen_categories.add(cat)
        for field in ("user_prompt", "context"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"{label} {field} must be a nonempty string.")
        for field in ("expected_behaviors", "failure_signals"):
            value = item.get(field)
            if not isinstance(value, list) or not value or any(not isinstance(v, str) or not v.strip() for v in value):
                errors.append(f"{label} {field} must be a non-empty list of strings.")
        if "turns" in item:
            turns = item["turns"]
            if not isinstance(turns, list) or not turns or any(not isinstance(t, str) or not t.strip() for t in turns):
                errors.append(f"{label} turns must be a non-empty list of strings when present.")
    missing = CATEGORIES - seen_categories
    if missing:
        errors.append(f"Missing evaluation categories: {', '.join(sorted(missing))}")
    return errors


def validate_results_claims(results_path: Path, scenario_ids: set[str]) -> list[str]:
    """Keep the RESULTS.md scenario-coverage claim in sync with scenarios.json."""
    errors: list[str] = []
    if not results_path.is_file():
        return [f"Missing evaluation results: {results_path}"]
    text = results_path.read_text(encoding="utf-8")
    match = COVERAGE_CLAIM_RE.search(text)
    if match is None:
        return [
            "RESULTS.md must state scenario coverage as '**Scenario coverage:** "
            "N of M fixture scenarios'."
        ]
    sampled, claimed_total = (int(part) for part in match.groups())
    if claimed_total != len(scenario_ids):
        errors.append(
            f"RESULTS.md claims {claimed_total} fixture scenarios, but "
            f"{SCENARIOS_PATH} defines {len(scenario_ids)}."
        )
    fragment = text.split(SUMMARY_HEADING, 1)
    if len(fragment) == 1:
        errors.append(f"RESULTS.md is missing a '{SUMMARY_HEADING}' table.")
        return errors
    summary = fragment[1].split("\n---", 1)[0]
    referenced = {token for token in BACKTICK_RE.findall(summary) if token in scenario_ids}
    if len(referenced) != sampled:
        errors.append(
            f"RESULTS.md claims {sampled} sampled scenarios, but its summary table "
            f"references {len(referenced)} known scenario ID(s)."
        )
    return errors


def validate_repo(root: Path) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_skill(root / "skills" / SKILL_NAME))
    scenarios_file = root / SCENARIOS_PATH
    scenario_errors = validate_scenarios(scenarios_file)
    errors.extend(scenario_errors)
    if not scenario_errors:
        data = json.loads(scenarios_file.read_text(encoding="utf-8"))
        ids = {
            item["id"]
            for item in data.get("scenarios", [])
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
        errors.extend(validate_results_claims(root / RESULTS_PATH, ids))
    for filename in (
        "README.md", "LICENSE", "CONTRIBUTING.md", "CHANGELOG.md", RESULTS_PATH,
        "evals/RUBRIC.md", "evals/RUNBOOK.md"
    ):
        if not (root / filename).is_file():
            errors.append(f"Missing repository document: {filename}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root to validate")
    args = parser.parse_args()
    errors = validate_repo(args.root.resolve())
    if errors:
        print(f"FAIL: {len(errors)} structural issue(s):")
        for issue in errors:
            print(" -", issue)
        return 1
    data = json.loads((args.root / "evals" / "scenarios.json").read_text(encoding="utf-8"))
    print(f"PASS: structural validation, {len(data['scenarios'])} evaluation scenarios, {len(CATEGORIES)} categories")
    print("Note: no model behavior or cross-agent compatibility was tested.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
