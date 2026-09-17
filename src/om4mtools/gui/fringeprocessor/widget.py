"""Fringeprocessor widget. Pure QWidget, no app bootstrap — see `launcher.py`."""

from __future__ import annotations

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class FringeProcessorWidget(QWidget):
    """Widget that runs demodulation/unwrapping on a fringe-pattern image."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self._label = QLabel("No image processed")
        layout.addWidget(self._label)

    def process_image(self, image_path: str, carrier_frequency: tuple[float, float]) -> None:
        """Process an image and display the resulting phase shape.

        Parameters
        ----------
        image_path : str
            Path to the fringe-pattern image.
        carrier_frequency : tuple[float, float]
            Spatial carrier frequency ``(fx, fy)``, in cycles per pixel.
        """
        from om4mtools.cli.fringeprocessor.runner import process_fringe_pattern

        phase = process_fringe_pattern(image_path, carrier_frequency)
        self._label.setText(f"unwrapped phase shape: {phase.shape}")
