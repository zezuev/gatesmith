
from typing import Sequence
from ..engine import circuit, LogicOperation


class Bit:

    def __init__(self, id_: int | None = None):
        # default to constant False in case no id is provided
        self._id = id_ or 0

    def _set_id(self, new_id: int):
        self._id = new_id

    def _set_state(self, new_state: bool, delay = 0):
        circuit.set_state(self._id, new_state, delay)

    def _get_input_id(self, input_idx: int):
        return circuit.get_input_id(self._id, input_idx)

    def _set_input(self, input_id: int, input_idx: int):
        circuit.set_input(self._id, input_id, input_idx)

    def __repr__(self):
        return f"{self.__class__.__name__}(id_={self._id})"

    def __bool__(self):
        return self.state

    def __int__(self):
        return int(self.state)

    def __and__(self, other):
        if isinstance(other, Bit):
            and_id = circuit.create_gate(
                LogicOperation.create_and(),
                circuit["DELAY_AND"],
                (self._id, other.id_),
            )
            return Bit(and_id)
        raise TypeError(
            f"Can only apply logical AND to instances of {self.__class__.__name__}"
        )

    def __rand__(self, other):
        return self.__and__(other)

    def __or__(self, other):
        if isinstance(other, Bit):
            or_id = circuit.create_gate(
                LogicOperation.create_or(),
                circuit["DELAY_OR"],
                (self._id, other.id_),
            )
            return Bit(or_id)
        raise TypeError(
            f"Can only apply logical OR to instances of {self.__class__.__name__}"
        )

    def __ror__(self, other):
        return self.__or__(other)

    def __xor__(self, other):
        if isinstance(other, Bit):
            xor_id = circuit.create_gate(
                LogicOperation.create_xor(),
                circuit["DELAY_XOR"],
                (self._id, other.id_),
            )
            return Bit(xor_id)
        raise TypeError(
            f"Can only apply logical XOR to instances of {self.__class__.__name__}"
        )

    def __rxor__(self, other):
        return self.__xor__(other)

    def __invert__(self):
        not_id = circuit.create_gate(
            LogicOperation.create_not(),
            circuit["DELAY_NOT"],
            (self._id,),
        )
        return Bit(not_id)

    @property
    def state(self) -> bool:
        """The current bit state."""
        return circuit.get_state(self._id)

    @property
    def id_(self) -> int:
        """The bit id in the circuit."""
        return self._id


# any type that can be interpreted as a Bit
type BitLike = Bit | int | bool


class Constant(Bit):

    def __init__(self, value: bool):
        super().__init__(int(value))


False_ = Constant(False)
True_ = Constant(True)

def convert_to_bit(b: BitLike) -> Bit:
    if isinstance(b, int):
        if b == 0:
            return False_
        return True_
    if b == False or b is None:
        return False_
    if b == True:
        return True_
    return b
