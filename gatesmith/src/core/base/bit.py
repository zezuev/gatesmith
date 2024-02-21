
from collections.abc import Iterable
from ..logic import circuit, Operator


class Bit:

    def __init__(self, component_id: int | None = None):
        self._component_id = component_id or 0

    def _set_input_ids(self, input_ids: Iterable[int]):
        circuit.set_input_ids(self._component_id, input_ids)

    def _set_input_id(self, input_idx: int, input_id: int):
        circuit.set_input_id(self._component_id, input_idx, input_id)

    def _get_input_ids(self) -> tuple[int, ...]:
        return circuit.get_input_ids(self._component_id)

    def _get_input_id(self, input_idx: int) -> int:
        return circuit.get_input_id(self._component_id, input_idx)

    def _set_state(self, new_state: bool, delay: int = 0):
        circuit.set_state(self._component_id, new_state, delay)

    def __bool__(self):
        return circuit.get_state(self._component_id)

    def __int__(self):
        return int(self.__bool__())

    def __repr__(self):
        return str(self.__int__())

    def __invert__(self):
        return Bit(circuit.create_component(
            Operator.create_not(),
            circuit.settings["DELAY_NOT"],
            (self._component_id,),
        ))

    def __and__(self, other):
        if isinstance(other, Bit):
            return Bit(circuit.create_component(
                Operator.create_and(),
                circuit.settings["DELAY_AND"],
                (self._component_id, other.component_id),
            ))
        if hasattr(other, "__and__"):
            return other.__and__(self)
        raise TypeError(f"Can only apply logical AND to a Bit or BitArray")

    def __or__(self, other):
        if isinstance(other, Bit):
            return Bit(circuit.create_component(
                Operator.create_or(),
                circuit.settings["DELAY_OR"],
                (self._component_id, other.component_id),
            ))
        if hasattr(other, "__or__"):
            return other.__or__(self)
        raise TypeError(f"Can only apply logical OR to a Bit or BitArray")

    def __xor__(self, other):
        if isinstance(other, Bit):
            return Bit(circuit.create_component(
                Operator.create_xor(),
                circuit.settings["DELAY_XOR"],
                (self._component_id, other.component_id),
            ))
        if hasattr(other, "__xor__"):
            return other.__xor__(self)
        raise TypeError(f"Can only apply logical XOR to a Bit or BitArray")

    @property
    def component_id(self) -> int:
        return self._component_id

    @property
    def state(self) -> bool:
        return self.__bool__()


class Constant(Bit):

    def __init__(self, value: bool):
        super().__init__(int(value))

FALSE = Constant(False)
TRUE = Constant(True)


type Bitlike = Bit | bool | int

def convert_to_bit(b: Bitlike) -> Bit:
    if isinstance(b, int):
        if b == 0:
            return FALSE
        return TRUE
    if b == False or b is None:
        return FALSE
    if b == True:
        return TRUE
    return b
