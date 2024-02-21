
from .base.bit import Bit, Bitlike, convert_to_bit
from .base.bitarray import BitArray


class SumCarry[T: (Bit, BitArray)]:

    def __init__(self, sum: T, c_out: Bit):
        self._sum = sum
        self._c_out = c_out

    @property
    def sum(self) -> T:
        return self._sum

    @property
    def c_out(self) -> Bit:
        return self._c_out


class HalfAdder(SumCarry[Bit]):

    def __init__(self, x: Bitlike, y: Bitlike):
        x, y = convert_to_bit(x), convert_to_bit(y)
        super().__init__(x ^ y, x & y)


class FullAdder(SumCarry[Bit]):

    def __init__(self, x: Bitlike, y: Bitlike, c_in: Bitlike):
        ha_0 = HalfAdder(x, y)
        ha_1 = HalfAdder(ha_0.sum, c_in)
        super().__init__(ha_1.sum, ha_0.c_out | ha_1.c_out)


class Adder(SumCarry[BitArray]):

    def __init__(self, x: BitArray, y: BitArray, c_in: Bitlike):
        bits: list[Bit] = []
        z_i = c_in
        for x_i, y_i in zip(reversed(x), reversed(y)):
            fa_i = FullAdder(x_i, y_i, z_i)
            bits.append(fa_i.sum)
            z_i = fa_i.c_out
        super().__init__(BitArray(bits, reverse=True), z_i)


class Subtractor(Adder):

    def __init__(self, x: BitArray, y: BitArray):
        super().__init__(x, ~y, 1)


class ALU(Adder):

    def __init__(self, x: BitArray, y: BitArray, s: Bit):
        super().__init__(x, s ^ y, s)
