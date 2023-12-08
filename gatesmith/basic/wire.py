
from ..engine import circuit
from .bit import Bit, BitLike, convert_to_bit


class Wire(Bit):

    def __init__(self):
        super().__init__(circuit.create_wire())
        self._remapped = False

    @property
    def in_(self) -> int:
        return self._id

    @in_.setter
    def in_(self, new_in: BitLike):
        if self._remapped:
            raise TypeError("Cannot set wire input twice.")
        new_id = convert_to_bit(new_in).id_
        circuit.remap_id(self._id, new_id)
        self._set_id(new_id)
        self._remapped = True
