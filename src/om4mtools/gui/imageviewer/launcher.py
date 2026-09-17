"""Standalone launcher for the imageviewer GUI: app bootstrap + show + exec."""

from __future__ import annotations

from om4mtools.gui.common.qapp import get_qapp
from om4mtools.gui.imageviewer.widget import ImageViewerWidget


def main() -> None:
    """Launch the imageviewer as a standalone application."""
    app = get_qapp()
    widget = ImageViewerWidget()
    widget.show()
    app.exec()


if __name__ == "__main__":
    main()
