#!/usr/bin/env python3
"""Standard-library evaluation harness for Tech-Me.

Inspects and formats evaluation scenarios for baseline vs. skill comparisons.
Distinguishes offline fixture preparation from live model evaluations to
prevent reporting unexecuted evaluations or synthetic benchmark results.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCENARIOS_PATH = ROOT / "evals" / "scenarios.json"
DEFAULT_SKILL_PATH = ROOT / "skills" / "tech-me" / "SKILL.md"
DEFAULT_MODEL = "google-antigravity/gemini-3.8-flash"
BASELINE_SYSTEM_PROMPT = "You are a helpful AI assistant."


def load_scenarios(scenarios_path: Path) -> dict:
    if not scenarios_path.is_file():
        raise FileNotFoundError(f"Scenarios file not found: {scenarios_path}")
    with scenarios_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_skill_prompt(skill_path: Path) -> tuple[str, str]:
    if not skill_path.is_file():
        raise FileNotFoundError(f"Skill file not found: {skill_path}")
    content = skill_path.read_text(encoding="utf-8")
    sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return content, sha256


def filter_scenarios(all_scenarios: list[dict], requested_ids: list[str]) -> list[dict]:
    known_by_id = {s["id"]: s for s in all_scenarios}
    if not requested_ids or "all" in requested_ids:
        return all_scenarios

    missing = [req for req in requested_ids if req not in known_by_id]
    if missing:
        raise ValueError(
            f"Unknown scenario ID(s): {', '.join(missing)}. "
            f"Available: {', '.join(sorted(known_by_id.keys()))}"
        )
    return [known_by_id[req] for req in requested_ids]


def build_evaluation_payload(
    scenario: dict,
    skill_content: str,
    model: str,
) -> dict:
    user_prompt = scenario["user_prompt"]
    context = scenario.get("context", "")

    return {
        "scenario_id": scenario["id"],
        "category": scenario.get("category", "unknown"),
        "fixture_dir": scenario.get("fixture_dir"),
        "predetermined_followups": scenario.get("turns", []),
        "baseline_prompt": {
            "system_prompt": BASELINE_SYSTEM_PROMPT,
            "user_prompt": user_prompt,
            "context": context,
        },
        "skill_prompt": {
            "system_prompt": skill_content,
            "user_prompt": user_prompt,
            "context": context,
        },
        "target_model": model,
        "expected_behaviors": scenario.get("expected_behaviors", []),
        "failure_signals": scenario.get("failure_signals", []),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Tech-Me Evaluation Harness")
    parser.add_argument(
        "--scenarios",
        "-s",
        nargs="+",
        default=["all"],
        help="Scenario IDs to inspect (comma-separated or multiple flags), or 'all'",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available scenario IDs and exit",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Format prompt payloads and print to stdout without invoking model APIs",
    )
    parser.add_argument(
        "--prepare-fixtures",
        action="store_true",
        help="Export formatted scenario payloads for downstream LLM evaluation runners",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Path to write prepared evaluation fixtures JSON",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Target model identifier for prompts (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--scenarios-file",
        type=Path,
        default=DEFAULT_SCENARIOS_PATH,
        help="Custom scenarios JSON path",
    )
    parser.add_argument(
        "--skill-file",
        type=Path,
        default=DEFAULT_SKILL_PATH,
        help="Custom SKILL.md path",
    )

    args = parser.parse_args()

    # Flatten any comma-separated entries in --scenarios
    requested_scenarios: list[str] = []
    for item in args.scenarios:
        for sub in item.split(","):
            sub = sub.strip()
            if sub:
                requested_scenarios.append(sub)

    try:
        data = load_scenarios(args.scenarios_file)
        all_scenarios = data.get("scenarios", [])

        if args.list:
            print(f"Available scenarios ({len(all_scenarios)} total):")
            for sc in all_scenarios:
                print(f"  - {sc['id']:<35} [{sc.get('category', 'none')}]")
            return 0

        selected = filter_scenarios(all_scenarios, requested_scenarios)
        skill_content, skill_sha256 = load_skill_prompt(args.skill_file)

    except Exception as e:
        print(f"Error initializing evaluation harness: {e}", file=sys.stderr)
        return 1

    # Check execution mode: fail closed when run without --dry-run or --prepare-fixtures
    if not args.dry_run and not args.prepare_fixtures:
        print(
            "Error: Live evaluation runner is not configured in this environment.\n"
            "Tech-Me evaluation fixtures require an active LLM evaluation harness to run.\n"
            "  - To inspect scenario prompt payloads: python scripts/run_evals.py --dry-run\n"
            "  - To export payloads for an external runner: python scripts/run_evals.py --prepare-fixtures --output <path>",
            file=sys.stderr,
        )
        return 2

    run_timestamp = datetime.now(timezone.utc).isoformat()
    rel_skill_source = (
        str(args.skill_file.relative_to(ROOT))
        if args.skill_file.is_relative_to(ROOT)
        else str(args.skill_file)
    )

    if args.dry_run:
        print(f"Tech-Me Evaluation Harness | Target Model: {args.model}")
        print(f"Scenarios selected ({len(selected)}): {', '.join(sc['id'] for sc in selected)}")
        print(f"Skill SHA-256: {skill_sha256}")
        print("-" * 60)

        for sc in selected:
            print(f"\n[DRY RUN] Scenario: {sc['id']} (Category: {sc.get('category')})")
            print(f"  Prompt: {sc['user_prompt']}")
            print(f"  Context: {sc.get('context', 'None')}")
            if sc.get("fixture_dir"):
                print(f"  Fixture dir: {sc['fixture_dir']}")
            print(f"  Expected behaviors: {len(sc.get('expected_behaviors', []))} rules")
            print(f"  Failure signals: {len(sc.get('failure_signals', []))} rules")
            print(f"  Scripted follow-up turns: {len(sc.get('turns', []))}")

        print("\nDry-run completed. (No LLM API invoked; no evaluation performed).")
        return 0

    if args.prepare_fixtures:
        fixtures_payload = {
            "type": "prepared_fixtures",
            "status": "not_evaluated",
            "generator": "scripts/run_evals.py",
            "timestamp": run_timestamp,
            "target_model": args.model,
            "skill_system_prompt_source": rel_skill_source,
            "skill_system_prompt_sha256": skill_sha256,
            "scenarios_count": len(selected),
            "fixtures": {},
        }

        for sc in selected:
            payload = build_evaluation_payload(sc, skill_content, args.model)
            fixtures_payload["fixtures"][sc["id"]] = payload

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("w", encoding="utf-8") as f:
                json.dump(fixtures_payload, f, indent=2)
            print(f"Prepared fixtures for {len(selected)} scenarios written to: {args.output}")
        else:
            print(f"Prepared fixtures for {len(selected)} scenarios (use --output to save).")

        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
