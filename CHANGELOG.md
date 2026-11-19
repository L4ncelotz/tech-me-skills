# Changelog

All notable changes to this project should be documented here.

## [Unreleased]

### Added

- `evals/short_prompt_baseline.md`: concise 1-paragraph architecture-advisor prompt enabling 3-way evaluation (`baseline` vs `short-prompt` vs `tech-me`) across all 21 scenarios in `scripts/run_evals.py` (with SHA-256 tracking) and `evals/RUBRIC.md`.
- `user_simulator` schema (`persona`, `known_facts`, `unknowns`, `stop_rule`) on multi-turn scenarios in `evals/scenarios.json`, validated by `scripts/validate_repo.py` and rendered into a deterministic `simulator_system_prompt` by `scripts/run_evals.py`.
- `--blind` / `--blind-seed` mode in `scripts/run_evals.py --prepare-fixtures` to anonymize condition labels (`A`/`B`/`C`) and write the reveal mapping to a separate `.blind-key.json` file.

## [0.3.0] - 2026-11-19

### Added

- Domain Playbooks under `skills/tech-me/references/` (`playbook-database.md`, `playbook-hosting.md`, `playbook-migration.md`), linked from `skills/tech-me/SKILL.md` for on-demand loading without volatile pricing or version numbers.
- `--skill-zip` flag in `scripts/pack_release.py` to build standalone `tech-me-skill-<ver>.zip` archives rooted at `tech-me/` (`SKILL.md`, `references/`, `assets/`, rejecting `README.md` at skill root) for `claude.ai` uploads, covered by 3 unit tests in `tests/test_scripts.py` and documented in `PUBLISHING.md` and `README.md`.
- Real fixture repositories under `evals/fixtures/` (`tight-monolith`, `multi-service-compose`, `small-healthy-app`) with `pack_release.py`-safe secret traps (`env.trap.fixture`), linked to `evals/scenarios.json` (`fixture_dir`, 19 → 21 scenarios) and exported by `scripts/run_evals.py`.
- `fixture_dir` structural checks in `scripts/validate_repo.py` and `tests/test_validator.py` (47 unit tests total).

### Changed

- `skills/tech-me/SKILL.md`: sharpened `review` and `migrate` fast inspect order to list non-ignored paths first and explicitly exclude secret/env patterns (`.env*`, `env.*`, `*secret*`, `*credential*`) based on read-only dogfooding against the new fixture repos.
- `evals/RESULTS.md`: updated scenario coverage line to `3 of 21 fixture scenarios` (with historical note).

### Limitations

- `.claude-plugin/` has not yet been verified with `claude plugin validate .` or a live Claude Code marketplace install (Phase 1.3).
- Dogfooding was performed via an isolated read-only subagent against `evals/fixtures/tight-monolith`, `evals/fixtures/small-healthy-app`, `quick`, and `help` modes; formal `n >= 3` multi-agent blind scoring against all 21 scenarios remains in Phase 2 (`v0.4.0`).

## [0.2.0] - 2026-11-18

### Added

- Invocation modes in `skills/tech-me/SKILL.md`: `/tech-me <topic>` (default adaptive interview), `quick` (no questions, labeled assumptions), `review` (read-only, manifests and configs first), `migrate` (transition cost and rollback), `adr` (draft a decision record), and `help` / bare `/tech-me` (mode cheat-sheet). Handles both inline arguments and `ARGUMENTS:` expansion (e.g., `teveus` and Claude Code), and works as natural language in agents without slash commands.
- Anti-rationalization guard table in `skills/tech-me/SKILL.md` to prevent common adherence drift (question bundling, familiarity bias, unmeasured figures, uninspected repository claims).
- Standalone slash-command wrappers in `commands/` (`tech-me-quick.md`, `tech-me-review.md`, `tech-me-migrate.md`, `tech-me-adr.md`) with `argument-hint` frontmatter and self-contained mode guardrails for Claude Code plugins and `teveus`.
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` for Claude Code plugin installs.
- `evals/scenarios.json`: 5 mode fixtures (`mode-quick-no-questions`, `mode-review-fast-inspect`, `mode-migrate-sqlite-postgres`, `mode-adr-from-decision`, `mode-help-menu`), bringing total scenarios to 19.
- `scripts/validate_repo.py` and `tests/test_validator.py`: validation for `commands/tech-me-*.md` wrappers, optional `mode` field, required non-default mode fixture coverage, and Claude plugin manifest alignment (`name` vs skill, `version` vs latest released CHANGELOG entry, marketplace `source`).
- README workflow Mermaid diagram, mode cheat-sheet, verification step (`/tech-me help`), deduplication notice, and plugin/teveus command usage notes.

### Changed

- SKILL.md `description` now names the modes and the review/migration use cases; `review` mode also inspects `ARCHITECTURE.md` and `docs/adr/` when present.
- `evals/RESULTS.md`: updated scenario coverage line to `3 of 19 fixture scenarios` (with historical note) to stay in sync with `evals/scenarios.json`.

### Limitations

- The 5 new mode fixtures have not been evaluated against a model yet. `mode-review-fast-inspect` is a text-only prompt simulating a repo until Phase 1.1 adds real fixture repos; it cannot test tool-level `.env` avoidance yet. The `review` inspect order comes from one tester's informal report (faster, fewer tokens) and has not been measured. `.claude-plugin/` has not yet been tested with `claude plugin validate`.

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
