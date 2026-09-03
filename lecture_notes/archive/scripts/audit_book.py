#!/usr/bin/env python3
"""Audit exercise structure, selection tags, references, and local assets."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import update_recommendations


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "_quarto.yml"
LEGACY = ROOT / "ESQC_2024_text_and_exercises" / "ESQC2024_math_exercises.tex"

EXERCISE_PATTERN = re.compile(r"\{#(exr-[a-z0-9][a-z0-9-]*)\b")
SOLUTION_PATTERN = re.compile(
    r"^### Solution to @(exr-[a-z0-9][a-z0-9-]*)\s*$", re.MULTILINE
)
IMAGE_PATTERN = re.compile(r"!\[[^]]*\]\(([^)\s]+)")


def fail(message: str, failures: list[str]) -> None:
    """Record one audit failure."""
    failures.append(message)


def main() -> int:
    """Run all source-level migration checks."""
    failures: list[str] = []
    chapter_paths = update_recommendations.chapter_paths(
        CONFIG.read_text(encoding="utf-8")
    )
    missing_chapters = [path for path in chapter_paths if not path.exists()]
    for path in missing_chapters:
        fail(f"missing chapter: {path.relative_to(ROOT)}", failures)

    all_ids: list[str] = []
    all_solutions: list[str] = []
    for path in chapter_paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        ids = EXERCISE_PATTERN.findall(text)
        solutions = SOLUTION_PATTERN.findall(text)
        all_ids.extend(ids)
        all_solutions.extend(solutions)

        if ids and '.content-visible when-profile="tutor"' not in text:
            fail(f"missing tutor profile gate: {path.relative_to(ROOT)}", failures)

        for image_path in IMAGE_PATTERN.findall(text):
            if image_path.startswith(("http://", "https://")):
                continue
            target = (path.parent / image_path).resolve()
            if not target.exists():
                fail(
                    f"missing image {image_path!r} in {path.relative_to(ROOT)}",
                    failures,
                )

        if r"\mytag{" in text:
            fail(f"legacy selection tag in {path.relative_to(ROOT)}", failures)
        if r"\operatornamewithlimits" in text:
            fail(f"unsupported TeX command in {path.relative_to(ROOT)}", failures)

    duplicate_ids = [
        identifier for identifier, count in Counter(all_ids).items() if count > 1
    ]
    for identifier in duplicate_ids:
        fail(f"duplicate exercise ID: {identifier}", failures)

    id_set = set(all_ids)
    solution_counts = Counter(all_solutions)
    for identifier in sorted(id_set):
        count = solution_counts[identifier]
        if count != 1:
            fail(f"{identifier} has {count} solution headings", failures)
    for identifier in sorted(set(all_solutions) - id_set):
        fail(f"solution references missing exercise: {identifier}", failures)

    legacy_text = LEGACY.read_text(encoding="utf-8")
    legacy_recommended = legacy_text.count(r"\mytag{recommended}") - 1
    legacy_curious = legacy_text.count(r"\mytag{for the curious}")
    migrated_recommended = sum(
        identifier.startswith("exr-recommended-") for identifier in all_ids
    )
    migrated_curious = sum(
        identifier.startswith("exr-curious-") for identifier in all_ids
    )
    if migrated_recommended != legacy_recommended:
        fail(
            "recommended count differs: "
            f"legacy={legacy_recommended}, migrated={migrated_recommended}",
            failures,
        )
    if migrated_curious != legacy_curious:
        fail(
            f"curious count differs: legacy={legacy_curious}, migrated={migrated_curious}",
            failures,
        )

    if (
        update_recommendations.updated_text()
        != update_recommendations.RECOMMENDATIONS.read_text(encoding="utf-8")
    ):
        fail("generated recommendation lists are stale", failures)

    if failures:
        for message in failures:
            print(f"ERROR: {message}")
        return 1

    print(
        f"audit passed: {len(all_ids)} exercises, "
        f"{migrated_recommended} recommended, {migrated_curious} curious"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
