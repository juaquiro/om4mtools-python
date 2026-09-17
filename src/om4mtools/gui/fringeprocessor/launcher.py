"""Standalone launcher for the fringeprocessor GUI: app bootstrap + show + exec."""

from __future__ import annotations

from om4mtools.gui.common.qapp import get_qapp
from om4mtools.gui.fringeprocessor.widget import FringeProcessorWidget


def main() -> None:
    """Launch the fringeprocessor as a standalone application."""
    app = get_qapp()
    widget = FringeProcessorWidget()
    widget.show()
    app.exec()


if __name__ == "__main__":
    main()
