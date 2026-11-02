# Changelog

All notable changes to this project should be documented here.

## [Unreleased]

## [0.1.1] - 2026-11-02

### Added

- `scripts/make_release_notes.py`: stdlib-only extractor that writes a version's release notes with explicit UTF-8 and fails closed on missing sections, malformed `### ` headings, stray `## ` headings, BOM and NUL bytes; covered by unit tests.
- `evals/runs/run_20261102_spotcheck.json`: post-change spot-check record for the v0.1.1 skill edits — full baseline/skill transcripts for `unknown-scale-defaults` and `historical-preference-bias`, per-dimension rubric scores, and an explicit non-comparability statement against the 2026-10-29 report.
- `ROADMAP.md`: project roadmap now tracked in the repository, with Phase 0 progress and decision records.

### Changed

- `scripts/validate_repo.py` now checks that the scenario-coverage claim in `evals/RESULTS.md` matches `evals/scenarios.json` (total count and sampled rows), and requires `evals/RESULTS.md` to exist.
- `skills/tech-me/SKILL.md` and references tightened per v0.1.0 self-review: the one-question rule no longer carries the "combine closely related" exception (`references/discovery.md` spells out one decision per turn); every provisional default must state an observable condition that would reopen it (`references/discovery.md` adds a `Revisit when` field, `references/output.md` adds a `Revisit when:` line); the bias counter-check uses one canonical, cost-held-fixed phrasing shared with `references/evaluation.md`; every unmeasured figure the assistant introduces must be labeled **estimate — not measured** with its basis or replaced by a relative comparison.
- `evals/scenarios.json`: expected behaviors of three fixture scenarios updated to cover the tightened rules ("at most one high-impact question per turn", unbundled unknowns, estimate labeling, per-default revisit conditions); scenario count unchanged (14).
- `evals/RESULTS.md` gains a v0.1.1 spot-check addendum linking to the run record; `README.md` documents `/tech-me` invocation in Claude Code and adds an n = 1 before/after example flagged as not-a-benchmark.

### Fixed

- Release-notes generation in `PUBLISHING.md` no longer relies on shell redirection/`awk`, which under Windows PowerShell could silently write UTF-16 (occurred in the v0.1.0 release); the documented workflow uses `scripts/make_release_notes.py` with no redirection.
- `evals/RESULTS.md` scenario coverage corrected to "3 of 14 fixture scenarios", matching `evals/scenarios.json`, and marked as a historical v0.1.0 run via a top-of-file note.

### Limitations

- The behavioral evidence for the v0.1.1 skill edits is an informal spot-check recorded **before this release** (`evals/runs/run_20261102_spotcheck.json`): one-shot OpenCode subagent runs, n = 1 per condition, non-blind scoring, model `deepseek-v4.1-flash-free`. It is not comparable to `evals/runs/run_20261029_step6.json` (`gemini-3.8-flash`, live harness) — the two score sets must not be read as a trend, and neither validates cross-agent behavior.

## [0.1.0] - 2026-10-29

### Added

- Portable `tech-me` Agent Skill with adaptive requirements discovery and bias-controlled architecture evaluation.
- References for discovery, evidence-based comparison, and decision report structure.
- Optional Architecture Decision Record template.
- Scenario-based evaluation fixtures, human scoring rubric, and comparison runbook.
- Stdlib-only repository validator, tests, and validation CI workflow.

### Fixed

- Documented fixture-preparation command now writes to git-ignored `dist/`, and `.gitignore` covers generated fixture files, so preparing fixtures no longer leaves an untracked file that blocks clean-tree release packaging.
- `run_evals.py` execution-mode check simplified to the plain `--dry-run`/`--prepare-fixtures` condition (dead code removed); behavior unchanged.
- Release packaging (`pack_release.py`) requires an annotated tag (`git tag -a`) in the `refs/tags/` namespace matching `--version`: untagged refs, lightweight tags, a branch sharing the tag name, and tag/ref commit mismatches all fail closed. `--allow-untagged` bypasses tag verification for local archives only (see PUBLISHING.md).
- `PUBLISHING.md` documents `pack_release.py` as the single supported release path and the manual `git archive` alternative (which skipped verification) was removed; the README install section now reflects the published canonical repository.

### Changed

- Updated canonical repository references and installation command to `L4ncelotz/tech-me-skills`.
- `evals/RESULTS.md` findings scoped to the three sampled scenarios (one response per condition) with explicit limitations; no cross-scenario generalization is implied.
- Evaluation fixtures gained an optional `turns` array of scripted user replies for multi-turn interviews, with focus on stopping discipline ("recommend now") and not re-asking answered constraints; validator and harness accept and export them. First multi-turn stopping scenario added.

### Limitations

- Initial draft: cross-agent behavior and comparative quality have **not yet been empirically verified**; this release is tagged as a GitHub **pre-release**.
- No skills.sh listing is implied by this package.
