"""Deterministic unit tests for local file and scenario validator."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_repo import ROOT, SUMMARY_HEADING, validate_repo, validate_results_claims, validate_scenarios, validate_skill  # noqa: E402


class ValidationTests(unittest.TestCase):
    def test_real_repo_passes(self):
        self.assertEqual(validate_repo(ROOT), [])

    def test_rejects_results_coverage_total_drift(self):
        fixture = json.loads((ROOT / "evals/scenarios.json").read_text(encoding="utf-8"))
        ids = {s["id"] for s in fixture["scenarios"]}
        with tempfile.TemporaryDirectory() as directory:
            results = Path(directory) / "RESULTS.md"
            results.write_text(
                "- **Scenario coverage:** 3 of 99 fixture scenarios; only some categories exercised.\n\n"
                f"{SUMMARY_HEADING}\n\n| Scenario ID |\n| :--- |\n| `unknown-scale-defaults` |\n\n---\n",
                encoding="utf-8",
            )
            errors = validate_results_claims(results, ids)
            self.assertTrue(any("99 fixture scenarios" in err for err in errors))

    def test_rejects_results_sampled_count_mismatch(self):
        fixture = json.loads((ROOT / "evals/scenarios.json").read_text(encoding="utf-8"))
        ids = {s["id"] for s in fixture["scenarios"]}
        with tempfile.TemporaryDirectory() as directory:
            results = Path(directory) / "RESULTS.md"
            results.write_text(
                "- **Scenario coverage:** 3 of "
                f"{len(ids)} fixture scenarios; only some categories exercised.\n\n"
                f"{SUMMARY_HEADING}\n\n| Scenario ID |\n| :--- |\n| `unknown-scale-defaults` |\n\n---\n",
                encoding="utf-8",
            )
            errors = validate_results_claims(results, ids)
            self.assertTrue(any("references 1 known scenario ID" in err for err in errors))

    def test_accepts_results_claims_of_real_files(self):
        with tempfile.TemporaryDirectory() as directory:
            results = (ROOT / "evals/RESULTS.md").read_text(encoding="utf-8")
            copy = Path(directory) / "RESULTS.md"
            copy.write_text(results, encoding="utf-8")
            fixture = json.loads((ROOT / "evals/scenarios.json").read_text(encoding="utf-8"))
            ids = {s["id"] for s in fixture["scenarios"]}
            self.assertEqual(validate_results_claims(copy, ids), [])

    def test_rejects_missing_coverage_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            results = Path(directory) / "RESULTS.md"
            results.write_text("# Report without the claim\n", encoding="utf-8")
            errors = validate_results_claims(results, {"a-scenario"})
            self.assertTrue(any("N of M fixture scenarios" in err for err in errors))

    def test_rejects_wrong_skill_directory_name(self):
        with tempfile.TemporaryDirectory() as directory:
            wrong = Path(directory) / "other-skill"
            wrong.mkdir()
            (wrong / "SKILL.md").write_text(
                "---\nname: tech-me\ndescription: Example\n---\n# Example\n", encoding="utf-8"
            )
            self.assertTrue(any("must match directory" in err for err in validate_skill(wrong)))

    def test_rejects_missing_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "tech-me"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: tech-me\ndescription: Example\n---\nSee [missing](references/nope.md).\n",
                encoding="utf-8",
            )
            self.assertTrue(any("link not found" in err for err in validate_skill(skill)))

    def test_rejects_duplicate_scenario_ids(self):
        fixture = json.loads((ROOT / "evals/scenarios.json").read_text(encoding="utf-8"))
        duplicate = dict(fixture["scenarios"][0])
        fixture["scenarios"].append(duplicate)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scenarios.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            self.assertTrue(any("Duplicate scenario id" in err for err in validate_scenarios(path)))

    def test_rejects_missing_categories(self):
        fixture = json.loads((ROOT / "evals/scenarios.json").read_text(encoding="utf-8"))
        fixture["scenarios"] = fixture["scenarios"][:1]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scenarios.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            self.assertTrue(any("Missing evaluation categories" in err for err in validate_scenarios(path)))

    def test_rejects_unsupported_frontmatter(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "tech-me"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: tech-me\ndescription: Example\nmagic: true\n---\n# Instructions\n",
                encoding="utf-8",
            )
            self.assertTrue(any("Unsupported frontmatter" in err for err in validate_skill(skill)))

    def test_accepts_scripted_turns(self):
        fixture = json.loads((ROOT / "evals/scenarios.json").read_text(encoding="utf-8"))
        multi_turn = [s for s in fixture["scenarios"] if s.get("turns")]
        self.assertTrue(multi_turn, "The scenario set must include at least one multi-turn (turns) fixture.")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scenarios.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            self.assertEqual(validate_scenarios(path), [])

    def test_rejects_malformed_scripted_turns(self):
        fixture = json.loads((ROOT / "evals/scenarios.json").read_text(encoding="utf-8"))
        fixture["scenarios"][0]["turns"] = "recommend now"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scenarios.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            self.assertTrue(
                any("turns must be a non-empty list of strings" in err for err in validate_scenarios(path))
            )


if __name__ == "__main__":
    unittest.main()
