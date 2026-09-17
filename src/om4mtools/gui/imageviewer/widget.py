"""Imageviewer widget. Pure QWidget, no app bootstrap — see `launcher.py`."""

from __future__ import annotations

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ImageViewerWidget(QWidget):
    """Widget that displays a fringe-pattern image and its properties."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self._label = QLabel("No image loaded")
        layout.addWidget(self._label)

    def load_image(self, image_path: str) -> None:
        """Load and display an image.

        Parameters
        ----------
        image_path : str
            Path to the image file to display.
        """
        from om4mtools.cli.imageviewer.runner import load_and_describe

        info = load_and_describe(image_path)
        self._label.setText(f"{info['path']}: {info['shape']} ({info['dtype']})")
