"""Integration tests for the imageviewer GUI widget."""

from __future__ import annotations

import pytest

pytest.importorskip("PyQt6")


def test_widget_is_a_pure_qwidget() -> None:
    """ImageViewerWidget has no application-bootstrap side effects on import."""
    from PyQt6.QtWidgets import QWidget

    from om4mtools.gui.imageviewer.widget import ImageViewerWidget

    assert issubclass(ImageViewerWidget, QWidget)
