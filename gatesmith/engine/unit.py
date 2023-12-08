
import numpy as np
from .logic import LogicOperation
from .auxiliary import double_width

_INIT_LEN = 32
_MEMBER_ROW = -1
_INPUT_ROWS = slice(-1)


class CircuitSimulationUnit:

    def __init__(self, op: LogicOperation, delay: int):
        self._op = op
        self._delay = delay

        self._state = np.ndarray((delay + 1, _INIT_LEN), dtype=np.bool_)
        self._state_pos = 0
        self._ids = np.ndarray((self._op.num_inputs + 1, _INIT_LEN), dtype=np.int32)
        self._next_idx = 0

    def update(self, global_state: np.ndarray[np.bool_]):
        """Update the state of all simulation unit members."""
        inputs = [  # fetch input state vectors from global state vector
            global_state[self._ids[input_idx, :self._next_idx]]
            for input_idx in range(self._op.num_inputs)
        ]
        # compute and save future state
        new_state = self._op(*inputs)
        update_pos = self._get_delayed_pos(self._delay)
        self._state[update_pos, :self._next_idx] = new_state
        # shift state position one step into the future
        self._state_pos = self._get_delayed_pos(1)

    def remap_id(self, virtual_id: int, new_id: int):
        """Remap all occurences of `virtual_id` in the input vectors to `new_id`."""
        self._ids[_INPUT_ROWS, :self._next_idx] = np.where(
            self._ids[_INPUT_ROWS, :self._next_idx] == virtual_id,
            new_id,
            self._ids[_INPUT_ROWS, :self._next_idx],
        )

    def create_gate(self, member_id: int):
        """Create a new gate within the simulation unit."""
        idx = self._generate_idx()
        self._state[:, idx] = False
        self._ids[_MEMBER_ROW, idx] = member_id
        self._ids[_INPUT_ROWS, idx] = 0  # constant False id

    def set_state(self, id_: int, new_state: bool, delay = 0):
        """Force-set a state of a member gate."""
        idx = self._get_idx_by_id(id_)
        self._state[self._get_delayed_pos(delay), idx] = new_state

    def set_input(self, id_: int, input_id: int, input_idx: int):
        """Set an input id of a member gate."""
        idx = self._get_idx_by_id(id_)
        self._ids[input_idx, idx] = input_id

    def get_input_id(self, id_: int, input_idx: int) -> int:
        """Get an input id of a member gate."""
        idx = self._get_idx_by_id(id_)
        return self._ids[input_idx, idx]

    def _get_delayed_pos(self, delay: int) -> int:
        """Get the index of a future state vector position."""
        return (self._state_pos + delay) % (self._delay + 1)

    def _get_idx_by_id(self, id_: int) -> int:
        """Get a member index by its id."""
        return np.searchsorted(self._ids[_MEMBER_ROW, :self._next_idx], id_)

    def _generate_idx(self) -> int:
        """Generate a new member index, possibly allocating new resources."""
        idx = self._next_idx
        if idx == self._state.shape[1]:
            self._state = double_width(self._state)
            self._ids = double_width(self._ids)
        self._next_idx += 1
        return idx

    @property
    def state(self) -> np.ndarray[np.bool_]:
        """The current state of all members of the simulation unit."""
        return self._state[self._state_pos, :self._next_idx]

    @property
    def ids(self) -> np.ndarray[np.int32]:
        """The ids of all members of the simulation unit."""
        return self._ids[_MEMBER_ROW, :self._next_idx]

    @property
    def op(self) -> LogicOperation:
        return self._op
