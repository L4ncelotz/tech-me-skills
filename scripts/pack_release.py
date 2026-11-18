#!/usr/bin/env python3
"""Packaging script to create clean release ZIP archives for Tech-Me.

Packages only committed files from a Git tree (git archive).
Enforces a clean working tree (no uncommitted changes or untracked files),
verifies that --version matches an annotated Git tag (v<version>) pointing at
the packaged ref, and verifies zero leakage of .git/, Python caches, virtual
environments, environment files (.env*), or build artifacts. Standard library only.
"""

import argparse
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]

# Denylist patterns that must NEVER appear in release archives
FORBIDDEN_SUBSTRINGS = [
    ".git/",
    ".git\\",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    ".DS_Store",
    ".env",
    "dist/",
    "dist\\",
    "build/",
    "build\\",
]

FORBIDDEN_EXTENSIONS = [
    ".pyc",
    ".pyo",
    ".pyd",
    ".zip",
    ".tar.gz",
    ".tgz",
    ".tmp",
    ".log",
]


def is_forbidden(rel_path: str) -> bool:
    normalized = rel_path.replace("\\", "/")
    parts = normalized.strip("/").split("/")
    if any(p == ".git" for p in parts):
        return True
    for sub in FORBIDDEN_SUBSTRINGS:
        if sub in normalized:
            return True
    for ext in FORBIDDEN_EXTENSIONS:
        if normalized.endswith(ext):
            return True
    return False


def assert_clean_git_tree(repo_root: Path) -> None:
    """Fail closed if Git metadata is missing or working tree is dirty."""
    if not (repo_root / ".git").exists():
        raise RuntimeError(
            "Git repository or metadata not found. Release packaging requires a valid Git repository."
        )

    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        raise RuntimeError(
            f"Git repository or metadata not found. Release packaging requires a valid Git repository: {e}"
        ) from e

    dirty_entries = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if dirty_entries:
        sample = "\n  ".join(dirty_entries[:5])
        suffix = f"\n  ... and {len(dirty_entries) - 5} more" if len(dirty_entries) > 5 else ""
        raise RuntimeError(
            "Working tree contains uncommitted changes or untracked files. "
            f"Release packaging requires a clean, committed Git working tree.\n  {sample}{suffix}"
        )


def verify_git_ref(repo_root: Path, ref: str) -> str:
    """Verify that the target Git ref exists and return its commit hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", f"{ref}^{{commit}}"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.SubprocessError as e:
        raise RuntimeError(f"Git ref '{ref}' not found or invalid: {e}") from e


def verify_release_tag(repo_root: Path, tag: str) -> str:
    """Return the commit hash the annotated release tag points at; fail closed otherwise.

    Resolves the tag through the refs/tags namespace only, so a branch sharing the
    tag name cannot satisfy the check, and requires the referenced object to be an
    annotated tag object rather than a lightweight tag pointing directly at a commit.
    """
    probe = f"refs/tags/{tag}"
    result = subprocess.run(
        ["git", "cat-file", "-t", probe],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        hint = ""
        branch_probe = subprocess.run(
            ["git", "show-ref", "--verify", f"refs/heads/{tag}"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        if branch_probe.returncode == 0:
            hint = f" (a branch named '{tag}' exists, but release tags must live in refs/tags/)"
        raise RuntimeError(
            f"Release tag '{tag}' not found{hint}. Release packaging requires an annotated tag "
            "matching the --version argument (see PUBLISHING.md). Pass --allow-untagged to archive "
            "untagged refs for local builds only."
        )
    if result.stdout.strip() != "tag":
        raise RuntimeError(
            f"Git tag '{tag}' is a lightweight tag pointing directly at a commit object. "
            "Release packaging requires an annotated tag created with 'git tag -a' (see PUBLISHING.md)."
        )
    return verify_git_ref(repo_root, probe)


def pack_release(
    version: str,
    output_dir: Path,
    repo_root: Path = ROOT,
    ref: str = "HEAD",
    prefix: str | None = None,
    check_clean: bool = True,
    require_tag: bool = True,
    skill_only: bool = False,
) -> Path:
    """Create a clean release ZIP archive from a committed Git tree."""
    if check_clean:
        assert_clean_git_tree(repo_root)

    commit_sha = verify_git_ref(repo_root, ref)
    clean_version = version.lstrip("v")
    tag_name = f"v{clean_version}"

    if require_tag:
        tag_commit = verify_release_tag(repo_root, tag_name)
        if tag_commit != commit_sha:
            raise RuntimeError(
                f"Git tag '{tag_name}' ({tag_commit[:8]}) does not point at ref '{ref}' ({commit_sha[:8]}). "
                "Version, tag and ref must agree on one commit before packaging a release; "
                "re-tag or pass --ref with the tagged refs' commit (see PUBLISHING.md)."
            )

    output_dir.mkdir(parents=True, exist_ok=True)
    if skill_only:
        zip_name = f"tech-me-skill-{clean_version}.zip"
        archive_prefix = "tech-me/" if prefix is None else prefix
        archive_target = f"{ref}:skills/tech-me"
    else:
        zip_name = f"tech-me-{clean_version}.zip"
        archive_prefix = f"tech-me-{clean_version}/" if prefix is None else prefix
        archive_target = ref
    zip_path = output_dir / zip_name

    tag_note = f"tag {tag_name}" if require_tag else "untagged (tag verification skipped)"
    kind_note = "skill-only " if skill_only else ""
    print(f"Packaging Tech-Me {kind_note}v{clean_version} ({tag_note}) from Git commit {commit_sha[:8]} (ref: {ref})...")

    # Run git archive directly to extract only the committed tree
    cmd = [
        "git",
        "archive",
        "--format=zip",
        f"--prefix={archive_prefix}",
        "-o",
        str(zip_path.resolve()),
        archive_target,
    ]

    try:
        subprocess.run(
            cmd,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.SubprocessError as e:
        zip_path.unlink(missing_ok=True)
        raise RuntimeError(f"git archive failed: {e}") from e

    # Post-archive security & integrity verification
    forbidden_items: list[str] = []
    names: list[str] = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        if not names:
            forbidden_items.append("EMPTY_ZIP")
        for name in names:
            if is_forbidden(name):
                forbidden_items.append(name)
        if skill_only:
            expected_skill_md = f"{archive_prefix}SKILL.md"
            if expected_skill_md not in names:
                forbidden_items.append(f"MISSING:{expected_skill_md}")
            if f"{archive_prefix}README.md" in names:
                forbidden_items.append(f"{archive_prefix}README.md")
            if archive_prefix and any(not name.startswith(archive_prefix) for name in names):
                forbidden_items.append("INVALID_ROOT_PREFIX")

    if forbidden_items:
        zip_path.unlink(missing_ok=True)
        raise RuntimeError(
            f"Integrity check failed: forbidden item found in release ZIP: {', '.join(forbidden_items)}"
        )
    size_kb = zip_path.stat().st_size / 1024
    print(f"Verification PASSED: {len(names)} committed entries, 0 forbidden artifacts.")
    print(f"Created: {zip_path} ({size_kb:.1f} KB)")
    return zip_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean release packager for Tech-Me")
    parser.add_argument(
        "--version",
        "-v",
        required=True,
        help="Release version string (e.g., '0.1.0' or 'v0.1.0')",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=ROOT / "dist",
        help="Output directory (default: dist/)",
    )
    parser.add_argument(
        "--ref",
        "-r",
        default="HEAD",
        help="Committed Git ref to package (default: HEAD)",
    )
    parser.add_argument(
        "--no-prefix",
        action="store_true",
        help="Do not prepend root folder prefix inside ZIP",
    )
    parser.add_argument(
        "--allow-untagged",
        action="store_true",
        help=(
            "Skip release tag verification. For local archives only; "
            "do not publish untagged builds."
        ),
    )
    parser.add_argument(
        "--skill-zip",
        action="store_true",
        help="Package only skills/tech-me/ rooted at tech-me/ (e.g., for claude.ai skill upload)",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=ROOT,
        help="Repository root directory (default: current repo root)",
    )

    args = parser.parse_args()
    prefix = "" if args.no_prefix else None

    try:
        pack_release(
            version=args.version,
            output_dir=args.output_dir,
            repo_root=args.repo_root,
            ref=args.ref,
            prefix=prefix,
            check_clean=True,
            require_tag=not args.allow_untagged,
            skill_only=args.skill_zip,
        )
        return 0
    except Exception as e:
        print(f"Packaging failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
