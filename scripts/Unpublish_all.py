#!/usr/bin/env python3
"""Mark every Schedule Markdown page as unpublished.

Run without --apply to preview the pages that would change. With --apply, this
script updates valid YAML front matter in every Markdown file under Schedule/.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


FRONT_MATTER_DELIMITER = "---"
PUBLICATION_PATTERN = re.compile(r"^(\s*(?:publish|published)\s*:\s*).*$", re.MULTILINE)


@dataclass(frozen=True)
class PublicationUpdate:
    """A validated publication-state update for one schedule page."""

    path: Path
    content: str


def updated_content(path: Path) -> str:
    """Return page content with every publication field set to false."""

    content = path.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)

    if not lines or lines[0].strip() != FRONT_MATTER_DELIMITER:
        raise ValueError("missing YAML front matter")

    closing_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == FRONT_MATTER_DELIMITER),
        None,
    )
    if closing_index is None:
        raise ValueError("front matter is missing its closing delimiter")

    front_matter = "".join(lines[1:closing_index])
    parsed = yaml.safe_load(front_matter) or {}
    if not isinstance(parsed, dict):
        raise ValueError("front matter must be a YAML mapping")

    updated_front_matter, replacements = PUBLICATION_PATTERN.subn(r"\1false", front_matter)
    if replacements == 0:
        updated_front_matter += "" if updated_front_matter.endswith("\n") else "\n"
        updated_front_matter += "published: false\n"

    return "".join([lines[0], updated_front_matter, *lines[closing_index:]])


def build_updates(schedule_dir: Path) -> list[PublicationUpdate]:
    """Validate all schedule pages before returning their proposed updates."""

    if not schedule_dir.is_dir():
        raise ValueError(f"schedule directory does not exist: {schedule_dir}")

    updates: list[PublicationUpdate] = []
    errors: list[str] = []
    for path in sorted(schedule_dir.glob("*.md")):
        try:
            content = updated_content(path)
        except (OSError, yaml.YAMLError, ValueError) as error:
            errors.append(f"{path}: {error}")
            continue
        if content != path.read_text(encoding="utf-8"):
            updates.append(PublicationUpdate(path=path, content=content))

    if errors:
        raise ValueError("Cannot update schedule publication state:\n" + "\n".join(errors))
    return updates


def main() -> int:
    """Preview updates and write them only when explicitly requested."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schedule-dir", default="Schedule", type=Path, help="Schedule directory to update")
    parser.add_argument("--apply", action="store_true", help="Write the proposed publication-state updates")
    parser.add_argument("--verbose", action="store_true", help="List every page that would change")
    args = parser.parse_args()

    try:
        updates = build_updates(args.schedule_dir)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    action = "Updated" if args.apply else "Would update"
    print(f"{action} {len(updates)} schedule page(s) to unpublished.")
    if args.verbose:
        for update in updates:
            print(update.path)

    if args.apply:
        for update in updates:
            update.path.write_text(update.content, encoding="utf-8")
        print("Regenerate the schedule data before publishing.")
    else:
        print("Run again with --apply to write these changes.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
