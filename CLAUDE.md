# CLAUDE.md — om4mtools-python

Guidance for Claude Code (and any other agent) working in this repo.
This file is the condensed, enforceable version of the project's
design decisions. When in doubt, prefer what's written here over
inferring conventions from surrounding code.

## What this project is

Python library for fringe-pattern processing (OM4M group).

- **Distribution name** (PyPI / repo): `om4mtools-python` — avoids
  clashing with the sibling `om4mtools-matlab` project.
- **Importable package**: `om4mtools` — hyphens aren't valid in
  Python identifiers, so `pip install om4mtools-python` but
  `from om4mtools import Demodulator`. Same pattern as
  `beautifulsoup4` → `bs4`. Never rename the import package to match
  the distribution name, and never rename the distribution to match
  the import name.
- **Public API**: the four core classes — `Demodulator`, `Unwrapper`,
  `PathFollower`, `DisplayProjector` — are the primary, intended way
  to use this library: directly, from a script or a notebook.
- **CLI/GUI/web are optional convenience layers** on top of that same
  API — for people who'd rather run a command or click a button than
  write Python. Never design a feature so it only works through the
  CLI or GUI; it must work by importing the core class directly first.

## Hard rule: dependency direction

**`core/` never imports from `cli/`, `gui/`, or `web/`.** Interfaces
depend on core; core never depends on interfaces. `core/` must have
zero imports of Qt/PyQt, Typer, or FastAPI — nor of `pooch` or
`om4mtools.datasets` (core takes arrays; loading data is someone
else's job).

This is enforced by `tests/test_architecture.py` (an AST/import-graph
scan), not just convention — treat a violation there as a build
break, not a lint warning. Run it before considering any change to
`core/` complete.

## Directory layout

```
src/om4mtools/
├── core/          # pure algorithms, no I/O deps — Demodulator, Unwrapper,
│                  #   PathFollower, DisplayProjector
├── datasets.py    # [planned] ONLY place that knows data hosts/archives —
│                  #   fetch(), data_dir(); package level, never in core/
├── resources/     # SHIPPED — icons, default schemas,
│                  #   [planned, interim] registry.txt (archive hash + URL)
├── cli/           # tool-oriented (mirrors gui/), not one-per-class
│   └── <tool>/
│       ├── runner.py   # plain function(s), notebook-callable, no argparse/Typer
│       └── main.py     # Typer app; parses argv, calls runner
├── gui/
│   ├── common/qapp.py  # get_qapp() singleton — safe from script, notebook, or launcher
│   └── <tool>/
│       ├── widget.py    # pure QWidget, NO app bootstrap
│       └── launcher.py  # main() -> get_qapp() + show() + exec_()
└── web/
tests/
├── test_architecture.py   # import-graph check — core/ stays clean
├── unit/                  # core/ only — this is the `smoke` subset
├── integration/           # test_cli/, test_web, test_gui/
├── conftest.py            # [planned] --run-remote-data, small_dir/heavy_dir fixtures
└── data/                  # tiny committed fixtures only (size budget), not shipped
tools/                     # [planned] dev-only scripts, e.g. build_data_archive.py
benchmarks/                # asv perf regression suite for core/
.binder/                   # env spec so examples/notebooks/ run on Binder
docs/                      # Sphinx source — conf.py, index.md, api/, guide/
docs/api/                  # autosummary generates one page per public class
examples/                  # demo notebooks/scripts — NOT shipped, excluded from sdist/wheel
```

Two tools currently modeled this way: `imageviewer`, `fringeprocessor`.
**Same tool, two skins, three entry points**: `runner.py`/`widget.py`
hold the logic; `main.py`/`launcher.py` are thin standalone wrappers.
When adding a new tool, follow this exact split — don't put argv
parsing or Qt bootstrap logic in the notebook-callable file.

**No `io/` subpackage for now**: image reading/writing goes straight
through OpenCV (`cv2.imread`/`cv2.imwrite`) at the point of use — in
`cli/<tool>/runner.py`, `gui/<tool>/widget.py`, or `web/` — not through
a shared loader wrapper. `core/` still never does file I/O itself. If
enough duplicated OpenCV boilerplate accumulates across tools, revisit
this and reintroduce `io/` at that point.

**Packaging discipline**: anything in the wheel lives under
`src/om4mtools/resources/`. `examples/` and `tests/data/` stay outside
`src/` and are excluded from sdist/wheel in `pyproject.toml`. Check
this whenever adding new data files.

**Optional extras** — `pip install om4mtools-python` alone must only
pull in `core` plus its direct dependencies (numpy, scipy, OpenCV):

```toml
[project.optional-dependencies]
gui = ["PyQt6", "pyqtgraph"]
web = ["fastapi", "uvicorn"]
cli = ["typer", "rich"]
data = ["pooch>=1.8"]          # [planned] om4mtools.datasets; also in dev deps
all = ["om4mtools-python[gui,web,cli,data]"]
```

Never add a GUI/CLI/web dependency to the base `[project.dependencies]`
— it belongs in the matching extra.

## Test & example data

Full spec: **`docs/dev/test_and_example_data.md`** — read it before
touching test data, `datasets.py`, `registry.txt`, `conftest.py`, the
data CI steps, or example data loading. Status (2026-09-30): **adopted,
not yet implemented** — implementation steps are in `TODO.md`. Until
`datasets.py` lands, the legacy `download_data_fixtures.sh` still
exists; don't extend it, it gets retired.

The model in brief:

- **Large binaries never live in git.** Heavy data goes into a few
  **versioned zip bundles** (`small` → `fringe_small_vN.zip`, `heavy` →
  `fringe_heavy_vN.zip`), files at the zip root, fetched on demand by
  `om4mtools.datasets` (Pooch), each pinned by a sha256 hash, cached in
  `pooch.os_cache("om4mtools")` (override: `OM4MTOOLS_DATA_DIR`).
- **Hosting:** interim = Dropbox, one read-only link per *archive*
  (never a folder link — Dropbox re-zips folders, hash isn't stable),
  listed in `src/om4mtools/resources/registry.txt`. Target = Zenodo,
  registry read from the DOI; only `datasets.py` changes on migration.
  Not used: Git LFS, DVC.
- **Published archives are immutable.** Any data change → new archive
  name (`_v2`, …), registered in the same commit that needs it. Bundle
  sources live outside the repo (`om4mtools-data/<bundle>/`) and are
  built with `tools/build_data_archive.py`.
- **Test tiers:** `smoke` (offline, synthetic or tiny `tests/data/`
  files; `develop` gate) → regular unmarked (offline) →
  `@pytest.mark.remote_data` (uses bundles; skipped unless
  `--run-remote-data`; runs in `full-suite` on `main` with a cached
  data dir).
- **Synthetic first**: prefer generated fringes with known ground truth
  (`I = a + b·cos(φ)`) over real scans; real scans are for
  regression/realism.
- **`tests/data/` size budget:** ≤ 500 kB per file, ≤ 5 MB total.
  Document each fixture's provenance next to it (see
  `tests/data/peaks_49x50.m`).

Hard rules for agents:

- Never commit a binary > 500 kB or break the `tests/data/` /
  `examples/data/` budget — propose adding it to a bundle instead.
- Never hardcode dataset URLs, hashes, or archive names outside
  `datasets.py` / `registry.txt`.
- A test is never both `smoke` and `remote_data`; `smoke` tests never
  touch the network or a bundle.
- Tests reach bundles only through the session fixtures `small_dir` /
  `heavy_dir` + `parametrize` over file names — no per-file fixtures, no
  direct `fetch()`/`pooch` calls in tests.
- Examples/notebooks load data via `om4mtools.datasets.fetch` /
  `data_dir` — no hardcoded URLs or absolute local paths.
- `core/` never imports `pooch` or `om4mtools.datasets` (enforced by
  `tests/test_architecture.py` alongside the Qt/Typer/FastAPI rule —
  add the `pooch`/`datasets` check there when `datasets.py` lands).
- Never edit a hash in `registry.txt` to make a failing download pass —
  a mismatch means the upstream archive changed; investigate and report.
- Never modify/overwrite a published archive, and never rebuild one
  after publishing (rebuilding changes the hash).

## Coding style (PEP 8)

- 4 spaces, never tabs. Line length: pick 79 or a team-agreed longer
  limit (e.g. 99) and enforce it with `ruff format`/`black` — don't
  hand-wrap.
- Naming: modules `lowercase_with_underscores`; classes `CapWords`;
  functions/vars `lowercase_with_underscores`; constants
  `UPPER_CASE`; internal/non-public single leading underscore
  (`_helper`, future `core/_math_utils.py`); class-private double
  leading underscore; exceptions end in `Error` (e.g. `UnwrapError`).
- **The four core classes are always public** — never
  underscore-prefix `Demodulator`, `Unwrapper`, `PathFollower`, or
  `DisplayProjector`, and always re-export them plainly from
  `core/__init__.py` and the top-level `__init__.py`.
- One import per line; stdlib, then third-party, then local, each
  group blank-line separated; no wildcard imports.
- Two blank lines around top-level defs/classes, one around methods.
- Compare to `None` with `is`/`is not`; prefer `isinstance()` over
  direct type comparison; use `with` for resource/app lifecycles.
- **Type hints required** on all public functions/methods, especially
  `core/` and `cli/*/runner.py` (the notebook-facing surface).
- **Docstrings required** on all public classes/functions — `docs/api/`
  is built from them; an undocumented public symbol is an incomplete
  change.
- Lint/format via `ruff` and `black` (or `ruff format`) — run these,
  don't rely on manual formatting review.

## Branching & CI — what this means for how you commit

Two branches: `develop` (default, everyday integration) and `main`
(protected — no direct pushes/force-pushes/deletion, updated only via
PR from `develop` or a `hotfix/*` branch).

- **Trivial changes** (docs, tiny fixes): push directly to `develop`.
- **Feature work**: branch `feature/xyz` off `develop`, PR into
  `develop`. Required check: `smoke` — `pytest -m smoke --no-cov`
  (core/ unit tests only, fast).
- **Release**: PR `develop → main`. Required check: `full-suite` —
  full `pytest --cov` + docs build. Bump the version in
  `pyproject.toml` as part of this PR (the tag step on merge reads it
  and is a no-op if the tag exists, so don't skip the bump).
- **Hotfix**: branch `hotfix/xyz` from `main`, PR into `main` (same
  `full-suite` gate). After merge, back-merge `main → develop` via PR
  with a **real merge commit, not squash** — squashing here silently
  drops the hotfix from the next `develop`-cut release.

When adding tests for `core/`, mark fast, dependency-free ones
`@pytest.mark.smoke` so they run in the `develop` gate; integration
tests under `cli`/`gui`/`web` stay out of `smoke`. Tests that need
downloaded bundles are `@pytest.mark.remote_data` instead — they only
run in `full-suite` (`pytest --cov --run-remote-data`) or locally with
`--run-remote-data`. See "Test & example data".

## Documentation (Sphinx)

**Tool: Sphinx** — not MkDocs. Follows the numpy/scipy/scikit-image/napari ecosystem
convention; `autodoc`/`autosummary` are Sphinx-native and better suited to a
class-reference-heavy library than mkdocstrings.

```
docs/
├── conf.py
├── index.md          # MyST Markdown entry point
├── api/              # autosummary — one page per public class, generated
└── guide/            # quickstart, cli, gui, web guides — authored in .md
```

```python
# conf.py essentials
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",  # NumPy/Google-style docstrings
    "myst_parser",  # write guide pages in Markdown, not .rst
    "nbsphinx",  # render examples/notebooks/ directly
]
autosummary_generate = True
html_theme = "pydata_sphinx_theme"
```

- Guide pages go in `docs/guide/` as `.md` (MyST) — no forced `.rst`.
- Example notebooks in `examples/` are rendered via `nbsphinx` with the
  `.binder/` launch button.
- The `full-suite` CI gate includes a docs build (`make html` must pass clean).

## Design decisions

**Parameter dataclasses use `@dataclass(slots=True)`** — e.g. `DemodParams`,
and any future `*Params` class. `slots=True` prevents silent dynamic attribute
creation, so a typo like `p.n_intgrams = 5` (instead of `p.n_integrams`) raises
`AttributeError` immediately rather than creating a phantom field that gets
silently ignored. Always use `slots=True` on parameter/config dataclasses.

**`DemodParams.delta_list` is typed as `tuple` (variable-length), not `list`.**
Tuples are immutable, so once a `DemodParams` is constructed the sequence of
phase shifts cannot be modified in-place — a caller must create a new
`DemodParams` to change it. This is intentional: it prevents accidental
mid-run mutation. The contents of `delta_list` (length, value ranges, etc.)
are validated by `_validate()` at construction time. Any future sequence-valued
field in a `*Params` class should follow the same pattern unless mutability is
explicitly required.

**All parameter validation is delegated to `DemodParams` (and equivalent `*Params`
classes), never to the core class itself.** Two levels:

- `_validate()` — called from `__post_init__`; validates each field individually
  at construction time, and normalizes field values when needed (e.g. converting
  an acceptable input form into the canonical internal representation).
- `verify_params()` — called by `Demodulator.process()` (and equivalent entry
  points) just before execution; checks cross-field constraints and
  algorithm-level preconditions.

`Demodulator` (and other core classes) must not duplicate or shadow this logic.
If a new validation rule is needed, it goes in `*Params`, not in the core class.

**Type aliases for NumPy arrays** — defined once and reused across `core/`:

```python
import numpy.typing as npt
import numpy as np
from typing import Any

FloatArray = npt.NDArray[np.floating[Any]]  # float32, float64, …
RealArray = npt.NDArray[np.integer[Any] | np.floating[Any]]  # uint8, uint16, float64, …
ComplexArray = npt.NDArray[np.complex128]
```

- **`RealArray`** is the correct input type for `process()` — callers may pass
  raw camera frames (uint8/uint16) or synthetic igrams (float64). `process()`
  converts internally with `np.asarray(ig, dtype=np.float64)`, which is a no-op
  when the array is already float64.
- **`FloatArray`** is for intermediate or output arrays that are guaranteed to be
  floating-point. Do not use it for public method inputs that accept camera data.
- Never use `NDArray[np.float64]` for inputs — it rejects float32 and integers.

**Use `Sequence` (not `list`) for read-only sequence inputs in public methods.**
`list` is invariant in type checkers: a `list[NDArray[np.float64]]` is not
accepted where `list[NDArray[np.floating[Any]]]` is expected, even though
`float64` is a floating type. `collections.abc.Sequence` is covariant, so the
type checker accepts any compatible element type. It also lets callers pass a
tuple or any other sequence, not just a list. Rule: if a method only reads a
sequence argument, type it as `Sequence[T]`; reserve `list[T]` for outputs or
arguments the method mutates.

Example: `Demodulator.process(self, igram_list: Sequence[RealArray]) -> list[ComplexArray]`

**Core classes do NOT implement `__setattr__`/`__getattr__` to proxy their
`*Params` objects.** The canonical access pattern is explicit:
`demodulator.demod_params.some_param`. Adding `__setattr__`/`__getattr__`
forwarding would not remove `.demod_params` access (both paths would coexist),
and would create confusion about which attributes belong to the class vs. the
params object. Do not add this forwarding to `Demodulator` or any other core class.

## Before finishing any change

1. If you touched `core/`, run `tests/test_architecture.py` and
   confirm no forbidden imports crept in.
2. Run `ruff` + `black`/`ruff format`.
3. Confirm public functions/classes you added or changed still have
   type hints and docstrings.
4. If you added a new tool under `cli/` or `gui/`, confirm it follows
   the `runner.py`/`widget.py` (logic) vs `main.py`/`launcher.py`
   (bootstrap) split.
5. If you added shippable data, confirm it's under
   `src/om4mtools/resources/`, not `examples/` or `tests/data/`.
6. If you added or changed test/example data, confirm the
   `tests/data/` size budget (≤ 500 kB/file, ≤ 5 MB total), that no
   URL/hash/archive name lives outside `datasets.py`/`registry.txt`,
   and that `remote_data` tests pass with `pytest --run-remote-data`.
