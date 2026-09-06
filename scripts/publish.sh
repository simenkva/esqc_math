#!/usr/bin/env bash

set -Eeuo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"

WEBSITE_DIR="$REPO_ROOT/website"
WEBSITE_BUILD="$WEBSITE_DIR/_site"
LECTURE_NOTES_DIR="$REPO_ROOT/lecture_notes"
LECTURE_NOTES_BUILD="$LECTURE_NOTES_DIR/docs"
LECTURES_DIR="$REPO_ROOT/lectures"
NOTEBOOKS_DIR="$REPO_ROOT/notebooks"
OUTPUT_DIR="$REPO_ROOT/docs"
QUARTO_CANVAS_DIR="${QUARTO_CANVAS_DIR:-$REPO_ROOT/../quarto-canvas}"
CANVAS_EXTENSION_DIR="${QUARTO_CANVAS_EXTENSION:-$QUARTO_CANVAS_DIR/extension}"

die() {
  printf 'publish: error: %s\n' "$*" >&2
  exit 1
}

require_directory() {
  [[ -d "$1" ]] || die "required directory not found: $1"
}

require_file() {
  [[ -f "$1" ]] || die "required file not found: $1"
}

command -v quarto >/dev/null 2>&1 || die "quarto is not installed or not on PATH"
command -v rsync >/dev/null 2>&1 || die "rsync is not installed or not on PATH"
command -v python >/dev/null 2>&1 || die "python is not installed or not on PATH"

require_directory "$WEBSITE_DIR"
require_directory "$LECTURE_NOTES_DIR"
require_directory "$LECTURES_DIR"
require_directory "$NOTEBOOKS_DIR"
require_directory "$REPO_ROOT/obsidian"
require_directory "$CANVAS_EXTENSION_DIR"
require_file "$REPO_ROOT/canvas_publish.yml"
require_file "$REPO_ROOT/scripts/make-file-list.py"

# Prefer an explicit override, then PATH, then the usual sibling checkout.
if [[ -n "${OBSIDIAN_CANVAS_QUARTO:-}" ]]; then
  CANVAS_CLI="$OBSIDIAN_CANVAS_QUARTO"
elif command -v obsidian-canvas-quarto >/dev/null 2>&1; then
  CANVAS_CLI="$(command -v obsidian-canvas-quarto)"
else
  CANVAS_CLI="$QUARTO_CANVAS_DIR/.venv/bin/obsidian-canvas-quarto"
fi

[[ -x "$CANVAS_CLI" ]] || die \
  "obsidian-canvas-quarto is unavailable; install it, put it on PATH, or set OBSIDIAN_CANVAS_QUARTO"

# Keep staging on the same filesystem as docs/ so the final replacement is a
# rename rather than a partially visible copy.
STAGING_DIR="$(mktemp -d "$REPO_ROOT/.publish.XXXXXX")"
ASSEMBLED_SITE="$STAGING_DIR/docs"
BACKUP_DIR="$STAGING_DIR/previous-docs"

cleanup() {
  local exit_status=$?

  # If the process is interrupted during the final two renames, put the old
  # publication back before removing the staging directory.
  if [[ ! -e "$OUTPUT_DIR" && -e "$BACKUP_DIR" ]]; then
    if ! mv -- "$BACKUP_DIR" "$OUTPUT_DIR"; then
      printf 'publish: error: could not restore docs/; recovery files are in %s\n' \
        "$STAGING_DIR" >&2
      trap - EXIT
      exit 1
    fi
  fi

  # Guard the recursive removal in case a variable is accidentally changed.
  case "$STAGING_DIR" in
    "$REPO_ROOT"/.publish.*) rm -rf -- "$STAGING_DIR" ;;
  esac

  return "$exit_status"
}
trap cleanup EXIT

printf 'publish: installing the current quarto-canvas extension\n'
(
  cd -- "$WEBSITE_DIR"
  quarto add "$CANVAS_EXTENSION_DIR" --no-prompt
)

printf 'publish: generating website content from the Obsidian vault\n'
(
  cd -- "$WEBSITE_DIR"
  "$CANVAS_CLI" build \
    --vault "$REPO_ROOT/obsidian" \
    --output generated-vault \
    --config "$REPO_ROOT/canvas_publish.yml"
)

printf 'publish: generating lecture and notebook file lists\n'
(
  cd -- "$REPO_ROOT"
  python scripts/make-file-list.py -f lectures -o website/lectures-file-list.md
  python scripts/make-file-list.py -f notebooks -o website/notebooks-file-list.md
)

printf 'publish: rendering website\n'
quarto render "$WEBSITE_DIR"
require_file "$WEBSITE_BUILD/index.html"

printf 'publish: rendering lecture notes\n'
quarto render "$LECTURE_NOTES_DIR"
require_file "$LECTURE_NOTES_BUILD/index.html"

printf 'publish: assembling docs/\n'
mkdir -p -- \
  "$ASSEMBLED_SITE/lecture_notes" \
  "$ASSEMBLED_SITE/lectures" \
  "$ASSEMBLED_SITE/notebooks"
cp -R -- "$WEBSITE_BUILD"/. "$ASSEMBLED_SITE"/
cp -R -- "$LECTURE_NOTES_BUILD"/. "$ASSEMBLED_SITE/lecture_notes"/
rsync -a \
  --exclude='.DS_Store' \
  --exclude='~$*' \
  --exclude='*.tmp' \
  --exclude='*.temp' \
  --exclude='*.swp' \
  --exclude='*.swo' \
  --exclude='*~' \
  "$LECTURES_DIR"/ "$ASSEMBLED_SITE/lectures"/
rsync -a \
  --exclude='.DS_Store' \
  --exclude='~$*' \
  --exclude='*.tmp' \
  --exclude='*.temp' \
  --exclude='*.swp' \
  --exclude='*.swo' \
  --exclude='*~' \
  "$NOTEBOOKS_DIR"/ "$ASSEMBLED_SITE/notebooks"/

# Tell GitHub Pages to serve Quarto's generated files without Jekyll processing.
touch "$ASSEMBLED_SITE/.nojekyll"

# Preserve the previous publication until both projects are built and staged.
if [[ -e "$OUTPUT_DIR" ]]; then
  mv -- "$OUTPUT_DIR" "$BACKUP_DIR"
fi

if ! mv -- "$ASSEMBLED_SITE" "$OUTPUT_DIR"; then
  if [[ -e "$BACKUP_DIR" ]]; then
    if ! mv -- "$BACKUP_DIR" "$OUTPUT_DIR"; then
      trap - EXIT
      die "could not install the new site or restore the previous one; recovery files are in $STAGING_DIR"
    fi
  fi
  die "could not install the assembled site"
fi

printf 'publish: complete: %s\n' "$OUTPUT_DIR"
