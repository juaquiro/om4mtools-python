"""Shared QApplication singleton, safe from a script, notebook, or launcher."""

from __future__ import annotations

from PyQt6.QtWidgets import QApplication


def get_qapp() -> QApplication:
    """Return the process-wide QApplication, creating it if needed.

    Safe to call repeatedly and from multiple entry points (a script, a
    notebook, or a tool's `launcher.py`) — reuses the existing instance
    instead of constructing a second one.

    Returns
    -------
    PyQt6.QtWidgets.QApplication
        The singleton application instance.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app
