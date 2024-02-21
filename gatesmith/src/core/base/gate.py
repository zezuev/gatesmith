
from collections.abc import Iterable
from .bit import Bit, Bitlike, convert_to_bit
from ..logic import circuit, Operator


class Gate(Bit):

    def __init__(
            self,
            op: Operator,
            delay: int,
            inputs: Iterable[Bitlike] | None = None,
    ):
        input_ids = [convert_to_bit(b) for b in inputs] if inputs else None
        super().__init__(circuit.create_component(op, delay, input_ids))

    def _get_num_inputs(self, inputs: Iterable[Bitlike] | None, n: int | None) -> int:
        if inputs:
            return len(inputs)
        if n is not None:
            return n
        raise ValueError("Must either provide a list of inputs or the desired input number")

    @property
    def inputs(self) -> tuple[Bit, ...]:
        return tuple(Bit(input_id) for input_id in circuit.get_input_ids(self._component_id))

    @inputs.setter
    def inputs(self, new_inputs: Iterable[Bitlike]):
        input_ids = [convert_to_bit(b).component_id for b in new_inputs]
        circuit.set_input_ids(self._component_id, input_ids)


class Not(Gate):

    def __init__(self, input: Bitlike | None = None, *, delay: int | None = None):
        if input is None:
            input = 0
        if delay is None:
            delay = circuit.settings["DELAY_NOT"]
        super().__init__(Operator.create_not(), delay, (input,))


class Id(Gate):

    def __init__(self, input: Bitlike | None = None, *, delay: int | None = None):
        if input is None:
            input = 0
        if delay is None:
            delay = circuit.settings["DELAY_ID"]
        super().__init__(Operator.create_id(), delay, (input,))


class And(Gate):

    def __init__(
            self,
            inputs: Iterable[Bitlike] | None = None,
            *,
            n: int | None = None,
            delay: int | None = None,
    ):
        if delay is None:
            delay = circuit.settings["DELAY_AND"]
        num_inputs = self._get_num_inputs(inputs, n)
        super().__init__(Operator.create_and(num_inputs), delay, inputs)


class Nand(Gate):

    def __init__(
            self,
            inputs: Iterable[Bitlike] | None = None,
            *,
            n: int | None = None,
            delay: int | None = None,
    ):
        if delay is None:
            delay = circuit.settings["DELAY_NAND"]
        num_inputs = self._get_num_inputs(inputs, n)
        super().__init__(Operator.create_nand(num_inputs), delay, inputs)


class Or(Gate):

    def __init__(
            self,
            inputs: Iterable[Bitlike] | None = None,
            *,
            n: int | None = None,
            delay: int | None = None,
    ):
        if delay is None:
            delay = circuit.settings["DELAY_OR"]
        num_inputs = self._get_num_inputs(inputs, n)
        super().__init__(Operator.create_or(num_inputs), delay, inputs)


class Nor(Gate):

    def __init__(
            self,
            inputs: Iterable[Bitlike] | None = None,
            *,
            n: int | None = None,
            delay: int | None = None,
    ):
        if delay is None:
            delay = circuit.settings["DELAY_NOR"]
        num_inputs = self._get_num_inputs(inputs, n)
        super().__init__(Operator.create_nor(num_inputs), delay, inputs)


class Xor(Gate):

    def __init__(
            self,
            inputs: Iterable[Bitlike] | None = None,
            *,
            n: int | None = None,
            delay: int | None = None,
    ):
        if delay is None:
            delay = circuit.settings["DELAY_XOR"]
        num_inputs = self._get_num_inputs(inputs, n)
        super().__init__(Operator.create_xor(num_inputs), delay, inputs)


class Eq(Gate):

    def __init__(
            self,
            inputs: Iterable[Bitlike] | None = None,
            *,
            n: int | None = None,
            delay: int | None = None,
    ):
        if delay is None:
            delay = circuit.settings["DELAY_EQ"]
        num_inputs = self._get_num_inputs(inputs, n)
        super().__init__(Operator.create_eq(num_inputs), delay, inputs)
