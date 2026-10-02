# om4mtools-python

Python library for fringe-pattern processing (OM4M group).

`pip install om4mtools-python`, `from om4mtools import Demodulator` — same
naming pattern as `beautifulsoup4` → `bs4`.

## Install

```bash
pip install om4mtools-python          # core only (OpenCV used directly for I/O)
pip install "om4mtools-python[cli]"   # + command-line tools
pip install "om4mtools-python[gui]"   # + PyQt6 desktop tools
pip install "om4mtools-python[web]"   # + FastAPI web layer
pip install "om4mtools-python[all]"   # everything
```

## Usage

The four core classes are the primary, intended way to use this library —
directly, from a script or a notebook:

```python
from om4mtools import Demodulator, Unwrapper

wrapped = Demodulator(carrier_frequency=(0.1, 0.0)).demodulate(image)
phase = Unwrapper().unwrap(wrapped)
```

The CLI (`om4m-imageviewer`, `om4m-fringeprocessor`), GUI, and web layers are
optional convenience wrappers around the same API.

## Development

See [CLAUDE.md](CLAUDE.md) for the full set of project conventions
(directory layout, dependency direction, branching model, coding style).

```bash
pip install -e ".[dev]"
pytest -m smoke --no-cov   # fast core/ tests — the develop PR gate
pytest --cov               # full suite — the main PR gate
pytest --run-remote-data   # also run tests that download data bundles
ruff check .
black --check .
```

Large test/example data is not in git: it's fetched on demand from
versioned bundles via `om4mtools.datasets` — see
[docs/dev/test_and_example_data.md](docs/dev/test_and_example_data.md)
(adopted, implementation in progress).

### Branching

- `develop` (default): everyday integration. Trivial changes push directly;
  feature work goes through a `feature/xyz` branch and a PR gated on the
  `smoke` check.
- `main` (protected): releases only, via PR from `develop` (or `hotfix/*`),
  gated on the `full-suite` check. Bump the version in `pyproject.toml` as
  part of the release PR.

### Editor settings (VS Code)

Settings are split into three layers — keep each thing in its layer:

| Layer | Where | What goes there |
|---|---|---|
| **Rules** (source of truth) | `pyproject.toml` (`[tool.ruff]`) | Line length, lint rule selection. Used by the CLI, CI, and every editor. |
| **Workspace** (shared, committed) | `.vscode/settings.json`, `.vscode/extensions.json` | Editor wiring only: Ruff as formatter, format/fix/sort imports on save; recommended extensions. |
| **User** (personal, not committed) | VS Code User settings (`Ctrl+Shift+P` → *Preferences: Open User Settings (JSON)*) | Theme, fonts, auto-save, environment manager (conda/venv/uv), interpreter paths. |

Rules for the committed workspace files:

- No lint/format rules — they live in `pyproject.toml` only, so there's a
  single source of truth.
- No absolute paths, interpreter paths, or personal preferences.
- Only `settings.json` and `extensions.json` are tracked; everything else in
  `.vscode/` is git-ignored (`.vscode/*` + `!` exceptions in `.gitignore`).

To share personal settings across your own machines, use VS Code
**Settings Sync** (with the *Settings* category enabled), not git.

Format-on-save does not run on delayed auto-save (`files.autoSave:
"afterDelay"`); save explicitly or use `"onFocusChange"`. CI/`ruff` remains
the actual enforcement — editor settings are a convenience.

## License

BSD 3-Clause — see [LICENSE](LICENSE).
