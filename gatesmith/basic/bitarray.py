
from typing import Sequence
from .bit import Bit, BitLike, convert_to_bit


def dec_to_bin(n: int, k: int | None = None) -> list[int]:
    bin_ = [int(x) for x in list(bin(n)[2:])]
    if k is None:
        return bin_
    if len(bin_) > k:
        raise ValueError("Not enough digits available.")
    # add leading zeros as padding
    return [0 for _ in range(k - len(bin_))] + bin_

def hex_to_bin(h: str, k: int | None = None) -> list[int]:
    return dec_to_bin(int(h, base=16), k)


class BitArray:

    def __init__(
            self,
            content: Sequence[BitLike] | None = None,
            reverse = False,
            dec: int | None = None,
            hex_: str | None = None,
            n: int | None = None,
    ):
        if dec is not None:
            content = dec_to_bin(dec, n)
        elif hex_ is not None:
            content = hex_to_bin(hex_, n)
        elif n is not None:
            # simply a padded zero
            content = dec_to_bin(0, n)

        content = content or []
        if reverse:
            content = reversed(content)
        self._bits = tuple(convert_to_bit(c) for c in content)

    def _set_bits(self, bits: Sequence[Bit]):
        self._bits = bits

    def __repr__(self):
        bit_str = "".join(str(int(b)) for b in self._bits)
        return f"{self.__class__.__name__}({bit_str})"

    def __iter__(self):
        return iter(self._bits)

    def __reversed__(self):
        return BitArray(self._bits, reverse=True)

    def __getitem__(self, idx: int) -> Bit:
        return self._bits[idx]

    def __len__(self):
        return len(self._bits)

    def __and__(self, other):
        if isinstance(other, BitArray):
            return BitArray(b_0 & b_1 for b_0, b_1 in zip(self, other, strict=True))
        if isinstance(other, Bit):
            return BitArray(b & other for b in self._bits)
        raise TypeError(
            f"Can only apply logical AND to instances of {self.__class__.__name__!r} "
            "or 'Bit'."
        )

    def __rand__(self, other):
        return self.__and__(other)

    def __or__(self, other):
        if isinstance(other, BitArray):
            return BitArray(b_0 | b_1 for b_0, b_1 in zip(self, other, strict=True))
        if isinstance(other, Bit):
            return BitArray(b | other for b in self._bits)
        raise TypeError(
            f"Can only apply logical OR to instances of {self.__class__.__name__!r} "
            "or 'Bit'."
        )

    def __ror__(self, other):
        return self.__or__(other)

    def __xor__(self, other):
        if isinstance(other, BitArray):
            return BitArray(b_0 ^ b_1 for b_0, b_1 in zip(self, other, strict=True))
        if isinstance(other, Bit):
            return BitArray(b ^ other for b in self._bits)
        raise TypeError(
            f"Can only apply logical XOR to instances of {self.__class__.__name__!r} "
            "or 'Bit'."
        )

    def __rxor__(self, other):
        return self.__xor__(other)

    def __invert__(self):
        return BitArray(~b for b in self._bits)

    @property
    def bits(self) -> tuple[Bit]:
        return self._bits
