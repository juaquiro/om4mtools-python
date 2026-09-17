## Summary

<!-- What does this PR do, and why? -->

## Type of change

- [ ] Feature work → `develop` (gated on `smoke`)
- [ ] Release → `main` from `develop` (gated on `full-suite`; bump `version` in `pyproject.toml`)
- [ ] Hotfix → `main` from `hotfix/*` (gated on `full-suite`; back-merge `main → develop` after, with a real merge commit — not squash)

## Checklist

- [ ] If `core/` was touched, `tests/test_architecture.py` passes (no forbidden imports)
- [ ] `ruff` and `black`/`ruff format` pass
- [ ] New/changed public functions and classes have type hints and docstrings
- [ ] New `cli/`/`gui/` tools follow the `runner.py`/`widget.py` vs `main.py`/`launcher.py` split
- [ ] New shippable data lives under `src/om4mtools/resources/`, not `examples/` or `tests/data/`
- [ ] New `core/` tests are marked `@pytest.mark.smoke` if fast and dependency-free
