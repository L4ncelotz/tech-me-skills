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
# Example for v0.1.0
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin main
git push origin v0.1.0
```

### 3. Build Clean Distribution Package
Before creating the GitHub release, package the release archive. Release packaging requires a clean, committed Git working tree, verifies that `--version` matches an annotated Git tag (`v<version>`) pointing at the packaged ref, and extracts exclusively from the committed Git tree (`git archive`):

Fail closed cases: missing tag, non-annotated tag objects (a lightweight tag points directly at a commit), a branch sharing the tag name, tag/ref commit mismatch, uncommitted changes, or leaked artifacts. Use `--allow-untagged` only for throwaway local archives; never publish one.
```bash
# Automated packaging with integrity assertions
python scripts/pack_release.py --version 0.1.0
```
This creates `dist/tech-me-0.1.0.zip` containing only committed files and asserts zero leakage of `.git/`, `__pycache__`, `.pytest_cache`, `.venv`, `.env*`, or temporary files.

Do not package releases with a hand-rolled `git archive` command. `pack_release.py` is the single supported release path: a manual `git archive` skips the version/tag/commit verification and the forbidden-artifact scan, so an archive built that way must never be distributed.

### 4. Create GitHub Release
Release notes must cover only the released version's own section, not the entire `CHANGELOG.md` history. Extract that section with `awk` (use Git Bash on Windows), then create the release. The title and flags intentionally mark this as a GitHub **pre-release**, matching the `0.1.0` Limitations entry in `CHANGELOG.md` (cross-agent behavior and comparative quality are not yet verified):

```bash
mkdir -p dist
awk '/^## \[0\.1\.0\]/{f=1; next} /^## /{f=0} f' CHANGELOG.md > dist/release-notes-0.1.0.md

gh release create v0.1.0 dist/tech-me-0.1.0.zip \
  --prerelease \
  --title "v0.1.0 - Initial Pre-release" \
  --notes-file dist/release-notes-0.1.0.md
```

Before uploading, sanity-check the notes: the file should start with a blank line followed by `### Added`, end with the Limitations entries, and contain no `## ` headings (`head -n 3` / `tail -n 3`). `dist/` is git-ignored, so writing the notes file does not dirty the working tree for `pack_release.py`.

To reuse the extraction for another version, avoid regex metacharacters entirely:
```bash
awk -v v="0.1.1" 'index($0, "## [" v "]") == 1 {f=1; next} /^## /{f=0} f' CHANGELOG.md > dist/release-notes-0.1.1.md
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
