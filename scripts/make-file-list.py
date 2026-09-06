import argparse
from fnmatch import fnmatch
from pathlib import Path

EXCLUDED_PATTERNS = (
    ".DS_Store",
    "~$*",
    "*.tmp",
    "*.temp",
    "*.swp",
    "*.swo",
    "*~",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a Markdown file list.")
    parser.add_argument(
        "-f",
        "--folder",
        type=Path,
        default=Path("lectures"),
        help="folder whose files should be listed (default: %(default)s)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("lecture-file-list.md"),
        help="output Markdown filename (default: %(default)s)",
    )
    args = parser.parse_args()

    if not args.folder.is_dir():
        parser.error(f"folder does not exist or is not a directory: {args.folder}")

    return args


def main() -> None:
    args = parse_args()
    print(f"Generating file list: folder='{args.folder}', output='{args.output}'")
    lines = []

    for path in sorted(args.folder.iterdir()):
        if path.is_file() and not any(
            fnmatch(path.name, pattern) for pattern in EXCLUDED_PATTERNS
        ):
            lines.append(f"- [{path.name}]({path.as_posix()})")

    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
