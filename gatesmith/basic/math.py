
from .bit import Bit, BitLike, convert_to_bit
from .bitarray import BitArray
from .gate import Xor, And
from .control import Mux, MultiMux


class HalfAdder:

    def __init__(self, x: BitLike, y: BitLike):
        self._sum = Xor(x, y)
        self._c_out = And(x, y)

    @property
    def sum_(self) -> Bit:
        return self._sum

    @property
    def c_out(self) -> Bit:
        return self._c_out


class FullAdder:

    def __init__(self, x: Bit, y: BitLike, c_in: BitLike | None = None):
        ha_0 = HalfAdder(x, y)
        ha_1 = HalfAdder(ha_0.sum_, convert_to_bit(c_in))
        self._sum = ha_1.sum_
        self._c_out = ha_0.c_out | ha_1.c_out

    @property
    def sum_(self) -> Bit:
        return self._sum

    @property
    def c_out(self) -> Bit:
        return self._c_out


class Adder:

    def __init__(self, x: BitArray, y: BitArray, c_in: BitLike | None = None):
        bits: list[Bit] = []
        z_i = c_in
        for x_i, y_i in zip(reversed(x), reversed(y)):
            fa_i = FullAdder(x_i, y_i, z_i)
            z_i = fa_i.c_out
            bits.append(fa_i.sum_)
        self._sum = BitArray(bits, reverse=True)
        self._c_out = z_i

    @property
    def sum_(self) -> BitArray:
        return self._sum

    @property
    def c_out(self) -> Bit:
        return self._c_out


class Subtractor:

    def __init__(self, x: BitArray, y: BitArray):
        # assumption: 2's complement
        add_0 = Adder(x, ~y, 1)
        self._sum = add_0.sum_
        self._c_out = add_0.c_out

    @property
    def sum_(self) -> BitArray:
        return self._sum

    @property
    def c_out(self) -> Bit:
        return self._c_out


class ALU:

    def __init__(self, x: BitArray, y: BitArray, s: Bit):
        add_0 = Adder(x, y)
        sub_0 = Subtractor(x, y)
        self._sum = MultiMux((add_0.sum_, sub_0.sum_), s)
        self._c_out = Mux((add_0.c_out, sub_0.c_out), s)

    @property
    def sum_(self) -> BitArray:
        return self._sum

    @property
    def c_out(self) -> Bit:
        return self._c_out
