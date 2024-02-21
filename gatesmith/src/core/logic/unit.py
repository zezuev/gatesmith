
from collections.abc import Iterable
import numpy as np
from numpy.typing import NDArray
from .operator import Operator
from .auxiliary import extend_array


INIT_LEN = 32
COMPONENT_ID = -1
INPUT_IDS = slice(-1)


class CircuitUnit:

    def __init__(self, op: Operator, delay: int):
        self._op = op
        self._delay = delay

        self._state = np.ndarray((delay + 1, INIT_LEN), dtype=np.bool_)
        self._state_pos = 0

        self._ids = np.ndarray((op.num_inputs + 1, INIT_LEN), dtype=np.int32)
        self._next_idx = 0

    def update(self, global_state: NDArray[np.bool_]):
        inputs = [
            global_state[self._ids[input_idx, :self._next_idx]]
            for input_idx in range(self._op.num_inputs)
        ]
        future_state = self._op(inputs)
        future_pos = self._get_future_pos(self._delay)
        self._state[future_pos, :self._next_idx] = future_state
        self._state_pos = self._get_future_pos(1)

    def create_component(self, component_id: int, input_ids: Iterable[int] | None = None):
        component_idx = self._generate_idx(component_id)
        for input_idx, input_id in enumerate(input_ids or []):
            self._ids[input_idx, component_idx] = input_id

    def get_state(self, component_id: int) -> bool:
        component_idx = self._get_idx_by_id(component_id)
        return self._state[self._state_pos, component_idx]

    def set_state(self, component_id: int, new_state: bool, delay: int):
        component_idx = self._get_idx_by_id(component_id)
        future_pos = self._get_future_pos(delay)
        self._state[future_pos, component_idx] = new_state

    def set_input_ids(self, component_id: int, input_ids: Iterable[int]):
        component_idx = self._get_idx_by_id(component_id)
        for input_idx, input_id in enumerate(input_ids):
            self._ids[input_idx, component_idx] = input_id

    def set_input_id(self, component_id: int, input_idx: int, input_id: int):
        component_idx = self._get_idx_by_id(component_id)
        self._ids[input_idx, component_idx] = input_id

    def get_input_ids(self, component_id: int) -> tuple[int, ...]:
        component_idx = self._get_idx_by_id(component_id)
        return tuple(self._ids[INPUT_IDS, component_idx])

    def get_input_id(self, component_id: int, input_idx: int) -> int:
        component_idx = self._get_idx_by_id(component_id)
        return self._ids[input_idx, component_idx]

    def update_input_id(self, old_id: int, new_id: int):
        self._ids[INPUT_IDS, :self._next_idx] = np.where(
            self._ids[INPUT_IDS, :self._next_idx] == old_id,
            new_id,
            self._ids[INPUT_IDS, :self._next_idx],
        )

    def _get_future_pos(self, delay: int) -> int:
        return (self._state_pos + delay) % (self._delay + 1)

    def _get_idx_by_id(self, component_id: int) -> int:
        return np.searchsorted(self._ids[COMPONENT_ID, :self._next_idx], component_id)

    def _generate_idx(self, component_id: int) -> int:
        new_idx = self._next_idx
        if new_idx == self._state.shape[1]:
            self._state = extend_array(self._state)
            self._ids = extend_array(self._ids)

        self._state[:, new_idx] = False
        self._ids[INPUT_IDS, new_idx] = 0
        self._ids[COMPONENT_ID, new_idx] = component_id
        self._next_idx += 1
        return new_idx

    @property
    def state(self) -> NDArray[np.bool_]:
        return self._state[self._state_pos, :self._next_idx]

    @property
    def component_ids(self) -> NDArray[np.int32]:
        return self._ids[COMPONENT_ID, :self._next_idx]
