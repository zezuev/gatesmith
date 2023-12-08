
from ..basic.bit import Bit
from ..basic.bitarray import BitArray
from ..basic.wire import Wire
from ..basic.memory import DFlipFlop, SRFlipFlop
from ..basic.gate import Nand
from ..basic.control import Mux


class Register(BitArray):

    def __init__(
            self,
            d: BitArray,
            e: Bit,
            clk: Bit,
            set_: Bit | None = None,
            rst: Bit | None = None,
    ):
        super().__init__(
            SRFlipFlop(Nand(~d_i, e), Nand(d_i, e), clk, set_, rst).q
            for d_i in d
        )


class ShiftRegister(BitArray):

    def __init__(
            self,
            d_l: Bit,
            d_r: Bit,
            dir_: Bit,
            clk: Bit,
            n: int,
            set_: Bit | None = None,
            rst: Bit | None = None,
    ):
        super().__init__()
        x_wires = [Wire() for _ in range(n)]
        y_wires = [Wire() for _ in range(n)]
        q: list[Bit] = []

        for x_i, y_i in zip(x_wires, y_wires):
            mux_i = Mux((x_i, y_i), dir_)
            flop_i = DFlipFlop(mux_i, clk, set_, rst)
            q.append(flop_i.q)

        x_wires[0].in_ = d_l
        for i in range(1, n):
            x_wires[i].in_ = q[i-1]

        for i in range(n-1):
            y_wires[i].in_ = q[i+1]
        y_wires[-1].in_ = d_r

        self._set_bits(q)
