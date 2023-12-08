
import numpy as np


def double_width(x: np.ndarray) -> np.ndarray:
    """Create an a vector or 2D matrix with double the width of `x`.
    Used for dynamic memory allocation."""
    if len(x.shape) == 1:  # vector
        new_x = np.ndarray(len(x) * 2, dtype=x.dtype)
        new_x[:len(x)] = x
        return new_x
    elif len(x.shape) == 2:  # array
        new_x = np.ndarray((x.shape[0], x.shape[1] * 2), dtype=x.dtype)
        new_x[:, :x.shape[1]] = x
        return new_x
    raise ValueError(f"Cannot double width of array with shape {x.shape}.")
