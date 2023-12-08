
basic types:
    - BitArrays from decimal and hex
    - Quine McCluskey solver and builder
    - make __eq__ return a new BitArray

basic components:
    - generalized MUX
        - N:M
        - use cascade from simple 2:1 Mux or Multi-Mux
        - use recursive implementation

    Mux(x, y, s)  # regular 2:1 MUX
    MultiMux(b_0, b_1, s)  # 2:1 MUX of BitArrays
    # perhaps it could be an ArrayMux instead
    # a more general version could be:
    Mux((x, y), s)  # x, y and s can be Bit or BitArray now
    Mux((x, y, z), s)
    Mux(x, z)  # choose from BitArray x

    # Decoder/Demux
    - cascade from simple 1:2 Demux
    - use interface analogous to that of Mux
    # Demux and MultiDemux (for arrays)

    - comparator
    - NOR-based latches and flops
    - DLatch

complex components:
    - barrel shifter with multiplexers
    - CLAG adder
    - general adder/subtractor like on F. 287
    - carry-save adder and multiplier
    - UniversalRegister
    - RAM
    - Anlauf-RISC with 64 addresses (6 Bit per address)




    a = BitArray((0,0,1,1,0,0,1,1))
    b = BitArray((1,1,0,1,0,1,0,0))
    c = BitArray((1,0,0,1,1,0,1,1))
    s_1 = BitArray((1,0,1))
    s_2 = Bit(0)
    s_3 = BitArray((0,1))

    mux_0 = Mux(a, s_1)  # choose position 6 from a
    mux_1 = MultiMux((a, b), s_2)  # choose a
    mux_2 = MultiMux((a, b, c), s_3)  # choose b


    class Mux:

        def __init__(
                self,
                x: Sequence[Bit] | BitArray,
                s: Bit | BitArray,
        ):
            if not isinstance(x, BitArray):
                x = BitArray(x)

            ...
