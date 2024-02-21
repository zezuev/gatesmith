
from collections.abc import Iterable
from .bit import Bit, Bitlike, convert_to_bit


def dec_to_bin(dec: int, n: int | None = None) -> list[int]:
    bits = [int(b) for b in bin(dec)[2:]]
    if n is None:
        n = len(bits)
    return bits + [0 for _ in range(n - len(bits))]

def hex_to_bin(hex: str, n: int | None = None) -> list[int]:
    return dec_to_bin(int(hex, base=26), n)


class BitArray:

    def __init__(
            self,
            content: Iterable[Bitlike],
            *,
            dec: int | None = None,
            hex: int | None = None,
            n: int | None = None,
            reverse: bool = False,
    ):
        if dec is not None:
            content = dec_to_bin(dec, n)
        elif hex is not None:
            content = hex_to_bin(hex, n)
        elif n is not None:
            content = dec_to_bin(0, n)
        if content is None:
            raise ValueError("No content information was provided")

        if reverse:
            content = reversed(content)
        self._bits = tuple(convert_to_bit(c) for c in content)

    def __int__(self):
        return int(self.__repr__(), base=2)

    def __repr__(self):
        return "".join(repr(b) for b in self._bits)

    def __iter__(self):
        return iter(self._bits)

    def __reversed__(self):
        return BitArray(self._bits, reverse=True)

    def __invert__(self):
        return BitArray(~b for b in self._bits)

    def __and__(self, other):
        if isinstance(other, BitArray):
            return BitArray(b_0 & b_1 for b_0, b_1 in zip(self._bits, other.bits))
        if isinstance(other, Bit):
            return BitArray(b & other for b in self._bits)
        raise TypeError(f"Can only apply logical AND to a Bit or BitArray")

    def __or__(self, other):
        if isinstance(other, BitArray):
            return BitArray(b_0 | b_1 for b_0, b_1 in zip(self._bits, other.bits))
        if isinstance(other, Bit):
            return BitArray(b | other for b in self._bits)
        raise TypeError(f"Can only apply logical OR to a Bit or BitArray")

    def __xor__(self, other):
        if isinstance(other, BitArray):
            return BitArray(b_0 ^ b_1 for b_0, b_1 in zip(self._bits, other.bits))
        if isinstance(other, Bit):
            return BitArray(b ^ other for b in self._bits)
        raise TypeError(f"Can only apply logical XOR to a Bit or BitArray")

    @property
    def bits(self) -> tuple[Bit, ...]:
        return self._bits
