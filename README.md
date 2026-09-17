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
ruff check .
black --check .
```

### Branching

- `develop` (default): everyday integration. Trivial changes push directly;
  feature work goes through a `feature/xyz` branch and a PR gated on the
  `smoke` check.
- `main` (protected): releases only, via PR from `develop` (or `hotfix/*`),
  gated on the `full-suite` check. Bump the version in `pyproject.toml` as
  part of the release PR.

## License

BSD 3-Clause — see [LICENSE](LICENSE).
