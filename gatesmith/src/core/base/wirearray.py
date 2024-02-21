
from collections.abc import Iterable
from .bit import Bit, Bitlike
from .bitarray import BitArray
from .wire import Wire


class WireArray(BitArray):

    def __init__(self, n: int):
        wires = [Wire() for _ in range(n)]
        super().__init__(wires)
        self._wires = wires

    @property
    def inputs(self) -> tuple[Bit, ...]:
        return tuple(w.input for w in self._wires)

    @inputs.setter
    def inputs(self, new_inputs: Iterable[Bitlike]):
        for w, i in zip(self._wires, new_inputs):
            w.input = i
