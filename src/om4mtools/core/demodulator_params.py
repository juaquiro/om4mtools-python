from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class DemodParams:
    roi_mask: Any = None
    z_list: Any = None
    n_igrams: int | None = None
    roi_norm_th: float = 0.15
    delta_list: tuple[float, ...] | None = None

    def __setattr__(self, name: str, value: Any) -> None:
        value = self._validate(name, value)
        object.__setattr__(self, name, value)

    def _validate(self, name: str, value: Any) -> Any:
        """Per-field checks. May return a normalized value."""
        if value is None:
            return value
        if name == "roi_norm_th":
            if not 0.0 <= value <= 1:
                raise ValueError("roi_norm_th must be in [0, 1]")
        elif name == "n_igrams":
            if value < 1:
                raise ValueError("n_igrams must be at least 1")
        elif name == "delta_list":
            try:
                value = tuple(float(x) for x in value)
            except (TypeError, ValueError) as e:
                raise TypeError("delta_list must be a sequence of numbers") from e
        return value

    def verify_params(self) -> None:
        """Cross-field consistency. Call before processing."""
        if self.n_igrams is None:
            raise ValueError("n_igrams must be set")
        if self.delta_list is None:
            raise ValueError("delta_list must be set")
        if len(self.delta_list) != self.n_igrams:
            raise ValueError(
                f"delta_list has {len(self.delta_list)} entries, "
                f"but n_igrams is {self.n_igrams}"
            )


"""
intended use

p = DemodParams()
p.n_igrams = 5
p.delta_list = [0, 1.57, 3.14, 4.71, 6.28]   # stored as a tuple of floats
p.verify_params()                               # ok

p.n_igrams = 6                                 # allowed: no eager cross-check
p.verify_params()                              # ValueError: 5 entries vs n_igrams 6
"""
