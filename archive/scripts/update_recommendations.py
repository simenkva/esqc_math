#!/usr/bin/env python3
"""Update generated exercise-selection lists in the Quarto book."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QUARTO_CONFIG = ROOT / "_quarto.yml"
RECOMMENDATIONS = ROOT / "chapters" / "recommendations-first-day.qmd"

CHAPTER_PATTERN = re.compile(r"^\s*-\s+(.+?\.qmd)\s*$")
EXERCISE_PATTERN = re.compile(r"\{#(exr-[a-z0-9][a-z0-9-]*)\b")
TITLE_PATTERN = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Exercise:
    """An exercise ID and the chapter that contains it."""

    identifier: str
    chapter: str


def chapter_paths(config_text: str) -> list[Path]:
    """Return QMD paths in the order listed by the book configuration."""
    paths: list[Path] = []
    for line in config_text.splitlines():
        match = CHAPTER_PATTERN.match(line)
        if not match:
            continue
        value = match.group(1).strip().strip("\"'")
        paths.append(ROOT / value)
    return paths


def collect_exercises(paths: list[Path]) -> list[Exercise]:
    """Collect exercise IDs in book and document order, rejecting duplicates."""
    exercises: list[Exercise] = []
    locations: dict[str, Path] = {}

    for path in paths:
        text = path.read_text(encoding="utf-8")
        title_match = TITLE_PATTERN.search(text)
        chapter = title_match.group(1) if title_match else path.stem

        for identifier in EXERCISE_PATTERN.findall(text):
            if identifier in locations:
                first = locations[identifier].relative_to(ROOT)
                second = path.relative_to(ROOT)
                raise ValueError(
                    f"duplicate exercise ID {identifier!r} in {first} and {second}"
                )
            locations[identifier] = path
            exercises.append(Exercise(identifier, chapter))

    return exercises


def selection_lines(exercises: list[Exercise], prefix: str) -> str:
    """Build a chapter-grouped Markdown list for one exercise-ID prefix."""
    selected = [item for item in exercises if item.identifier.startswith(prefix)]
    if not selected:
        return "<!-- No matching exercises. -->"

    lines: list[str] = []
    current_chapter = ""
    for exercise in selected:
        if exercise.chapter != current_chapter:
            if lines:
                lines.append("")
            lines.append(f"- **{exercise.chapter}**")
            current_chapter = exercise.chapter
        lines.append(f"  - @{exercise.identifier}")
    return "\n".join(lines)


def replace_region(text: str, name: str, generated: str) -> str:
    """Replace one generated region while retaining its marker comments."""
    begin = f"<!-- BEGIN GENERATED {name} EXERCISES -->"
    end = f"<!-- END GENERATED {name} EXERCISES -->"
    pattern = re.compile(rf"({re.escape(begin)})\n.*?\n({re.escape(end)})", re.DOTALL)
    if len(pattern.findall(text)) != 1:
        raise ValueError(f"expected one {name.lower()} generated region")
    return pattern.sub(rf"\1\n{generated}\n\2", text)


def updated_text() -> str:
    """Return the recommendation page with both generated lists updated."""
    config_text = QUARTO_CONFIG.read_text(encoding="utf-8")
    exercises = collect_exercises(chapter_paths(config_text))
    text = RECOMMENDATIONS.read_text(encoding="utf-8")
    text = replace_region(
        text,
        "RECOMMENDED",
        selection_lines(exercises, "exr-recommended-"),
    )
    return replace_region(
        text,
        "CURIOUS",
        selection_lines(exercises, "exr-curious-"),
    )


def main() -> int:
    """Update the page or check that its generated regions are current."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report stale generated content without changing the file",
    )
    args = parser.parse_args()

    old_text = RECOMMENDATIONS.read_text(encoding="utf-8")
    new_text = updated_text()
    if args.check:
        if old_text != new_text:
            print(f"{RECOMMENDATIONS.relative_to(ROOT)} is out of date")
            return 1
        print(f"{RECOMMENDATIONS.relative_to(ROOT)} is up to date")
        return 0

    if old_text != new_text:
        RECOMMENDATIONS.write_text(new_text, encoding="utf-8")
        print(f"updated {RECOMMENDATIONS.relative_to(ROOT)}")
    else:
        print(f"{RECOMMENDATIONS.relative_to(ROOT)} is already up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
