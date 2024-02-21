
from collections.abc import Iterable
import numpy as np
from numpy.typing import NDArray
from .operator import Operator
from .unit import CircuitUnit
from .auxiliary import extend_array


INIT_LEN = 32
type UnitType = tuple[Operator, int]


class CircuitManager:

    def __init__(self):
        self._state = np.ndarray(INIT_LEN, dtype=np.bool_)
        self._next_id = 0
        self._units: dict[UnitType, CircuitUnit] = {}
        self._unit_by_id: dict[int, CircuitUnit] = {}
        self._wire_ids: set[int] = set()

        self._state[[0, 1]] = [False, True]
        self._next_id += 2

    def update(self, iterations: int = 1):
        for _ in range(iterations):
            for unit in self._units.values():
                unit.update(self._state[:self._next_id])
            for unit in self._units.values():
                self._state[unit.component_ids] = unit.state

    def create_component(
            self,
            op: Operator,
            delay: int,
            input_ids: Iterable[int] | None = None,
    ) -> int:
        component_id = self._generate_id()
        unit = self._units.setdefault((op, delay), CircuitUnit(op, delay))
        unit.create_component(component_id, input_ids)
        self._unit_by_id[component_id] = unit
        return component_id

    def create_wire(self) -> int:
        if self._wire_ids:
            return self._wire_ids.pop()
        return self._generate_id()

    def connect_wire(self, wire_id: int, input_id: int):
        for unit in self._units.values():
            unit.update_input_id(wire_id, input_id)
        self._wire_ids.add(wire_id)

    def set_input_ids(self, component_id: int, input_ids: Iterable[int]):
        self._unit_by_id[component_id].set_input_ids(input_ids)

    def set_input_id(self, component_id: int, input_idx: int, input_id: int):
        self._unit_by_id[component_id].set_input_id(component_id, input_idx, input_id)

    def get_input_ids(self, component_id: int) -> tuple[int, ...]:
        return self._unit_by_id[component_id].get_input_ids(component_id)

    def get_input_id(self, component_id: int, input_idx: int) -> int:
        return self._unit_by_id[component_id].get_input_id(component_id, input_idx)

    def set_state(self, component_id: int, new_state: bool, delay: int = 0):
        if delay == 0:
            self._state[component_id] = new_state
        else:
            self._unit_by_id[component_id].set_state(component_id, new_state, delay)

    def get_state(self, component_id: int) -> bool:
        if component_id in [0, 1]:
            return self._state[component_id]
        return self._unit_by_id[component_id].get_state(component_id)

    def _generate_id(self) -> int:
        new_id = self._next_id
        if new_id == len(self._state):
            self._state = extend_array(self._state)

        self._state[new_id] = False
        self._next_id += 1
        return new_id

    @property
    def state(self) -> NDArray[np.bool_]:
        return self._state[:self._next_id]
