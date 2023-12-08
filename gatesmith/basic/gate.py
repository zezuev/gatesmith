
from typing import Sequence
from ..engine import circuit, LogicOperation
from .bit import Bit, BitLike, convert_to_bit


def convert_to_ids(s: Sequence[BitLike] | None) -> list[int]:
    if s is None:
        return []
    return [convert_to_bit(b).id_ for b in s]


class Gate(Bit):

    def __init__(
            self,
            op: LogicOperation,
            delay: int,
            inputs: Sequence[int] | None = None,
    ):
        super().__init__(circuit.create_gate(op, delay, inputs))

    @property
    def num_inputs(self) -> int:
        return circuit.get_num_inputs(self._id)

    @property
    def in_(self) -> tuple[int]:
        return tuple(self._get_input_id(idx) for idx in range(self.num_inputs))

    @in_.setter
    def in_(self, new_in: Sequence[BitLike]):
        bits = [convert_to_bit(b) for b in new_in]
        for input_idx, b in enumerate(bits):
            self._set_input(b.id_, input_idx)


class SingleInputGate(Gate):

    def __init__(
            self,
            op: LogicOperation,
            delay: int,
            in_0: BitLike | None = None,
    ):
        super().__init__(op, delay, (convert_to_bit(in_0).id_,))

    @property
    def in_0(self) -> int:
        return self._get_input_id(0)

    @in_0.setter
    def in_0(self, new_in_0: BitLike):
        self._set_input(convert_to_bit(new_in_0).id_, 0)


class DoubleInputGate(Gate):

    def __init__(
            self,
            op: LogicOperation,
            delay: int,
            in_0: BitLike | None = None,
            in_1: BitLike | None = None,
    ):
        super().__init__(op, delay, (convert_to_bit(in_0).id_, convert_to_bit(in_1).id_))

    @property
    def in_0(self) -> int:
        return self._get_input_id(0)

    @in_0.setter
    def in_0(self, new_in_0: BitLike):
        self._set_input(convert_to_bit(new_in_0), 0)

    @property
    def in_1(self) -> int:
        return self._get_input_id(1)

    @in_1.setter
    def in_1(self, new_in_1: BitLike):
        self._set_input(convert_to_bit(new_in_1), 1)


class Not(SingleInputGate):

    def __init__(self, in_0: BitLike | None = None, delay: int | None = None):
        super().__init__(
            LogicOperation.create_not(),
            delay if delay is not None else circuit["DELAY_NOT"],
            in_0,
        )


class And(DoubleInputGate):

    def __init__(
            self,
            in_0: BitLike | None = None,
            in_1: BitLike | None = None,
            delay: int | None = None,
    ):
        super().__init__(
            LogicOperation.create_and(),
            delay if delay is not None else circuit["DELAY_AND"],
            in_0,
            in_1,
        )


class MultiAnd(Gate):

    def __init__(
            self,
            n: int,
            in_: Sequence[BitLike] | None = None,
            delay: int | None = None,
    ):
        super().__init__(
            LogicOperation.create_and(n),
            delay if delay is not None else circuit["DELAY_AND"],
            convert_to_ids(in_),
        )


class Or(DoubleInputGate):

    def __init__(
            self,
            in_0: BitLike | None = None,
            in_1: BitLike | None = None,
            delay: int | None = None,
    ):
        super().__init__(
            LogicOperation.create_or(),
            delay if delay is not None else circuit["DELAY_OR"],
            in_0,
            in_1,
        )


class MultiOr(Gate):

    def __init__(
            self,
            n: int,
            in_: Sequence[BitLike] | None = None,
            delay: int | None = None,
    ):
        super().__init__(
            LogicOperation.create_or(n),
            delay if delay is not None else circuit["DELAY_OR"],
            convert_to_ids(in_),
        )


class Xor(DoubleInputGate):

    def __init__(
            self,
            in_0: BitLike | None = None,
            in_1: BitLike | None = None,
            delay: int | None = None,
    ):
        super().__init__(
            LogicOperation.create_xor(),
            delay if delay is not None else circuit["DELAY_XOR"],
            in_0,
            in_1,
        )


class MultiXor(Gate):

    def __init__(
            self,
            n: int,
            in_: Sequence[BitLike] | None = None,
            delay: int | None = None,
    ):
        super().__init__(
            LogicOperation.create_xor(n),
            delay if delay is not None else circuit["DELAY_XOR"],
            convert_to_ids(in_),
        )


class Nand(DoubleInputGate):

    def __init__(
            self,
            in_0: BitLike | None = None,
            in_1: BitLike | None = None,
            delay: int | None = None,
    ):
        super().__init__(
            LogicOperation.create_nand(),
            delay if delay is not None else circuit["DELAY_NAND"],
            in_0,
            in_1,
        )


class MultiNand(Gate):

    def __init__(
            self,
            n: int,
            in_: Sequence[BitLike] | None = None,
            delay: int | None = None,
    ):
        super().__init__(
            LogicOperation.create_nand(n),
            delay if delay is not None else circuit["DELAY_NAND"],
            convert_to_ids(in_),
        )


class Nor(DoubleInputGate):

    def __init__(
            self,
            in_0: BitLike | None = None,
            in_1: BitLike | None = None,
            delay: int | None = None,
    ):
        super().__init__(
            LogicOperation.create_nor(),
            delay if delay is not None else circuit["DELAY_NOR"],
            in_0,
            in_1,
        )


class MultiNor(Gate):

    def __init__(
            self,
            n: int,
            in_: Sequence[BitLike] | None = None,
            delay: int | None = None,
    ):
        super().__init__(
            LogicOperation.create_nor(n),
            delay if delay is not None else circuit["DELAY_NOR"],
            convert_to_ids(in_),
        )
