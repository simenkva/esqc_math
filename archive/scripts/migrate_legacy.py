#!/usr/bin/env python3
"""Convert the 2024 LaTeX exercise collection into Quarto chapters.

The converter performs the mechanical part of the migration. It preserves the
source wording, separates student tasks from solutions, maps legacy selection
tags to exercise-ID prefixes, and groups source sections by mathematical
subject. Review and rendering remain required after generation.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "ESQC_2024_text_and_exercises" / "ESQC2024_math_exercises.tex"
CHAPTER_DIR = ROOT / "chapters"

RECOMMENDED = "ESQCRECOMMENDEDTAG"
CURIOUS = "ESQCCURIOUSTAG"
ITEM_PATTERN = re.compile(r"^(\d+)\.\s{2}(.*)$")
HEADER_PATTERN = re.compile(r"^(#{1,3})\s+(.+?)\s*$")
SOLUTION_START = re.compile(r"^:::\s+solution\s*$")

MATH_MACROS = r"""
\newcommand{\rmi}{\mathrm{i}}
\newcommand{\rmd}{\mathrm{d}}
\newcommand{\RR}{\mathbb{R}}
\newcommand{\CC}{\mathbb{C}}
\newcommand{\FF}{\mathbb{F}}
\newcommand{\QQ}{\mathbb{Q}}
\newcommand{\NN}{\mathbb{N}}
\newcommand{\ZZ}{\mathbb{Z}}
\newcommand{\TT}{\mathbb{T}}
\newcommand{\bvec}[1]{\mathbf{#1}}
\newcommand{\spn}{\operatorname{span}}
\newcommand{\Tr}{\operatorname{Tr}}
\newcommand{\pdiff}[2]{\frac{\partial #1}{\partial #2}}
\newcommand{\diff}[2]{\frac{\mathrm{d} #1}{\mathrm{d} #2}}
\newcommand{\smallO}{\mathcal{O}}
\newcommand{\ket}[1]{\left|#1\right\rangle}
\newcommand{\bra}[1]{\left\langle#1\right|}
\newcommand{\braket}[1]{\left\langle#1\right\rangle}
\newcommand{\dag}{\dagger}
\newcommand{\mathbbm}[1]{\mathbf{#1}}
\newcommand{\axiomname}[1]{\quad\text{#1}}
"""


@dataclass(frozen=True)
class ChapterSpec:
    """A generated chapter and the legacy units that supply its content."""

    filename: str
    title: str
    introduction: str
    units: tuple[str, ...]


@dataclass
class ConvertedUnit:
    """Converted student content, solutions, and tutor notes for one unit."""

    title: str
    prelude: str
    exercises: str
    solutions: list[tuple[str, str]]
    tutor_notes: list[str]


CHAPTERS = (
    ChapterSpec(
        "sets-and-functions.qmd",
        "Sets and functions",
        "These exercises use elementary set notation, ordered pairs, Cartesian products, functions, and complements.",
        ("Sets etc.",),
    ),
    ChapterSpec(
        "cardinality-and-countability.qmd",
        "Cardinality and countability",
        "Cardinality compares sets through bijections. The exercises cover countable sets, Cantor's diagonal argument, and the cardinality of the continuum.",
        ("Cardinality of numbers",),
    ),
    ChapterSpec(
        "general-vector-spaces.qmd",
        "General vector spaces",
        "A vector space needs vector addition and scalar multiplication, but it need not resemble Euclidean coordinate space.",
        ("General vector spaces",),
    ),
    ChapterSpec(
        "vectors-and-matrices.qmd",
        "Vectors and matrices",
        "These exercises connect bases and vector decomposition with matrix multiplication and linear systems.",
        ("Basic vectors", "More vectors and matrices"),
    ),
    ChapterSpec(
        "complex-vector-space.qmd",
        "The complex numbers as a real vector space",
        r"Identifying $x + \mathrm{i}y$ with $(x,y)$ turns the complex plane into a two-dimensional real vector space.",
        ("The complex numbers as a real vector space",),
    ),
    ChapterSpec(
        "gaussian-elimination.qmd",
        "Gaussian elimination",
        "Elementary row operations solve linear systems, compute inverses, and expose the rank and consistency of a system.",
        ("Elementary row operations and Gaussian elimination",),
    ),
    ChapterSpec(
        "bra-ket-notation.qmd",
        "Bra-ket notation",
        "Bra-ket notation represents vectors, inner products, operators, and basis expansions in a form used throughout quantum mechanics.",
        ("Bra-ket notation",),
    ),
    ChapterSpec(
        "eigenvalues-and-diagonalization.qmd",
        "Eigenvalues and diagonalization",
        "These exercises develop the spectral theorem and apply determinants to finite-dimensional eigenvalue problems.",
        ("Eigenvalue decomposition", "Diagonalization of a matrix"),
    ),
    ChapterSpec(
        "gram-schmidt.qmd",
        "Gram--Schmidt orthogonalization",
        "Orthogonal projection leads to the Gram--Schmidt construction and the QR factorization of a full-rank matrix.",
        ("Gram--Schmidt orthogonalization",),
    ),
    ChapterSpec(
        "singular-value-decomposition.qmd",
        "The singular-value decomposition",
        "The singular-value decomposition gives orthogonal matrix expansions and low-rank approximations, including image compression.",
        ("The singular value decomposition as a compression tool",),
    ),
    ChapterSpec(
        "polynomial-vector-spaces.qmd",
        "Polynomial vector spaces",
        "Polynomials form finite-dimensional vector spaces on which differentiation, multiplication, and changes of basis act as linear maps.",
        ("Space of polynomials",),
    ),
    ChapterSpec(
        "metric-spaces.qmd",
        "Metric spaces",
        "A metric measures distance through symmetry, positivity, and the triangle inequality.",
        ("Metric spaces",),
    ),
    ChapterSpec(
        "open-and-closed-sets.qmd",
        "Open and closed sets in Euclidean space",
        "Open balls define interior points, open sets, closed sets, boundaries, and closures in Euclidean space.",
        ("Open and closed sets in Euclidean space",),
    ),
    ChapterSpec(
        "visualizing-functions.qmd",
        "Visualizing functions",
        "Graphs, level sets, and vector fields provide complementary views of scalar- and vector-valued functions.",
        ("Visualization of functions",),
    ),
    ChapterSpec(
        "continuity-and-differentiability.qmd",
        "Continuity and differentiability",
        "Limits define continuity, while partial derivatives describe local change for functions of several variables.",
        ("Continuity", "Differentiability"),
    ),
    ChapterSpec(
        "matrix-exponentials-and-commutators.qmd",
        "Matrix exponentials and commutators",
        "Power series define matrix exponentials. Differentiating products of exponentials produces nested commutators.",
        ("Taylor polynomials",),
    ),
    ChapterSpec(
        "complex-arithmetic.qmd",
        "Complex arithmetic and geometry",
        "Cartesian and polar forms connect complex arithmetic with plane geometry, rotations, dot products, and cross products.",
        ("Complex numbers", "Basic calculations"),
    ),
    ChapterSpec(
        "complex-sets.qmd",
        "Subsets of the complex plane",
        "The modulus and real and imaginary parts describe curves and regions in the complex plane.",
        ("Visualizing complex sets",),
    ),
    ChapterSpec(
        "complex-exponential.qmd",
        "The complex exponential",
        "The functional equation for the exponential and the Cauchy--Riemann equations determine the complex exponential.",
        ("Complex functions / The complex exponential function",),
    ),
    ChapterSpec(
        "complex-power-series.qmd",
        "Complex power series",
        "Geometric and exponential series give power-series representations of elementary complex functions.",
        ("Complex functions / Taylor series",),
    ),
    ChapterSpec(
        "singularities-and-contour-integrals.qmd",
        "Singularities and contour integrals",
        "Laurent series classify isolated singularities and determine contour integrals around poles.",
        ("Complex functions / Singularities", "Complex functions / Line integrals"),
    ),
    ChapterSpec(
        "dual-numbers.qmd",
        "Dual numbers and automatic differentiation",
        r"Dual numbers adjoin a nonzero element $\varepsilon$ with $\varepsilon^2=0$, which encodes first derivatives algebraically.",
        ("Dual numbers",),
    ),
    ChapterSpec(
        "newtons-method.qmd",
        "Newton's method",
        "Newton's method replaces a nonlinear system by its first-order Taylor approximation at each iteration.",
        ("Newton--Rhapson method",),
    ),
    ChapterSpec(
        "complex-step-differentiation.qmd",
        "Complex-step differentiation",
        "Complex-step differentiation estimates derivatives without the subtractive cancellation of a centered finite difference.",
        ("Complex step method",),
    ),
)


def latex_body() -> str:
    """Read and preprocess the active exercise body for Pandoc."""
    source = SOURCE.read_text(encoding="utf-8")
    start = source.index(r"\chapter{Exercise set 1: Introduction}")
    end = source.rindex(r"\end{document}")
    body = source[start:end]
    body = body.replace(r"\mytag{recommended}", f" {RECOMMENDED} ")
    body = body.replace(r"\mytag{for the curious}", f" {CURIOUS} ")

    environments = {
        "myDefinitionx": "Definition",
        "myDefinition": "Definition",
        "myExamplex": "Example",
        "myExample": "Example",
        "myLemma": "Lemma",
        "myTheorem": "Theorem",
    }
    for environment, label in environments.items():
        begin = re.compile(rf"\\begin\{{{environment}\}}\{{([^{{}}]*)\}}\{{[^{{}}]*\}}")
        body = begin.sub(rf"\\begin{{quote}}\\textbf{{{label}: \1.}}", body)
        body = body.replace(rf"\end{{{environment}}}", r"\end{quote}")

    asset_paths = {
        "illustrations/chess.ai": "../figures/exercises/chess.svg",
        "images/sol-fig1.png": "../figures/exercises/sol-fig1.png",
        "images/parrot.jpg": "../figures/exercises/parrot.jpg",
        "images/parallelogram_rule.png": "../figures/exercises/parallelogram-rule.png",
    }
    for old, new in asset_paths.items():
        body = body.replace(old, new)

    return MATH_MACROS + "\n" + body


def pandoc_markdown(source: str) -> str:
    """Use Pandoc's LaTeX reader for the syntax-level conversion."""
    command = [
        "pandoc",
        "--from=latex",
        "--to=markdown+tex_math_dollars+raw_tex",
        "--wrap=none",
    ]
    result = subprocess.run(
        command,
        input=source,
        text=True,
        capture_output=True,
        check=False,
        cwd=ROOT,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    return clean_markdown(result.stdout)


def clean_markdown(text: str) -> str:
    """Normalize Pandoc artifacts and source cross-references."""
    replacements = {
        'Figure\u00a0[2.1](#fig:chessboard){reference-type="ref" reference="fig:chessboard"}': "@fig-chessboard",
        'Figure\u00a0[3.1](#fig:parrot){reference-type="ref" reference="fig:parrot"}': "@fig-parrot",
        'Eq.\u00a0[\\[eq:1\\]](#eq:1){reference-type="eqref" reference="eq:1"}': "the basis defined in the vectors and matrices chapter",
        'Eq.\u00a0[\\[eq:legendrediff\\]](#eq:legendrediff){reference-type="eqref" reference="eq:legendrediff"}': "the derivative relation above",
        '[\\[item:needed\\]](#item:needed){reference-type="ref" reference="item:needed"}': "that normality is preserved by unitary similarity",
        '[\\[x\\]](#x){reference-type="ref" reference="x"}': "the hyperbolic-paraboloid exercise above",
        '[]{#x label="x"} ': "",
        r" \label{eq:legendrediff}": "",
        r"\y": r"\\ y",
        r"\operatornamewithlimits{arg min}": r"\mathop{\mathrm{arg\,min}}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace("#fig:chessboard", "#fig-chessboard")
    text = text.replace("#fig:parrot", "#fig-parrot")
    text = text.replace("#fig:parallelogram_rule", "#fig-parallelogram-rule")
    text = re.sub(r"\[\]\{#[^}]+\}\s*", "", text)
    text = re.sub(r'\{reference-type="[^"]+" reference="[^"]+"\}', "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def source_units(markdown: str) -> dict[str, str]:
    """Split converted Markdown into legacy sections and subsections."""
    lines = markdown.splitlines()
    units: dict[str, str] = {}
    index = 0
    while index < len(lines):
        match = HEADER_PATTERN.match(lines[index])
        if not match or match.group(1) != "##":
            index += 1
            continue

        section_title = match.group(2)
        end = index + 1
        while end < len(lines):
            next_header = HEADER_PATTERN.match(lines[end])
            if next_header and len(next_header.group(1)) <= 2:
                break
            end += 1

        section_lines = lines[index + 1 : end]
        subsection_starts = [
            offset
            for offset, line in enumerate(section_lines)
            if line.startswith("### ")
        ]
        if not subsection_starts:
            units[section_title] = "\n".join(section_lines).strip()
        else:
            prelude = section_lines[: subsection_starts[0]]
            for position, start in enumerate(subsection_starts):
                stop = (
                    subsection_starts[position + 1]
                    if position + 1 < len(subsection_starts)
                    else len(section_lines)
                )
                subsection_title = section_lines[start][4:].strip()
                content = section_lines[start + 1 : stop]
                if position == 0:
                    content = prelude + content
                key = f"{section_title} / {subsection_title}"
                units[key] = "\n".join(content).strip()
        index = end
    return units


def extract_divs(text: str, div_class: str = "solution") -> tuple[str, list[str]]:
    """Remove fenced divs of one class and return their contents."""
    lines = text.splitlines()
    kept: list[str] = []
    extracted: list[str] = []
    index = 0
    while index < len(lines):
        if lines[index].strip() != f"::: {div_class}":
            kept.append(lines[index])
            index += 1
            continue

        base_indent = len(lines[index]) - len(lines[index].lstrip())
        content: list[str] = []
        index += 1
        while index < len(lines):
            line = lines[index]
            indent = len(line) - len(line.lstrip())
            if line.strip() == ":::" and indent == base_indent:
                break
            if base_indent and line.startswith(" " * base_indent):
                line = line[base_indent:]
            content.append(line)
            index += 1
        if index == len(lines):
            raise ValueError(f"unterminated {div_class} div")
        extracted.append("\n".join(content).strip())
        index += 1
    return trim("\n".join(kept)), extracted


def first_item_index(lines: list[str]) -> int | None:
    """Return the first top-level ordered-list item index."""
    for index, line in enumerate(lines):
        if ITEM_PATTERN.match(line):
            return index
    return None


def item_block(lines: list[str], start: int) -> tuple[list[str], int]:
    """Read one Pandoc top-level ordered-list item and dedent its body."""
    first = ITEM_PATTERN.match(lines[start])
    assert first is not None
    body = [first.group(2)]
    index = start + 1
    while index < len(lines):
        line = lines[index]
        if ITEM_PATTERN.match(line):
            break
        if line and not line.startswith("    "):
            break
        body.append(line[4:] if line.startswith("    ") else line)
        index += 1
    return body, index


def identifier(text: str, fallback: str, used: set[str]) -> str:
    """Create a short descriptive identifier from an exercise prompt."""
    plain = re.sub(r"\$+.*?\$+", " ", text, flags=re.DOTALL)
    plain = re.sub(r"\\[A-Za-z]+", " ", plain)
    plain = re.sub(r"[^A-Za-z0-9]+", " ", plain).lower()
    stop_words = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "be",
        "by",
        "for",
        "from",
        "in",
        "is",
        "let",
        "of",
        "on",
        "show",
        "that",
        "the",
        "this",
        "to",
        "using",
        "we",
        "what",
        "which",
        "with",
    }
    words = [word for word in plain.split() if word not in stop_words]
    base = "-".join(words[:6]) or fallback
    candidate = base
    suffix = 2
    while candidate in used:
        candidate = f"{base}-{suffix}"
        suffix += 1
    used.add(candidate)
    return candidate


def selection_prefix(text: str, default: str = "") -> tuple[str, str]:
    """Remove a tag sentinel and return the corresponding ID prefix."""
    if RECOMMENDED in text:
        return "recommended-", trim(text.replace(RECOMMENDED, ""))
    if CURIOUS in text:
        return "curious-", trim(text.replace(CURIOUS, ""))
    return default, text


def convert_unit(
    title: str, content: str, used: set[str], namespace: str
) -> ConvertedUnit:
    """Convert one legacy unit to template-shaped exercise content."""
    first_item = first_item_index(content.splitlines())
    leading = (
        content if first_item is None else "\n".join(content.splitlines()[:first_item])
    )
    whole_prefix, leading = selection_prefix(leading)
    leading, tutor_notes = extract_divs(leading)

    if first_item is None:
        remaining = content
        if leading:
            remaining = remaining.replace(
                content.splitlines()[0], leading.splitlines()[0], 1
            )
        remaining, extra_notes = extract_divs(remaining)
        tutor_notes.extend(extra_notes)
        return ConvertedUnit(title, remaining, "", [], tutor_notes)

    lines = content.splitlines()
    prelude_lines = lines[:first_item]
    remainder_lines = lines[first_item:]
    prelude = "\n".join(prelude_lines)
    _, prelude = selection_prefix(prelude)
    prelude, prelude_notes = extract_divs(prelude)
    tutor_notes.extend(note for note in prelude_notes if note not in tutor_notes)

    if whole_prefix:
        body = "\n".join(remainder_lines)
        body, source_solutions = extract_divs(body)
        base = f"{namespace}-{identifier(title, 'exercise', used)}"
        exercise_id = f"exr-{whole_prefix}{base}"
        solution_parts = []
        for number, solution in enumerate(source_solutions, start=1):
            solution_parts.append(f"**Source solution {number}.**\n\n{solution}")
        solution = "\n\n".join(solution_parts)
        if not solution:
            solution = "*The source does not supply a solution.*"
        exercise = f":::{{#{exercise_id}}}\n\n{body}\n\n:::"
        return ConvertedUnit(
            title, prelude, exercise, [(exercise_id, solution)], tutor_notes
        )

    output: list[str] = []
    solutions: list[tuple[str, str]] = []
    index = 0
    while index < len(remainder_lines):
        if not ITEM_PATTERN.match(remainder_lines[index]):
            context_start = index
            index += 1
            while index < len(remainder_lines) and not ITEM_PATTERN.match(
                remainder_lines[index]
            ):
                index += 1
            context = "\n".join(remainder_lines[context_start:index])
            context, notes = extract_divs(context)
            tutor_notes.extend(notes)
            if context:
                output.append(context)
            continue

        body_lines, index = item_block(remainder_lines, index)
        body = trim("\n".join(body_lines))
        prefix, body = selection_prefix(body)
        body, source_solutions = extract_divs(body)
        base = f"{namespace}-{identifier(body, 'exercise', used)}"
        exercise_id = f"exr-{prefix}{base}"
        output.append(f":::{{#{exercise_id}}}\n\n{body}\n\n:::")
        solution = "\n\n".join(source_solutions)
        if not solution:
            solution = "*The source does not supply a solution.*"
        solutions.append((exercise_id, solution))

    return ConvertedUnit(
        title,
        prelude,
        trim("\n\n".join(output)),
        solutions,
        tutor_notes,
    )


def trim(text: str) -> str:
    """Strip outer whitespace and collapse runs of blank lines."""
    return re.sub(r"\n{3,}", "\n\n", text.strip())


def chapter_text(spec: ChapterSpec, units: dict[str, str]) -> str:
    """Build one complete exercise chapter from its source units."""
    used: set[str] = set()
    namespace = spec.filename.removesuffix(".qmd")
    converted = [
        convert_unit(name, units[name], used, namespace) for name in spec.units
    ]
    lines = [f"# {spec.title}", "", spec.introduction, ""]

    if len(converted) == 1 and converted[0].prelude:
        lines.extend([converted[0].prelude, ""])
    lines.extend(["## Exercises", ""])

    for position, unit in enumerate(converted):
        if len(converted) > 1:
            display_title = unit.title.split(" / ")[-1]
            lines.extend([f"### {display_title}", ""])
            if unit.prelude:
                lines.extend([unit.prelude, ""])
        if unit.exercises:
            lines.extend([unit.exercises, ""])

    lines.extend(
        ['::: {.content-visible when-profile="tutor"}', "", "## Solutions", ""]
    )
    for unit in converted:
        for note in unit.tutor_notes:
            label = unit.title.split(" / ")[-1]
            lines.extend([f"### Tutor note: {label}", "", note, ""])
        for exercise_id, solution in unit.solutions:
            lines.extend([f"### Solution to @{exercise_id}", "", solution, ""])
    lines.extend([":::", ""])

    text = trim("\n".join(lines)) + "\n"
    if spec.filename == "matrix-exponentials-and-commutators.qmd":
        text = text.replace(
            ":::{#exr-matrix-exponentials-and-commutators-consider-matrix-valued-function}",
            "<!-- SOURCE REVIEW: The 2024 tutor note says this item has no question. -->\n\n"
            ":::{#exr-matrix-exponentials-and-commutators-consider-matrix-valued-function}",
        )
    return text


def main() -> int:
    """Generate all mapped exercise chapters."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite chapters that may contain post-conversion review edits",
    )
    args = parser.parse_args()

    existing = [CHAPTER_DIR / spec.filename for spec in CHAPTERS]
    if not args.force and any(path.exists() for path in existing):
        print("migration chapters already exist; use --force to replace them")
        return 2

    markdown = pandoc_markdown(latex_body())
    units = source_units(markdown)
    expected = {unit for chapter in CHAPTERS for unit in chapter.units}
    missing = sorted(expected - units.keys())
    if missing:
        raise ValueError(f"missing source units: {', '.join(missing)}")

    for spec in CHAPTERS:
        target = CHAPTER_DIR / spec.filename
        target.write_text(chapter_text(spec, units), encoding="utf-8")
        print(f"wrote {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
