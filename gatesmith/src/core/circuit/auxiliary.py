
import numpy as np
from numpy.typing import NDArray


def extend_array(arr: NDArray) -> NDArray:
    match arr.shape:
        case (x,) if x > 0:
            ext_arr = np.ndarray(2*x, dtype=arr.dtype)
            ext_arr[:x] = arr
        case (x, y):
            ext_arr = np.ndarray((x, 2*y), dtype=arr.dtype)
            ext_arr[:, :y] = arr
        case _:
            raise TypeError(
                f"Can only extend vectors or matrices, not arrays of dimension {arr.shape!r}"
            )
    return ext_arr
