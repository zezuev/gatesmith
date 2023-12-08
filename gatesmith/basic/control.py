
from typing import Sequence, Literal
from .bit import Bit, BitLike, convert_to_bit
from .bitarray import BitArray


def zeros_padding[T](x: tuple[T], n: int, dir_: Literal["l", "r"] = "l") -> tuple[T]:
    k = n - len(x)
    if k < 0:
        raise ValueError("Not enough space left for padding.")
    padding = tuple(0 for _ in range(k))
    if dir_ == "l":
        return padding + x
    return x + padding


class Mux(Bit):

    def __init__(self, x: Sequence[Bit] | BitArray, s: Bit | BitArray):
        super().__init__()
        if not isinstance(x, BitArray):
            x = BitArray(x)
        if isinstance(s, Bit):
            s = BitArray((s,))
        if len(x) > 2**len(s):
            raise ValueError("Not enough selection lines for multiplexer.")
    
        layer = BitArray(x.bits + tuple(0 for _ in range(2**len(s) - len(x))))
        for s_i in reversed(s):
            layer = BitArray(
                (layer[2*i] & ~s_i) | (layer[2*i+1] & s_i)
                for i in range(len(layer) // 2)
            )
        self._set_id(layer[0].id_)


class MultiMux(BitArray):

    def __init__(self, x: BitArray | Sequence[BitArray], s: Bit | BitArray):
        if isinstance(x, BitArray):
            x = [x]
        else:
            x = [*x]
        if isinstance(s, Bit):
            s = BitArray((s,))
        if len(x) > 2**len(s):
            raise ValueError("Not enough selection lines for multiplexer.")

        layer = x + [BitArray(n=len(x[0])) for _ in range(2**len(s) - len(x))]
        for s_i in reversed(s):
            layer = [
                (layer[2*i] & ~s_i) | (layer[2*i+1] & s_i)
                for i in range(len(layer) // 2)
            ]
        self._set_bits(layer[0].bits)
