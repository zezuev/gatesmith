
from .bit import Bit, convert_to_bit
from .gate import Nand, MultiNand


class SRLatch:
    """Classic NAND-based SR Latch implementation."""

    def __init__(
            self,
            s: Bit,
            r: Bit,
            set_: Bit | None = None,
            rst: Bit | None = None,
    ):
        if not (set_ is None and rst is None):
            set_, rst = convert_to_bit(set_), convert_to_bit(rst)
            s = set_ | (s & ~rst)
            r = rst | (r & ~set_)

        nand_0 = Nand()
        nand_1 = Nand(s, nand_0)
        nand_0.in_ = r, nand_1
        self._q = nand_0
        self._nq = nand_1

    @property
    def q(self) -> Bit:
        return self._q

    @property
    def nq(self) -> Bit:
        return self._nq


class DFlipFlop:

    def __init__(
            self,
            d: Bit,
            clk: Bit,
            set_: Bit | None = None,
            rst: Bit | None = None,
    ):
        nand_0 = Nand()
        nand_1 = Nand()

        mnand_0 = MultiNand(3)
        mnand_1 = MultiNand(3, (mnand_0, clk, nand_1))
        mnand_0.in_ = mnand_1, clk, nand_0

        nand_0.in_ = mnand_0, nand_1
        nand_1.in_ = mnand_1, d

        srl_0 = SRLatch(mnand_1, mnand_0, set_, rst)
        self._q = srl_0.q
        self._nq = srl_0.nq

    @property
    def q(self) -> Bit:
        return self._q

    @property
    def nq(self) -> Bit:
        return self._nq


class SRFlipFlop:

    def __init__(
            self,
            s: Bit,
            r: Bit,
            clk: Bit,
            set_: Bit | None = None,
            rst: Bit | None = None,
    ):
        nand_0 = Nand()
        nand_1 = Nand()

        mnand_0 = MultiNand(3)
        mnand_1 = MultiNand(3, (mnand_0, clk, nand_1))
        mnand_0.in_ = mnand_1, clk, nand_0

        nand_0.in_ = mnand_0, r
        nand_1.in_ = mnand_1, s

        srl_0 = SRLatch(mnand_1, mnand_0, set_, rst)
        self._q = srl_0.q
        self._nq = srl_0.nq

    @property
    def q(self) -> Bit:
        return self._q

    @property
    def nq(self) -> Bit:
        return self._nq
