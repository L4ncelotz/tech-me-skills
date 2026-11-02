#!/usr/bin/env python3
"""Extract one version's release notes from CHANGELOG.md with explicit UTF-8.

A shell redirection must never own this encoding: PowerShell 5.1 redirects
silently write UTF-16, which produced unreadable GitHub release notes in a real
release. This script reads and writes the text itself with explicit UTF-8 and
fails closed if the generated file would contain a BOM or a NUL byte.

Standard library only.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_SUBSECTION_PREFIX = "### "
_BOM = b"\xef\xbb\xbf"


class NotesError(RuntimeError):
    """Raised when changelog extraction or output verification fails."""


def extract_release_notes(changelog: str, version: str) -> str:
    """Return the body of the '## [<version>]' section, ending at the next '## ' heading."""
    pattern = re.compile(
        rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(changelog)
    if match is None:
        raise NotesError(f"CHANGELOG has no '## [{version}]' section.")
    return validate_notes_text(version, match.group(1))


def validate_notes_text(version: str, notes: str) -> str:
    """Fail closed on malformed note bodies and return the normalized body."""
    stripped = notes.strip("\n")
    first = next((line for line in stripped.splitlines() if line.strip()), "")
    if not first.startswith(_SUBSECTION_PREFIX):
        raise NotesError(
            f"Release notes for {version} must start with a '{_SUBSECTION_PREFIX}' heading."
        )
    if re.search(r"^## ", stripped, flags=re.MULTILINE):
        raise NotesError(f"Release notes for {version} contain a stray '## ' heading.")
    return stripped + "\n"


def check_bom_and_nul(name: str, data: bytes) -> None:
    """Detect byte artifacts left behind by broken shell redirections."""
    if data.startswith(_BOM):
        raise NotesError(f"{name} starts with a UTF-8 BOM.")
    if b"\x00" in data:
        raise NotesError(f"{name} contains a NUL byte.")


def write_release_notes(version: str, changelog: str, output_path: Path) -> bytes:
    """Extract, write, and verify the release notes; return the written bytes."""
    notes = extract_release_notes(changelog, version)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = notes.encode("utf-8")
    output_path.write_bytes(data)
    written = output_path.read_bytes()
    if written != data:
        raise NotesError(f"{output_path} changed between write and read.")
    check_bom_and_nul(str(output_path), written)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", "-v", required=True, help="Version to extract, e.g. 0.1.1")
    parser.add_argument(
        "--changelog",
        type=Path,
        default=ROOT / "CHANGELOG.md",
        help="Changelog to extract from (default: CHANGELOG.md)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output path (default: dist/release-notes-<version>.md)",
    )
    args = parser.parse_args()

    output = args.output or (ROOT / "dist" / f"release-notes-{args.version}.md")
    try:
        changelog = args.changelog.read_text(encoding="utf-8")
        data = write_release_notes(args.version, changelog, output)
    except (NotesError, OSError, UnicodeError) as exc:
        print(f"Release notes extraction failed: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {output} ({len(data)} bytes; UTF-8, no BOM, no NUL)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
