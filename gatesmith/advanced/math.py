
from ..basic import Bit, BitArray, Wire, WireArray, DFlipFlop, ALU, MultiMux
from .memory import Register


class Accumulator:

    def __init__(
            self,
            d: BitArray,
            s_0: Bit,
            s_1: Bit,
            e: Bit,
            clk: Bit,
            rst: Bit | None = None,
    ):
        w_0 = WireArray(len(d))
        reg_0 = Register(w_0, e, clk, rst=rst)
        alu_0 = ALU(reg_0, d, s_0)
        w_0.in_ = MultiMux((alu_0.sum_, d), s_1)
        self._sum = reg_0
        self._c_out = alu_0.c_out

    @property
    def sum_(self) -> BitArray:
        return self._sum

    @property
    def c_out(self) -> Bit:
        return self._c_out


class BinaryCounter:

    def __init__(
            self,
            clk: Bit,
            set_: Bit,
            n: int,
    ):
        q: list[Bit] = []
        wires = [Wire() for _ in range(n)]
        d = clk

        for w_i in wires:
            flop_i = DFlipFlop(w_i, d, set_=set_)
            w_i.in_ = flop_i.nq
            d = flop_i.nq
            q.append(flop_i.q)

        self._q = BitArray(q, reverse=True)

    @property
    def q(self) -> BitArray:
        return self._q
