#!/usr/bin/env python3
"""Migrate the 2024 ESQC mathematics lecture notes to Quarto Markdown.

This script performs the repeatable mechanical conversion. The generated QMD
files are intended to be reviewed and curated after generation.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "ESQC_2024_text_and_exercises"
CHAPTER_DIR = ROOT / "chapters"
PART_DIR = ROOT / "parts"
FIGURE_DIR = ROOT / "figures" / "lecture-notes"
READING_DIR = FIGURE_DIR / "recommended-reading"


@dataclass(frozen=True)
class PartSpec:
    source: str
    slug: str
    sections: tuple[tuple[str, str], ...]


PARTS = (
    PartSpec(
        "sets_and_numbers.tex",
        "fundamentals",
        (
            ("Introduction", "fundamentals-introduction.qmd"),
            ("Preliminary notes", "fundamentals-preliminary-notes.qmd"),
            ("Numbers", "fundamentals-numbers.qmd"),
        ),
    ),
    PartSpec(
        "linear_algebra.tex",
        "linear-algebra",
        (
            ("Finite dimensional vector spaces", "linear-algebra-finite-dimensional.qmd"),
            ("Inner product spaces", "linear-algebra-inner-product-spaces.qmd"),
            ("Matrices", "linear-algebra-matrices.qmd"),
        ),
    ),
    PartSpec(
        "topological_vector_spaces.tex",
        "topology",
        (
            ("The notion of a topology", "topology-notion.qmd"),
            ("Metric space hierarchy", "topology-metric-space-hierarchy.qmd"),
            ("Some topological concepts", "topology-concepts.qmd"),
        ),
    ),
    PartSpec(
        "measure_and_integration.tex",
        "measure-and-integration",
        (
            ("Measurable sets", "measure-measurable-sets.qmd"),
            ("Measure", "measure.qmd"),
            ("The integral", "measure-integral.qmd"),
            (
                "Lebesgue measure and the Lebesgue integral",
                "measure-lebesgue-measure-and-integral.qmd",
            ),
            ("Lebesgue spaces", "measure-lebesgue-spaces.qmd"),
        ),
    ),
    PartSpec(
        "functional_analysis.tex",
        "functional-analysis",
        (
            ("Infinite dimensions", "functional-analysis-infinite-dimensions.qmd"),
            ("$L^p$ spaces (Lebesgue spaces)", "functional-analysis-lp-spaces.qmd"),
            ("Hilbert spaces", "functional-analysis-hilbert-spaces.qmd"),
            ("Linear transformations", "functional-analysis-linear-transformations.qmd"),
            (
                "Operators over separable Hilbert spaces",
                "functional-analysis-operators.qmd",
            ),
            (
                "Weak formulation of the Schrodinger equation",
                "functional-analysis-weak-schrodinger.qmd",
            ),
            ("The Fourier transform", "functional-analysis-fourier-transform.qmd"),
            ("Distributions", "functional-analysis-distributions.qmd"),
        ),
    ),
    PartSpec(
        "calculus.tex",
        "calculus-and-complex-analysis",
        (
            ("Introductory remarks", "calculus-introductory-remarks.qmd"),
            ("Functions of several variables", "calculus-several-variables.qmd"),
            (
                "The tools of calculus [move/edit this material]",
                "calculus-tools.qmd",
            ),
            ("Complex analysis", "complex-analysis.qmd"),
        ),
    ),
)


MATH_MACROS = r"""
\newcommand{\rmi}{\mathrm{i}}
\newcommand{\rmd}{\mathrm{d}}
\newcommand{\diff}[2]{\frac{\mathrm{d} #1}{\mathrm{d} #2}}
\newcommand{\pdiff}[2]{\frac{\partial #1}{\partial #2}}
\newcommand{\cl}{\operatorname{cl}}
\newcommand{\interior}{\operatorname{int}}
\renewcommand{\Re}{\operatorname{Re}}
\renewcommand{\Im}{\operatorname{Im}}
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
\newcommand{\Arg}{\operatorname{Arg}}
\newcommand{\salgebra}[1]{\boldsymbol{#1}}
\newcommand{\smallO}{\mathcal{O}}
\newcommand{\axiomname}[1]{\qquad\textit{#1}}
\newcommand{\fconst}{\frac{1}{(2\pi)^{n/2}}}
\newcommand{\ket}[1]{\left|#1\right\rangle}
\newcommand{\bra}[1]{\left\langle#1\right|}
\newcommand{\braket}[1]{\left\langle#1\right\rangle}
\newcommand{\mathbbm}[1]{\mathbf{#1}}
"""


ENVIRONMENTS = {
    "myDefinition": ("def", "Definition"),
    "myTheorem": ("thm", "Statement"),
    "myLemma": ("lem", "Lemma"),
    "myExample": ("exm", "Example"),
    "myRemark": ("rem", "Remark"),
}


class Converter:
    def __init__(self) -> None:
        self.counter = 0
        self.used_ids: set[str] = set()
        self.block_tokens: dict[str, tuple[str, str]] = {}
        self.recommendation_tokens: dict[str, str] = {}
        self.figure_tokens: dict[str, tuple[str, list[tuple[str, str]]]] = {}
        self.todo_tokens: dict[str, str] = {}
        self.label_map: dict[str, str] = {}

    def token(self, kind: str) -> str:
        self.counter += 1
        return f"ESQC{kind}{self.counter:04d}"

    @staticmethod
    def slug(text: str) -> str:
        text = re.sub(r"\\[A-Za-z]+", " ", text)
        text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
        return text or "untitled"

    def unique_id(self, prefix: str, preferred: str) -> str:
        base = f"{prefix}-{self.slug(preferred)}"
        identifier = base
        suffix = 2
        while identifier in self.used_ids:
            identifier = f"{base}-{suffix}"
            suffix += 1
        self.used_ids.add(identifier)
        return identifier

    @staticmethod
    def parse_group(text: str, start: int) -> tuple[str, int]:
        if start >= len(text) or text[start] != "{":
            raise ValueError("expected a brace group")
        depth = 0
        index = start
        while index < len(text):
            if text[index] == "{" and (index == 0 or text[index - 1] != "\\"):
                depth += 1
            elif text[index] == "}" and (index == 0 or text[index - 1] != "\\"):
                depth -= 1
                if depth == 0:
                    return text[start + 1 : index], index + 1
            index += 1
        raise ValueError("unterminated brace group")

    def replace_command(
        self,
        text: str,
        command: str,
        groups: int,
        replacement,
    ) -> str:
        needle = f"\\{command}"
        output: list[str] = []
        position = 0
        while True:
            found = text.find(needle, position)
            if found < 0:
                output.append(text[position:])
                break
            output.append(text[position:found])
            cursor = found + len(needle)
            while cursor < len(text) and text[cursor].isspace():
                cursor += 1
            values: list[str] = []
            try:
                for _ in range(groups):
                    value, cursor = self.parse_group(text, cursor)
                    values.append(value)
                    while cursor < len(text) and text[cursor].isspace():
                        cursor += 1
            except ValueError:
                output.append(needle)
                position = found + len(needle)
                continue
            output.append(replacement(*values))
            position = cursor
        return "".join(output)

    def replace_comments(self, text: str) -> str:
        text = re.sub(
            r"\\begin\{comment\}.*?\\end\{comment\}",
            "",
            text,
            flags=re.DOTALL,
        )
        return re.sub(r"(?<!\\)%[^\n]*", "", text)

    def replace_todos(self, text: str) -> str:
        def replacement(body: str) -> str:
            token = self.token("TODO")
            self.todo_tokens[token] = body.strip()
            return token

        return self.replace_command(text, "todo", 1, replacement)

    def replace_recommendations(self, text: str) -> str:
        def replacement(body: str, image: str) -> str:
            token = self.token("RECOMMENDATION")
            filename = Path(image).name
            if not Path(filename).suffix:
                filename += ".png"
            filename = filename.replace("_", "-")
            self.recommendation_tokens[token] = filename
            return (
                f"\\par {token}BEGIN \\par\n"
                f"{body}\n"
                f"\\par {token}END \\par\n"
            )

        return self.replace_command(text, "recommended", 2, replacement)

    def replace_figures(self, text: str) -> str:
        pattern = re.compile(
            r"\\begin\{figure\}(?P<body>.*?)\\end\{figure\}",
            flags=re.DOTALL,
        )

        def replacement(match: re.Match[str]) -> str:
            body = match.group("body")
            label_match = re.search(r"\\label\{([^}]+)\}", body)
            if not label_match:
                return match.group(0)
            legacy_label = label_match.group(1)
            identifier = self.label_map[legacy_label]

            caption = "Illustration"
            caption_start = body.find(r"\caption")
            if caption_start >= 0:
                cursor = caption_start + len(r"\caption")
                while cursor < len(body) and body[cursor].isspace():
                    cursor += 1
                caption, _ = self.parse_group(body, cursor)
                caption = re.sub(r"\\label\{[^}]+\}", "", caption).strip()

            images: list[tuple[str, str]] = []
            image_pattern = re.compile(
                r"\\includegraphics(?:\[([^]]*)\])?\{([^}]+)\}"
            )
            for options, source in image_pattern.findall(body):
                path = f"../figures/lecture-notes/{Path(source).stem}.svg"
                width = ""
                width_match = re.search(r"width=([0-9.]+)?\\(?:textwidth|linewidth)", options)
                if width_match:
                    factor = float(width_match.group(1) or "1")
                    width = f'{factor * 100:g}%'
                images.append((path, width))

            token = self.token("FIGURE")
            self.figure_tokens[token] = (identifier, images)
            return (
                f"\\par {token}BEGIN \\par\n"
                f"\\par {token}CAPTION {caption} \\par\n"
                f"\\par {token}END \\par"
            )

        return pattern.sub(replacement, text)

    def replace_environments(self, text: str) -> str:
        for environment, (prefix, fallback) in ENVIRONMENTS.items():
            pattern = re.compile(
                rf"\\begin\{{{environment}\}}"
                rf"\{{(?P<title>(?:[^{{}}]|\{{[^{{}}]*\}})*)\}}"
                rf"(?:\{{(?P<label>[^{{}}]*)\}})?"
                rf"(?P<body>.*?)"
                rf"\\end\{{{environment}\}}",
                flags=re.DOTALL,
            )

            def replacement(match: re.Match[str]) -> str:
                title = match.group("title").strip() or fallback
                legacy_label = (match.group("label") or "").strip()
                preferred = legacy_label or title
                identifier = self.unique_id(prefix, preferred)
                if legacy_label:
                    legacy_prefix = "ex" if prefix == "exm" else prefix
                    self.label_map[f"{legacy_prefix}:{legacy_label}"] = identifier
                token = self.token("BLOCK")
                self.block_tokens[token] = (identifier, title)
                return (
                    f"\\par {token}BEGIN \\par\n"
                    f"\\par {token}TITLE {title} \\par\n"
                    f"{match.group('body')}\n"
                    f"\\par {token}END \\par"
                )

            text = pattern.sub(replacement, text)
        return text

    def register_source_labels(self, text: str) -> None:
        for label in re.findall(r"\\label\{([^}]+)\}", text):
            if label in self.label_map:
                continue
            if label.startswith("fig:"):
                new = f"fig-{self.slug(label[4:])}"
            elif label.startswith("eq:"):
                new = f"eq-{self.slug(label[3:])}"
            else:
                tail = label.split(":", 1)[-1]
                new = f"sec-{self.slug(tail)}"
            self.label_map[label] = new

    def preprocess(self, text: str) -> str:
        text = self.replace_comments(text)
        self.register_source_labels(text)
        text = self.replace_figures(text)
        text = self.replace_environments(text)
        text = self.replace_recommendations(text)
        text = self.replace_todos(text)
        text = text.replace(r"\autocites", r"\cite")
        text = text.replace(r"\textalpha", "α")
        text = text.replace(r"\begin{displayquote}", r"\begin{quote}")
        text = text.replace(r"\end{displayquote}", r"\end{quote}")
        for source in re.findall(r"illustrations/([^}\]]+)", text):
            target = f"../figures/lecture-notes/{Path(source).stem}.svg"
            text = text.replace(f"illustrations/{source}", target)
        return MATH_MACROS + "\n" + text

    @staticmethod
    def pandoc(text: str) -> str:
        result = subprocess.run(
            [
                "pandoc",
                "--from=latex",
                "--to=markdown+tex_math_dollars+raw_tex",
                "--wrap=none",
            ],
            input=text,
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        if result.returncode:
            raise RuntimeError(result.stderr.strip())
        return result.stdout

    def replace_tokens(self, text: str) -> str:
        for token, (identifier, images) in self.figure_tokens.items():
            pattern = re.compile(
                rf"{token}BEGIN\s+{token}CAPTION\s+(.*?)\s+{token}END",
                flags=re.DOTALL,
            )
            match = pattern.search(text)
            if not match:
                continue
            caption = match.group(1).strip()
            if len(images) == 1:
                path, width = images[0]
                attributes = f"#{identifier}"
                if width:
                    attributes += f' width="{width}"'
                rendered = f"![{caption}]({path}){{{attributes}}}"
            else:
                image_lines = []
                for index, (path, width) in enumerate(images, start=1):
                    attributes = f'{{width="{width}"}}' if width else ""
                    image_lines.append(f"![Illustration panel {index}]({path}){attributes}")
                rendered = (
                    f"::: {{#{identifier} layout-ncol={len(images)}}}\n\n"
                    + "\n\n".join(image_lines)
                    + f"\n\n{caption}\n\n:::"
                )
            text = pattern.sub(lambda _match: rendered, text, count=1)

        for token, (identifier, _title) in self.block_tokens.items():
            text = re.sub(
                rf"(?:\\?\[?){token}BEGIN(?:\\?\]?)",
                f"::: {{#{identifier}}}",
                text,
            )
            text = re.sub(
                rf"(?:\\?\[?){token}TITLE\s+(.+?)(?:\\?\]?)$",
                r"## \1",
                text,
                flags=re.MULTILINE,
            )
            text = re.sub(
                rf"(?:\\?\[?){token}END(?:\\?\]?)",
                ":::",
                text,
            )

        for token, filename in self.recommendation_tokens.items():
            text = text.replace(f"{token}BEGIN", "::: {.recommended-reading}")
            image = (
                f"![](../figures/lecture-notes/recommended-reading/{filename})"
                f'{{.recommended-reading-cover fig-alt="Book or resource cover"}}\n\n:::'
            )
            text = text.replace(f"{token}END", image)

        for token, body in self.todo_tokens.items():
            body = body.replace("--", "—").replace("\n", " ").strip()
            text = text.replace(token, f"\n\n<!-- Legacy TODO: {body} -->\n\n")
        return text

    def clean_references(self, text: str) -> str:
        for old, new in sorted(self.label_map.items(), key=lambda item: -len(item[0])):
            text = text.replace(f"#{old}", f"#{new}")
            text = text.replace(f'reference="{old}"', f'reference="{new}"')
            text = text.replace(rf"\ref{{{old}}}", f"@{new}")
            text = text.replace(rf"\eqref{{{old}}}", f"@{new}")
            text = text.replace(rf"\label{{{old}}}", f"{{#{new}}}")

        reference = re.compile(
            r"\[\\\[.*?\\\]\]\(#[^)]+\)"
            r"\{reference-type=\"(?:ref|eqref)\" reference=\"([^\"]+)\"\}"
        )

        def replace_reference(match: re.Match[str]) -> str:
            legacy = match.group(1)
            target = self.label_map.get(legacy, legacy.replace(":", "-"))
            return f"@{target}"

        text = reference.sub(replace_reference, text)
        simple_reference = re.compile(
            r"\[[^]]+\]\(#[^)]+\)"
            r"\{reference-type=\"(?:ref|eqref)\" reference=\"([^\"]+)\"\}"
        )
        text = simple_reference.sub(replace_reference, text)
        text = re.sub(r"\[\]\{#([^ }]+)(?: [^}]*)?\}", r"{#\1}", text)
        text = re.sub(r"\{#(fig|eq|sec|chapter):([^} ]+)\}", r"{#\1-\2}", text)
        text = re.sub(
            r"\b(?:Figure|Fig\.|Equation|Eq\.|Chapter|Section|Sec\.|Definition|Theorem|Lemma|Example|Remark)\s+(@(?:fig|eq|sec|def|thm|lem|exm|rem)-[a-z0-9-]+)",
            r"\1",
            text,
        )
        return text

    @staticmethod
    def normalize_equation_labels(text: str) -> str:
        output: list[str] = []
        position = 0
        while True:
            start = text.find("$$", position)
            if start < 0:
                output.append(text[position:])
                break
            end = text.find("$$", start + 2)
            if end < 0:
                output.append(text[position:])
                break
            output.append(text[position:start])
            body = text[start + 2 : end]
            label_match = re.search(r"\{#(eq-[a-z0-9-]+)\}", body)
            if label_match:
                identifier = label_match.group(1)
                body = body[: label_match.start()] + body[label_match.end() :]
                output[-1] = output[-1].rstrip()
                output.append(f"\n\n$$\n{body.strip()}\n$$ {{#{identifier}}}\n\n")
            else:
                output.append(text[start : end + 2])
            position = end + 2
        return "".join(output)

    def clean(self, text: str) -> str:
        text = self.replace_tokens(text)
        text = self.clean_references(text)
        text = self.normalize_equation_labels(text)
        text = re.sub(
            r"\\text\{\\qquad\\textit\{([^{}]+)\}\}",
            r"\\qquad\\text{\1}",
            text,
        )
        text = text.replace(r"\textalpha", "α")
        text = text.replace(r"\ldots", r"\dots")
        text = text.replace(
            r"# The tools of calculus \[move/edit this material\]",
            "# The tools of calculus\n\n<!-- Legacy TODO: Move or edit this material. -->",
        )
        text = text.replace("## Move me", "## Continuity in finite dimensions")
        text = text.replace(
            "# Weak formulation of the Schrodinger equation",
            "# Weak formulation of the Schrödinger equation",
        )
        text = re.sub(r"\\\[([^\n]+?)\\\]", r"*\1*", text)
        text = re.sub(r"(?<=[A-Za-z0-9:;,.!?])\[@", " [@", text)
        text = text.replace(
            "@sec-functional-analysis",
            "[Functional analysis](../parts/functional-analysis.qmd)",
        )
        text = text.replace(
            "@sec-measure-and-integration",
            "[measure and integration theory](../parts/measure-and-integration.qmd)",
        )
        text = text.replace(
            "@sec-calculus",
            "[calculus and complex analysis](../parts/calculus-and-complex-analysis.qmd)",
        )
        text = text.replace("@sec-topology", "[topology](../parts/topology.qmd)")
        text = text.replace("@sec-prodrule", "the product-rule item above")
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n"


def heading_title(line: str) -> str:
    title = re.sub(r"\s*\{#[^}]+\}\s*$", "", line)
    title = title.lstrip("#").strip()
    return title.replace(r"\[", "[").replace(r"\]", "]")


def split_part(markdown: str) -> tuple[str, str, dict[str, str]]:
    lines = markdown.splitlines()
    chapter_index = next(i for i, line in enumerate(lines) if line.startswith("# "))
    part_heading = lines[chapter_index]
    section_indices = [
        i for i, line in enumerate(lines) if line.startswith("## ") and not line.startswith("### ")
    ]
    first_section = section_indices[0] if section_indices else len(lines)
    prelude = "\n".join(lines[chapter_index:first_section]).strip() + "\n"
    sections: dict[str, str] = {}
    for position, start in enumerate(section_indices):
        end = section_indices[position + 1] if position + 1 < len(section_indices) else len(lines)
        chunk = lines[start:end]
        title = heading_title(chunk[0])
        shifted: list[str] = []
        for line in chunk:
            match = re.match(r"^(#{2,6})(\s+.*)$", line)
            if match:
                line = "#" * (len(match.group(1)) - 1) + match.group(2)
            shifted.append(line)
        sections[title] = "\n".join(shifted).strip() + "\n"
    return heading_title(part_heading), prelude, sections


def copy_assets() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    READING_DIR.mkdir(parents=True, exist_ok=True)
    used_illustrations = (
        "geometric-complex.ai",
        "epsilon-ball.ai",
        "manhattan-euclidean.ai",
        "open-closed.ai",
        "limits.ai",
        "limits2.ai",
        "limits3.ai",
        "char-function.ai",
        "simple-function.ai",
        "func-approx-simple.ai",
        "bump.pdf",
        "projection.ai",
        "complex-domain.ai",
        "geometric-series-domain.ai",
        "smooth-curve.ai",
        "punctured-domain.ai",
    )
    for filename in used_illustrations:
        source = SOURCE_DIR / "illustrations" / filename
        target = FIGURE_DIR / f"{source.stem}.svg"
        subprocess.run(
            ["pdftocairo", "-svg", str(source), str(target)],
            check=True,
            cwd=ROOT,
        )

    reading_sources = (
        SOURCE_DIR / "images" / "Ciesielski-frontpage.png",
        SOURCE_DIR / "images" / "Fraleigh_frontpage.png",
        SOURCE_DIR / "images" / "Beezer_frontpage.png",
        SOURCE_DIR / "images" / "Halmos_finite_frontpage.jpg",
        SOURCE_DIR / "Bartle_frontpage.png",
        SOURCE_DIR / "images" / "bright_side_of_mathematics.png",
        SOURCE_DIR / "images" / "Kreyszig_frontpage.png",
        SOURCE_DIR / "images" / "Evans-frontpage.png",
        SOURCE_DIR / "images" / "Reed_Simon_frontpage.png",
        SOURCE_DIR / "images" / "Zeidler-frontpage.png",
        SOURCE_DIR / "images" / "Marsden_frontpage.png",
        SOURCE_DIR / "images" / "Busam_Freitag-frontpage.png",
        SOURCE_DIR / "images" / "Butkov-frontpage.png",
        SOURCE_DIR / "images" / "MathMajor_complex.png",
    )
    for source in reading_sources:
        filename = source.name.replace("_", "-")
        shutil.copy2(source, READING_DIR / filename)


def merge_bibliography() -> None:
    root_bib = ROOT / "references.bib"
    source = (SOURCE_DIR / "references.bib").read_text(encoding="utf-8").strip()
    existing = root_bib.read_text(encoding="utf-8").strip()
    marker = "% Entries imported from the 2024 lecture-note source"
    if marker in existing:
        existing = existing.split(marker, 1)[0].rstrip()
    root_bib.write_text(f"{existing}\n\n{marker}\n{source}\n", encoding="utf-8")


def write_outputs(force: bool) -> None:
    converter = Converter()
    CHAPTER_DIR.mkdir(exist_ok=True)
    PART_DIR.mkdir(exist_ok=True)

    written: list[Path] = []
    preprocessed: dict[str, str] = {}
    for part in PARTS:
        raw = (SOURCE_DIR / part.source).read_text(encoding="utf-8")
        preprocessed[part.source] = converter.preprocess(raw)

    if "ex:tdse" in converter.label_map:
        converter.label_map["example:tdse"] = converter.label_map["ex:tdse"]

    for part in PARTS:
        converted = converter.pandoc(preprocessed[part.source])
        part_title, prelude, sections = split_part(converted)

        part_path = PART_DIR / f"{part.slug}.qmd"
        written.append(part_path)
        if part_path.exists() and not force:
            raise FileExistsError(f"refusing to overwrite {part_path.relative_to(ROOT)}")
        part_path.write_text(converter.clean(prelude), encoding="utf-8")

        for source_title, filename in part.sections:
            if source_title not in sections:
                available = ", ".join(sections)
                raise KeyError(f"missing section {source_title!r}; available: {available}")
            target = CHAPTER_DIR / filename
            written.append(target)
            if target.exists() and not force:
                raise FileExistsError(f"refusing to overwrite {target.relative_to(ROOT)}")
            target.write_text(converter.clean(sections[source_title]), encoding="utf-8")

    about = (SOURCE_DIR / "about.tex").read_text(encoding="utf-8")
    about = converter.pandoc(converter.preprocess(about))
    about = converter.clean(about)
    (ROOT / "index.qmd").write_text(about, encoding="utf-8")

    copy_assets()
    merge_bibliography()
    print(f"wrote {len(written)} part/chapter files")
    print(f"converted {len(converter.block_tokens)} theorem-like blocks")
    print(f"converted {len(converter.recommendation_tokens)} reading callouts")
    print(f"preserved {len(converter.todo_tokens)} legacy TODO comments")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    write_outputs(args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
