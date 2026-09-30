# tests/data

Tiny committed fixtures used by tests. Not shipped in the sdist/wheel —
see the packaging discipline note in `CLAUDE.md`.

Rules (full spec: `docs/dev/test_and_example_data.md`):

- **Size budget:** each file ≤ 500 kB, whole folder ≤ 5 MB. Anything
  bigger goes into a versioned data bundle fetched via
  `om4mtools.datasets`, never into git.
- **Prefer synthetic data** generated in code with known ground truth;
  commit a file here only when that's impractical.
- **Document provenance** next to each fixture — e.g. the script that
  generated it (`peaks_49x50.m` → `peaks_49x50.csv`).
- Files here are usable by `smoke` tests (offline, no network).
