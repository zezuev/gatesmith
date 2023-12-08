
from ..basic import Bit, BitArray, MultiMux, False_
from .math import Accumulator


class ProgramCounter:

    def __init__(
            self,
            d: BitArray,
            s_0: Bit,
            s_1: Bit,
            e: Bit,
            clk: Bit,
            rst: Bit | None = None,
    ):
        mux_0 = MultiMux((d, BitArray(dec=1, n=len(d))))
        acc_0 = Accumulator(mux_0, False_, s_0, e, clk, rst)
        self._q = acc_0.sum_

    @property
    def q(self) -> BitArray:
        return self._q
