# Test & Example Data — design spec

> **Status (2026-09-30): adopted, not yet implemented.** This is the
> agreed model for test/example data. Until the pieces below land
> (`datasets.py`, `registry.txt`, `tests/conftest.py`,
> `tools/build_data_archive.py`), the legacy `download_data_fixtures.sh`
> still exists; it is retired once `datasets.py` lands. Implementation
> steps are tracked in `TODO.md`. The enforceable summary lives in
> `CLAUDE.md` ("Test & example data"); this file is the full reference.
>
> Not part of the Sphinx build (the docs build is `.rst`-only for now).

**Core principle: large binaries never live in git.** Heavy test/example
data is bundled into a **few versioned archives** (not dozens of loose
files), hosted externally, and fetched on demand through a single module,
`om4mtools.datasets`, built on [Pooch](https://www.fatiando.org/pooch/).
Each archive is pinned by a hash, so a download that doesn't match fails
loudly instead of producing mysterious test failures. The archive is
downloaded once, unpacked once into the local cache, and then reused.

## 1. Bundles

Data is split by purpose into bundles, each one a zip archive:

| Bundle | Archive (example) | Contents | Used by |
|---|---|---|---|
| `small` | `fringe_small_v1.zip` | Few-MB real scans for quick realism checks | `remote_data` tests, notebooks |
| `heavy` | `fringe_heavy_v1.zip` | Large scans for regression/performance | `remote_data` tests, `benchmarks/` |

Add a bundle only when a group of files has a clearly different audience or
size. Two or three bundles are enough; more defeats the purpose.

**Archive layout:** files sit at the **root** of the zip (build it from
inside the folder, see 5.7), so `fetch("scan_01.tif", bundle="small")`
maps directly to a file name. Subfolders are allowed and are addressed as
`"subdir/scan_01.tif"`.

**Versioning rule:** a published archive is never modified. Any change
(add, fix, remove a file) produces a **new archive name** with the version
bumped (`fringe_small_v2.zip`), registered in the same commit that needs it.
Old and new versions coexist in the cache, and old releases of
`om4mtools-python` keep passing their tests.

The source of truth for bundle contents is a local folder kept **outside
the repo** (e.g. `om4mtools-data/small/`, `om4mtools-data/heavy/`), from
which archives are built.

## 2. Hosting — two phases

| Phase | Host | Registry | Notes |
|---|---|---|---|
| **Interim (current)** | Dropbox, read-only link per archive | `resources/registry.txt`, one line per archive with hash + Dropbox URL | Links verified read-only (download only). One link per archive, not per file. |
| **Target** | Zenodo record (new version per data change) | None to maintain: file list and checksums read from the DOI via `load_registry_from_doi()` | Immutable, free up to 50 GB/record, DOI per version, citable in OM4M papers. |

Not used: Git LFS (bandwidth quotas hurt CI), DVC (tooling burden),
Dropbox *folder* links with `?dl=1` (Dropbox zips folders on the fly, so
the hash isn't stable — always upload an archive built locally).

Moving from interim to target changes only `datasets.py` (5.4). Tests,
fixtures, notebooks, and examples stay the same, because they only use
`fetch()` and `data_dir()`.

## 3. Layout additions

```
src/om4mtools/
├── datasets.py              # the ONLY place that knows hosts/archives; fetch(), data_dir()
└── resources/
    └── registry.txt         # interim only: "archive sha256:hash url" — tiny, shipped
tests/
├── conftest.py              # --run-remote-data option, auto-skip, bundle fixtures
└── data/                    # tiny committed fixtures only (see size budget)
tools/
└── build_data_archive.py    # zip a bundle folder + print its registry line (not shipped)
```

- `datasets.py` sits at package level, **not** in `core/`. `core/` must
  never import `datasets` or `pooch` (checked in
  `tests/test_architecture.py` alongside the Qt/Typer/FastAPI rule).
  `core/` takes arrays; loading is somebody else's job.
- Optional extra in `pyproject.toml`, included in `all` and in the
  test/dev dependencies:

  ```toml
  [project.optional-dependencies]
  data = ["pooch>=1.8"]
  all  = ["om4mtools-python[gui,web,cli,data]"]
  ```

- `.binder/environment.yml` includes `pooch` so notebooks can fetch data.

## 4. `om4mtools.datasets`

**Interim (Dropbox + `registry.txt`):**

```python
"""Download-on-demand access to om4mtools test and example datasets."""

from importlib.resources import files
from pathlib import Path

BUNDLES = {
    "small": "fringe_small_v1.zip",
    "heavy": "fringe_heavy_v1.zip",
}

_FETCHER = None


def _get_fetcher():
    global _FETCHER
    if _FETCHER is None:
        try:
            import pooch
        except ImportError as exc:
            raise ImportError(
                "Datasets require pooch: pip install om4mtools-python[data]"
            ) from exc
        _FETCHER = pooch.create(
            path=pooch.os_cache("om4mtools"),
            base_url="",  # every archive has its own URL in registry.txt
            registry=None,
            env="OM4MTOOLS_DATA_DIR",  # override cache dir (CI, shared lab disk)
        )
        registry = files("om4mtools.resources").joinpath("registry.txt")
        with registry.open() as f:
            _FETCHER.load_registry(f)
    return _FETCHER


def data_dir(bundle: str = "small") -> Path:
    """Download and unpack ``bundle`` (once); return its local folder."""
    import pooch

    archive = BUNDLES[bundle]
    fetcher = _get_fetcher()
    fetcher.fetch(archive, processor=pooch.Unzip())
    return Path(fetcher.abspath) / f"{archive}.unzip"


def fetch(name: str, bundle: str = "small") -> str:
    """Return a local path to file ``name`` inside ``bundle``."""
    path = data_dir(bundle) / name
    if not path.exists():
        raise FileNotFoundError(f"{name!r} not found in bundle {bundle!r}")
    return str(path)
```

`registry.txt` (one line per archive; append `?dl=1` so Dropbox serves the
raw file):

```
fringe_small_v1.zip  sha256:ab12...  https://www.dropbox.com/scl/fi/.../fringe_small_v1.zip?rlkey=...&dl=1
fringe_heavy_v1.zip  sha256:cd34...  https://www.dropbox.com/scl/fi/.../fringe_heavy_v1.zip?rlkey=...&dl=1
```

**Target (Zenodo) — only `_get_fetcher()` changes:**

```python
        _FETCHER = pooch.create(
            path=pooch.os_cache("om4mtools"),
            base_url="doi:10.5281/zenodo.XXXXXXX/",  # the version's DOI
            registry=None,
            env="OM4MTOOLS_DATA_DIR",
        )
        _FETCHER.load_registry_from_doi()  # file list + checksums from Zenodo
```

`registry.txt` is then deleted. Upgrading data = new Zenodo version + new
DOI + new archive names in `BUNDLES`, all in one commit.

## 5. Test tiers

| Tier | Marker | Data source | Network | Runs in |
|---|---|---|---|---|
| **Smoke** | `@pytest.mark.smoke` | Synthetic fixtures generated in code, or tiny files in `tests/data/` | **Never** | `smoke` (PR/push → `develop`), local default |
| **Regular** | (none) | Same as smoke | Never | `full-suite`, local `pytest` |
| **Heavy / remote** | `@pytest.mark.remote_data` | Bundles via `om4mtools.datasets` | Yes (cached) | `full-suite` only (PR/push → `main`), or locally with `--run-remote-data` |

**Synthetic first.** Prefer procedurally generated fringes, e.g.
`I = a + b·cos(φ(x, y))` with a known `φ`, over real scans. They need no
download and give exact ground truth for `Demodulator` / `Unwrapper`
assertions. Real scans are for regression and realism checks, not
correctness.

**Size budget for `tests/data/`:** each file ≤ 500 kB, whole folder
≤ 5 MB. Anything bigger goes into a bundle.

`tests/conftest.py`:

```python
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-remote-data", action="store_true", default=False,
        help="run tests that download dataset bundles",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: fast offline core subset")
    config.addinivalue_line("markers", "remote_data: needs downloaded bundles")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-remote-data"):
        return
    skip = pytest.mark.skip(reason="needs --run-remote-data")
    for item in items:
        if "remote_data" in item.keywords:
            item.add_marker(skip)


@pytest.fixture(scope="session")
def small_dir():
    from om4mtools.datasets import data_dir
    return data_dir("small")


@pytest.fixture(scope="session")
def heavy_dir():
    from om4mtools.datasets import data_dir
    return data_dir("heavy")
```

Repo note: markers are already registered in `pyproject.toml`
(`[tool.pytest.ini_options] markers`). Add `remote_data` there next to
`smoke` and drop `pytest_configure` from `conftest.py`, so markers are
declared in one place.

Tests use **one fixture per bundle** plus `parametrize` over file names,
never one fixture per file:

```python
@pytest.mark.remote_data
@pytest.mark.parametrize("name", ["scan_01.tif", "scan_02.tif"])
def test_unwrap_real_scans(small_dir, name):
    image = load_image(small_dir / name)
    ...
```

Rules: a test is never both `smoke` and `remote_data`. Tests don't call
`fetch()` or `pooch` directly; they go through the bundle fixtures.

## 6. CI

**`.github/workflows/smoke.yml`** (`develop`): unchanged. `pytest -m smoke --no-cov`.
No data download, no cache step.

**`.github/workflows/full-suite.yml`** (`main`, `full-suite` job): restore the data cache keyed
on whatever defines the data version (the registry in the interim phase,
`datasets.py` in both), so runners re-download only when bundles change:

```yaml
    env:
      OM4MTOOLS_DATA_DIR: ${{ runner.temp }}/om4mtools-data
    steps:
      # ... checkout, setup-python, pip install -e ".[all]" + test deps ...
      - name: Cache dataset bundles
        uses: actions/cache@v4
        with:
          path: ${{ runner.temp }}/om4mtools-data
          key: om4mtools-data-${{ hashFiles('src/om4mtools/datasets.py', 'src/om4mtools/resources/registry.txt') }}
      - name: Full test suite
        run: pytest --cov --run-remote-data
```

If the data host is down, `full-suite` fails. That is intended: releases
must be verified against the real data.

## 7. Building and publishing a bundle

`tools/build_data_archive.py` (dev-only, not shipped):

```python
"""Zip a bundle folder (files at archive root) and print its registry line.

Usage: python tools/build_data_archive.py <folder> <archive.zip>
"""

import sys
import zipfile
from pathlib import Path

import pooch

folder, archive = Path(sys.argv[1]), Path(sys.argv[2])
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
    for path in sorted(folder.rglob("*")):
        if path.is_file():
            zf.write(path, path.relative_to(folder).as_posix())
print(f"{archive.name}  sha256:{pooch.file_hash(str(archive))}  <URL>")
```

Checklist for any data change:

1. Edit the bundle's source folder (outside the repo).
2. Build a **new versioned archive**:
   `python tools/build_data_archive.py om4mtools-data/small fringe_small_v2.zip`
3. Publish it: upload to Dropbox and create a read-only link (interim), or
   add it to a new Zenodo version (target).
4. Interim: replace that bundle's line in `registry.txt` with the printed
   line, filling in the `?dl=1` URL. Target: update the DOI.
5. Update `BUNDLES` in `datasets.py` to the new archive name.
6. Adjust the `remote_data` tests that use the changed files.
7. Run `pytest --run-remote-data` locally before opening the PR.

Hash the exact file you uploaded. Rebuilding the archive, even from
identical files, can change its hash, so never rebuild after publishing.

## 8. Examples and notebooks

`examples/` scripts and notebooks load data with
`from om4mtools.datasets import fetch, data_dir`, never via hardcoded URLs,
local absolute paths, or the old bash download script (retired once
`datasets.py` lands). `examples/data/` holds at most small placeholders;
real sample inputs live in bundles.

## 9. Rules for AI assistants (Claude / Claude Code)

- Never commit binary files > 500 kB, and never add files to `tests/data/`
  or `examples/data/` that break the size budget. Propose adding them to a
  bundle instead.
- Never hardcode dataset URLs, hashes, or archive names outside
  `datasets.py` / `registry.txt`.
- Never make a `smoke`-marked test touch the network or a bundle.
- Prefer synthetic fixtures with known ground truth for new core tests.
  Use `remote_data` only when real data is actually required.
- Tests access bundles through the `small_dir` / `heavy_dir` fixtures and
  `parametrize` over file names; no per-file fixtures, no direct `pooch`
  calls in tests.
- Never import `pooch` or `om4mtools.datasets` from `core/`.
- Never edit a hash in `registry.txt` to make a failing download pass. A
  hash mismatch means the upstream archive changed and must be
  investigated.
- Never modify or overwrite a published archive. Changes go into a new
  versioned archive name (`_v2`, `_v3`, ...).
