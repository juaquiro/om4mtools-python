# TODO

## Demodulator / PSA4 review (2026-09-25)

1. ~~**`demodulator_factory.py:8`** — `def create(...)` is missing the trailing
   `:` after the return type annotation. `SyntaxError`, file won't import.~~
   **DONE**
2. ~~**`demodulator_factory.py:10`** — `return(DemodulatorPSA4)` returns the
   *class*, not an instance. Should be `return DemodulatorPSA4()`.~~
   **DONE**
3. ~~**`demodulator_factory.py`** — `**kwargs` accepted but never forwarded to
   the demodulator constructor. Dead parameter.~~
   **N/A** — intentional: reserved for future demodulator types that take
   constructor args; PSA4 has none, so nothing to forward yet.
4. ~~**`demodulator_PSA4.py:_setup`** — sets `self.n_igrams` /
   `self.delta_list` as bare instance attributes instead of going through
   `self.demod_params.n_igrams` / `self.demod_params.delta_list`, bypassing
   `DemodParams._validate()`. Deviates from the pattern documented in
   CLAUDE.md ("Design decisions").~~
   **DONE**
5. ~~**`demodulator_PSA4.py:process`** — never calls
   `self.demod_params.verify_params()` before executing, as CLAUDE.md
   specifies core classes should.~~
   **DONE**
6. ~~**`demodulator_params.py` / `demodulator_PSA4.py`** — `DemodParams.z_list`
   is never populated by `process()`. Decide whether it should hold the
   output phasor(s) and wire it up, or remove/document it as unused for now.~~
   **DONE** — `process()` now returns `None` and stores the phasor in
   `self.demod_params.z_list`.
7. ~~**`demodulator_PSA4.py:6-7`** — redundant imports of `RealArray`/
   `ComplexArray` from both `.demodulator` and `.types`; keep only the
   `.types` import.~~
   **DONE**
8. ~~**`demodulator_PSA4.py`** — `class DemodulatorPSA4` has no class
   docstring (required by CLAUDE.md for public classes).~~
   **DONE**
9. ~~**`demodulator_params.py`** — `class DemodParams` has no class docstring.~~
   **DONE**
10. ~~**Typos in docstrings**: `demodulator.py` typos~~ **fixed via #16**.
    ~~`demodulator_PSA4.py:35` "descrived"→"described".~~
    **DONE** — scanned remaining files, no further typos found.
11. ~~**`demodulator_params.py:47-57`** — stray unassigned triple-quoted
    string after the class (not a docstring, not a comment — a no-op
    expression statement). Turn into a comment or move into docs/example.~~
    **DONE** — folded into the class docstring as an `Examples` (doctest)
    section.
12. ~~**`demodulator_types.py`** — inconsistent indentation in the
    `References`/`----------` docstring lines.~~
    **DONE** — also caught and fixed a missed typo, "avalilable"→"available".
13. ~~**`demodulator.py`** — ~8 trailing blank lines at end of file.~~
    **DONE**
14. ~~**`demodulator_PSA4.py:process`** — only validates `len(igram_list)`;
    no explicit check that all igrams share shape/dtype before arithmetic
    (numpy will raise anyway on mismatch — low priority).~~
    **N/A** — intentional: rely on numpy's own broadcasting/shape-mismatch
    errors instead of a redundant explicit check.
15. ~~**`demodulator_factory.py:create`** — missing `@staticmethod` decorator;
    works today only via unbound-function access on the class, fragile if
    called on an instance.~~
    **DONE**
17. ~~**`demodulator_PSA4.py:39`** — stray `3` on its own line inside
    `process()`'s docstring (was blank before a recent edit).~~
    **DONE**
16. ~~**`demodulator.py:26`** — abstract `process()` signature was updated to
    `-> None` (results now land in `demod_params.z_list`), but the docstring
    still describes the old "returns a tuple of ComplexArray" contract.
    Rewrite to match the new `z_list`-based contract (and fix the typos
    noted in #10 while in there).~~
    **DONE** — docstrings for `_setup()` and `process()` rewritten; also
    fixes the `demodulator.py` typos from #10 ("musr"/"functin"/
    "differnet"/"Cppmpex").

## `download_data_fixtures.sh` review (2026-09-25)

1. ~~**Wrong destination** — `DEST_DIR="data"` resolved relative to cwd, not
   to `tests/data` where tests actually load fixtures from.~~
   **DONE** — resolved relative to the script's own location via
   `SCRIPT_DIR`, targets `tests/data`.
2. ~~**Destructive `rm -rf "$DEST_DIR"`** with no confirmation, on a
   directory that holds hand-authored files (`README.md`,
   `peaks_49x50.m`, the generated CSV) not present in the Dropbox
   bundle.~~
   **DONE** — now prompts `[y/N]` before deleting an existing
   `tests/data/`.
3. **Hardcoded Dropbox share link (`rlkey=...`) committed to the
   script** — once committed it's exposed to anyone with repo access
   indefinitely, independent of the repo's own permissions.
   **TRACKED, not fixed** — kept intentionally for now (Dropbox+bash
   approach is the current choice); follow-up captured in
   [GH issue #2](https://github.com/juaquiro/om4mtools-python/issues/2)
   and in CLAUDE.md's "Test fixture hosting" convention (prefer a
   GitHub Release asset, or `pooch`, over a public third-party link).
4. ~~**Header/filename drift** — top-of-file comment still referenced
   `download_dropbox_directory.sh` instead of the actual filename.~~
   **DONE**
5. **Location at repo root instead of `tests/data/`** — raised as a
   suggestion.
   **N/A** — intentional: this is a post-clone setup script, meant to
   be the first thing a new contributor runs/sees at the repo root.
6. ~~**No cleanup on failure** — `rm -f "$TEMP_ZIP"` only ran at the very
   end; a failed extraction under `set -e` would leave it behind.~~
   **DONE** — replaced with `trap 'rm -f "$TEMP_ZIP"' EXIT`.
