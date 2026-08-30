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
