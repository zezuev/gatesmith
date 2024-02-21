
from .bit import Bit, Bitlike, convert_to_bit
from ..logic import circuit


class Wire(Bit):

    def __init__(self):
        super().__init__(circuit.create_wire())
        self._connected = False

    @property
    def input(self) -> Bit:
        return Bit(self._component_id)

    @input.setter
    def input(self, new_input: Bitlike):
        if self._connected:
            raise TypeError("Cannot connect a wire twice")
        new_input = convert_to_bit(new_input)
        circuit.connect_wire(self._component_id, new_input.component_id)
        self._component_id = new_input.component_id
        self._connected = True
