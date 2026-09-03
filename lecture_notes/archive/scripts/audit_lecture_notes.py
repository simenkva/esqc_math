#!/usr/bin/env python3
"""Audit the migrated ESQC lecture-note structure and local resources."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "_quarto.yml"
SOURCE_DIR = ROOT / "ESQC_2024_text_and_exercises"
SOURCE_FILES = (
    "sets_and_numbers.tex",
    "linear_algebra.tex",
    "topological_vector_spaces.tex",
    "measure_and_integration.tex",
    "functional_analysis.tex",
    "calculus.tex",
)

BLOCK_PATTERN = re.compile(r"\\begin\{(myDefinition|myTheorem|myLemma|myExample|myRemark)\}")
ID_PATTERN = re.compile(r"\{#((?:def|thm|lem|exm|rem|fig|eq|sec)-[a-z0-9-]+)")
REF_PATTERN = re.compile(r"@((?:def|thm|lem|exm|rem|fig|eq|sec)-[a-z0-9-]+)")
IMAGE_PATTERN = re.compile(r"!\[[^]]*\]\(([^)\s]+)\)")


def active_source() -> str:
    text = "\n".join(
        (SOURCE_DIR / filename).read_text(encoding="utf-8") for filename in SOURCE_FILES
    )
    return re.sub(
        r"\\begin\{comment\}.*?\\end\{comment\}",
        "",
        text,
        flags=re.DOTALL,
    )


def configured_files() -> list[Path]:
    paths = [ROOT / "index.qmd", ROOT / "references.qmd"]
    config = CONFIG.read_text(encoding="utf-8")
    for relative in re.findall(r"- (?:part: )?((?:parts|chapters)/[^\s]+\.qmd)", config):
        paths.append(ROOT / relative)
    return paths


def main() -> int:
    failures: list[str] = []
    paths = configured_files()
    missing = [path for path in paths if not path.exists()]
    failures.extend(f"missing configured file: {path.relative_to(ROOT)}" for path in missing)

    if len([path for path in paths if path.parent.name == "chapters"]) != 26:
        failures.append("expected 26 configured chapter files")
    if len([path for path in paths if path.parent.name == "parts"]) != 6:
        failures.append("expected 6 configured part files")

    texts: dict[Path, str] = {
        path: path.read_text(encoding="utf-8") for path in paths if path.exists()
    }
    combined = "\n".join(texts.values())

    source_blocks = BLOCK_PATTERN.findall(active_source())
    migrated_blocks = re.findall(
        r"\{#(?:def|thm|lem|exm|rem)-[a-z0-9-]+", combined
    )
    if len(source_blocks) != 182:
        failures.append(f"unexpected active source block count: {len(source_blocks)}")
    if len(migrated_blocks) != len(source_blocks):
        failures.append(
            f"semantic block count differs: source={len(source_blocks)}, migrated={len(migrated_blocks)}"
        )

    callouts = combined.count("::: {.recommended-reading}")
    if callouts != 14:
        failures.append(f"expected 14 recommended-reading callouts, found {callouts}")

    figures = re.findall(r"\{#fig-[a-z0-9-]+", combined)
    if len(figures) != 13:
        failures.append(f"expected 13 figure blocks, found {len(figures)}")

    ids = ID_PATTERN.findall(combined)
    for identifier, count in Counter(ids).items():
        if count > 1:
            failures.append(f"duplicate identifier: {identifier}")

    id_set = set(ids)
    for reference in sorted(set(REF_PATTERN.findall(combined))):
        if reference not in id_set:
            failures.append(f"unresolved source cross-reference: @{reference}")

    forbidden = {
        "legacy theorem environment": r"\\(?:begin|end)\{my",
        "legacy label command": r"\\label\{",
        "legacy reference command": r"\\(?:eq)?ref\{",
        "Pandoc reference artifact": r"reference-type=",
        "raw HTML figure": r"<fig(?:ure|caption)",
        "conversion token": r"ESQC(?:BLOCK|FIGURE|RECOMMENDATION|TODO)",
        "legacy illustration path": r"(?:illustrations|images)/",
        "legacy custom macro": r"\\(?:RR|CC|FF|QQ|NN|ZZ|TT|rmi|rmd|diff|pdiff|bvec|spn|axiomname|smallO|fconst)\b",
    }
    for label, pattern in forbidden.items():
        if re.search(pattern, combined):
            failures.append(f"found {label}")

    for path, text in texts.items():
        headings = re.findall(r"^# (?!#)", text, flags=re.MULTILINE)
        if len(headings) != 1:
            failures.append(
                f"{path.relative_to(ROOT)} has {len(headings)} level-one headings"
            )
        for image in IMAGE_PATTERN.findall(text):
            if image.startswith(("http://", "https://")):
                continue
            target = (path.parent / image).resolve()
            if not target.exists():
                failures.append(
                    f"missing image {image!r} in {path.relative_to(ROOT)}"
                )

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1

    print(
        "audit passed: "
        "26 chapters, 6 parts, 182 semantic blocks, "
        "14 reading callouts, 13 figures"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
