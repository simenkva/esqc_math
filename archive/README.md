# Archived migration tooling

This directory preserves the scripts and test used to migrate the 2024 LaTeX
exercise collection into the Quarto book. The migration is complete, so these
files are not part of routine book maintenance.

- `scripts/migrate_legacy.py` records the one-time conversion. Its `--force`
  option would overwrite the reviewed chapter files.
- `scripts/update_recommendations.py` implements the retired generated-list
  system.
- `scripts/audit_book.py` implements the migration-specific structural audit
  and depends on the retired recommendation generator.
- `tests/test_update_recommendations.py` tests that generator.

Keep these files for migration history. The next recommendation system can be
designed independently of them.

The lecture-note migration added a separate reproducible pair of tools:

- `scripts/migrate_lecture_notes.py` converts the active content included by
  `ESQC2024_maths.tex`, creates the Quarto part and chapter files, converts the
  PDF-compatible Illustrator figures to SVG, and imports the bibliography.
- `scripts/audit_lecture_notes.py` checks the configured file tree, semantic
  block counts, callouts, figures, identifiers, references, image paths, and
  legacy-LaTeX artifacts.

Run them from the project root with:

```sh
python3 archive/scripts/migrate_lecture_notes.py --force
python3 archive/scripts/audit_lecture_notes.py
quarto render
```
