
from typing import Callable
import numpy as np


class LogicOperation:

    def __init__(self, func: Callable, num_inputs: int, ident: str):
        self._func = func
        self._num_inputs = num_inputs
        self._ident = ident

    def __call__(self, *inputs: np.ndarray[np.bool_]) -> np.ndarray[np.bool_]:
        if self._num_inputs == 1:
            return self._func(inputs[0])
        return self._func(inputs)

    def __hash__(self):
        return hash((self._num_inputs, self._ident))

    def __eq__(self, other):
        if isinstance(other, LogicOperation):
            return (self._num_inputs, self._ident) == (other.num_inputs, other.ident)
        return False

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(ident={self._ident!r}, "
            f"num_inputs={self._num_inputs})"
        )

    @property
    def num_inputs(self) -> int:
        return self._num_inputs

    @property
    def ident(self) -> str:
        return self._ident

    @classmethod
    def create_id(cls):
        """Create an identity operator."""
        return cls(lambda x: x, 1, "ID")

    @classmethod
    def create_and(cls, num_inputs = 2):
        return cls(np.logical_and.reduce, num_inputs, "AND")

    @classmethod
    def create_or(cls, num_inputs = 2):
        return cls(np.logical_or.reduce, num_inputs, "OR")

    @classmethod
    def create_not(cls):
        return cls(np.logical_not, 1, "NOT")

    @classmethod
    def create_xor(cls, num_inputs = 2):
        return cls(np.logical_xor.reduce, 2, "XOR")

    @classmethod
    def create_nor(cls, num_inputs = 2):
        return cls(lambda inputs: ~np.logical_or.reduce(inputs), num_inputs, "NOR")

    @classmethod
    def create_nand(cls, num_inputs = 2):
        return cls(lambda inputs: ~np.logical_and.reduce(inputs), num_inputs, "NAND")
