
from typing import Callable
import numpy as np
from numpy.typing import NDArray


type OperatorFunction = Callable[[tuple[NDArray[np.bool_], ...]], NDArray[np.bool_]]

class Operator:

    def __init__(self, func: OperatorFunction, operator_id: str, num_inputs: int):
        self._func = func
        self._operator_id = operator_id
        self._num_inputs = num_inputs

    def __call__(self, inputs: tuple[NDArray[np.bool_], ...]) -> NDArray[np.bool_]:
        if len(inputs) == self._num_inputs:
            return self._func(inputs)
        raise TypeError(
            f"Operator object takes {self._num_inputs} inputs, but {len(inputs)} were provided."
        )

    def __hash__(self):
        return hash((self._operator_id, self._num_inputs))

    def __eq__(self, other):
        if isinstance(other, Operator):
            return (self._operator_id, self._num_inputs) == (other.operator_id, other.num_inputs)
        return False

    @classmethod
    def create_not(cls):
        return Operator(np.logical_not, "NOT", 1)

    @classmethod
    def create_id(cls):
        return Operator(lambda inputs: inputs[0], "ID", 1)

    @classmethod
    def create_and(cls, num_inputs: int = 2):
        return Operator(np.logical_and.reduce, "AND", num_inputs)

    @classmethod
    def create_nand(cls, num_inputs: int = 2):
        nand_func = lambda inputs: ~np.logical_and.reduce(inputs)
        return Operator(nand_func, "NAND", num_inputs)

    @classmethod
    def create_or(cls, num_inputs: int = 2):
        return Operator(np.logical_or.reduce, "OR", num_inputs)

    @classmethod
    def create_nor(cls, num_inputs: int = 2):
        nor_func = lambda inputs: ~np.logical_or.reduce(inputs)
        return Operator(nor_func, "NOR", num_inputs)

    @classmethod
    def create_xor(cls, num_inputs: int = 2):
        xor_func = lambda inputs: sum(inputs) == 1
        return Operator(xor_func, "XOR", num_inputs)

    @classmethod
    def create_eq(cls, num_inputs: int = 2):
        eq_func = lambda inputs: (sum(inputs) % num_inputs) == 0
        return Operator(eq_func, "EQ", num_inputs)

    @property
    def operator_id(self) -> str:
        return self._operator_id

    @property
    def num_inputs(self) -> int:
        return self._num_inputs
