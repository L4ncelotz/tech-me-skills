# Publishing and Release Guide

This document covers the release, packaging, and distribution workflow for Tech-Me.

## Canonical Repository Status

The canonical upstream repository is live at:
**`https://github.com/L4ncelotz/tech-me-skills`**

Do not run initial `git init` or destructive force-pushes against this repository. Use standard Git feature-branch and tagging workflows.

---

## Release & Tagging Workflow (Maintainers)

Follow these steps when cutting a new version release:

### 1. Pre-release Verification
Run all local validation and evaluation checks:
```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python scripts/run_evals.py --dry-run
```
Ensure `CHANGELOG.md` reflects all changes and version bumps.

### 2. Commit and Tag
Ensure the working tree is completely clean, then create and push an annotated Git tag with semantic versioning:
```bash
# Example for v0.1.1
git tag -a v0.1.1 -m "Release v0.1.1"
git push origin main
git push origin v0.1.1
```

### 3. Build Clean Distribution Package
Before creating the GitHub release, package the release archive. Release packaging requires a clean, committed Git working tree, verifies that `--version` matches an annotated Git tag (`v<version>`) pointing at the packaged ref, and extracts exclusively from the committed Git tree (`git archive`):

Fail closed cases: missing tag, non-annotated tag objects (a lightweight tag points directly at a commit), a branch sharing the tag name, tag/ref commit mismatch, uncommitted changes, or leaked artifacts. Use `--allow-untagged` only for throwaway local archives; never publish one.
```bash
# Automated packaging with integrity assertions
python scripts/pack_release.py --version 0.1.1
```
This creates `dist/tech-me-0.1.1.zip` containing only committed files and asserts zero leakage of `.git/`, `__pycache__`, `.pytest_cache`, `.venv`, `.env*`, or temporary files.

Do not package releases with a hand-rolled `git archive` command. `pack_release.py` is the single supported release path: a manual `git archive` skips the version/tag/commit verification and the forbidden-artifact scan, so an archive built that way must never be distributed.

### 4. Create GitHub Release
Release notes must cover only the released version's own section, not the entire `CHANGELOG.md` history. Extract that section with the stdlib-only helper, which reads and writes text with explicit UTF-8 and fails closed if the generated file would contain a BOM or NUL byte (a PowerShell `>` redirection silently writes UTF-16 and produced unreadable release notes in real releases):

```bash
# Example for v0.1.1; substitute the version you are releasing.
python scripts/make_release_notes.py --version 0.1.1
# -> dist/release-notes-0.1.1.md
```

The same command behaves identically in PowerShell and Git Bash because the script writes the file itself — do **not** redirect its output with `>`. It extracts with the literal version string (no regex metacharacter interpretation), stops at the next `## ` heading, and refuses to write when the section is missing, does not start with a `### ` heading, contains a stray `## ` heading, or would contain a BOM/NUL byte. Unit tests in `tests/test_scripts.py` cover the extraction and the BOM/NUL checks. `dist/` is git-ignored, so writing the notes file does not dirty the working tree for `pack_release.py`.

Before uploading, sanity-check the notes (`head -n 3` / `tail -n 3`): the file should skip the leading blank lines and start at the first `### ` heading, and end at the Limitations entries.

Then create the release. The title and flags intentionally mark this as a GitHub **pre-release**, matching the Limitations section of the notes (cross-agent behavior and comparative quality are not yet verified):

```bash
gh release create v0.1.1 dist/tech-me-0.1.1.zip \
  --prerelease \
  --title "v0.1.1 - Post-release Fixes" \
  --notes-file dist/release-notes-0.1.1.md
```

---
## Downstream Forking & Mirroring

If you are maintaining a private fork or mirror under another GitHub account:
1. Fork `L4ncelotz/tech-me-skills` via the GitHub UI or `gh repo fork L4ncelotz/tech-me-skills`.
2. Configure your downstream remote:
   ```bash
   git remote add downstream https://github.com/<your-user>/tech-me-skills.git
   git push -u downstream main
   ```
3. Never overwrite or force-push to upstream `origin`.

---

## Clean Installation Verification

After publishing a tag or release, verify that agent runtimes can install and consume the skill cleanly:

```bash
npx skills add L4ncelotz/tech-me-skills --skill tech-me
```

Confirm your agent runtime reads the skill when presented with an architecture decision request, and that it does not falsely activate for routine bug fixes or syntax questions.
