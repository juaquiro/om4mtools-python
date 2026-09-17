"""Import-graph guard: `core/` must never depend on the interface layers.

Enforces the dependency-direction rule from CLAUDE.md: `core/` never imports
from `cli/`, `gui/`, or `web/`, and has zero imports of Qt/PyQt, Typer, or
FastAPI. A violation here is a build break, not a lint warning.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

CORE_DIR = Path(__file__).resolve().parent.parent / "src" / "om4mtools" / "core"

FORBIDDEN_OM4MTOOLS_SUBPACKAGES = {"cli", "gui", "web"}

FORBIDDEN_THIRD_PARTY_PREFIXES = (
    "PyQt5",
    "PyQt6",
    "PySide2",
    "PySide6",
    "pyqtgraph",
    "typer",
    "fastapi",
    "uvicorn",
)


def _core_module_files() -> list[Path]:
    return sorted(CORE_DIR.rglob("*.py"))


def _imported_module_names(tree: ast.AST) -> list[str]:
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module is not None:
                names.append(node.module)
    return names


def _violation(module_name: str) -> str | None:
    if module_name.startswith("om4mtools."):
        parts = module_name.split(".")
        if len(parts) >= 2 and parts[1] in FORBIDDEN_OM4MTOOLS_SUBPACKAGES:
            return f"om4mtools.{parts[1]}"
    for prefix in FORBIDDEN_THIRD_PARTY_PREFIXES:
        if module_name == prefix or module_name.startswith(prefix + "."):
            return prefix
    return None


@pytest.mark.smoke
def test_core_has_no_forbidden_imports() -> None:
    """`core/` must not import `cli/`, `gui/`, `web/`, Qt, Typer, or FastAPI."""
    violations: list[str] = []
    for path in _core_module_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for module_name in _imported_module_names(tree):
            forbidden = _violation(module_name)
            if forbidden is not None:
                violations.append(
                    f"{path.relative_to(CORE_DIR.parent.parent.parent)}: imports {module_name}"
                )

    assert not violations, "core/ imports forbidden modules:\n" + "\n".join(violations)


@pytest.mark.smoke
def test_core_directory_exists() -> None:
    """Sanity check that the scan actually looked at files."""
    assert _core_module_files(), f"no .py files found under {CORE_DIR}"
