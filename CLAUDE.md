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
zero imports of Qt/PyQt, Typer, or FastAPI.

This is enforced by `tests/test_architecture.py` (an AST/import-graph
scan), not just convention — treat a violation there as a build
break, not a lint warning. Run it before considering any change to
`core/` complete.

## Directory layout

```
src/om4mtools/
├── core/          # pure algorithms, no I/O deps — Demodulator, Unwrapper,
│                  #   PathFollower, DisplayProjector
├── resources/     # SHIPPED — icons, default schemas
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
└── data/                  # small synthetic fixtures, not shipped
benchmarks/                # asv perf regression suite for core/
.binder/                   # env spec so examples/notebooks/ run on Binder
docs/api/                  # autodoc/autosummary from docstrings
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
all = ["om4mtools-python[gui,web,cli]"]
```

Never add a GUI/CLI/web dependency to the base `[project.dependencies]`
— it belongs in the matching extra.

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
tests under `cli`/`gui`/`web` stay out of `smoke`.

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
