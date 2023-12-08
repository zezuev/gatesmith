
from .bitarray import BitArray
from .wire import Wire


class WireArray(BitArray):

    def __init__(self, n: int):
        super().__init__()
        self._wires = tuple(Wire() for _ in range(n))
        self._set_bits(self._wires)

    @property
    def in_(self) -> tuple[int]:
        return tuple(w.in_ for w in self._wires)

    @in_.setter
    def in_(self, new_in: BitArray):
        for w_i, in_i in zip(self._wires, new_in, strict=True):
            w_i.in_ = in_i
