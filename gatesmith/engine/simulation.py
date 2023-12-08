
from typing import Sequence
import numpy as np
from .logic import LogicOperation
from .unit import CircuitSimulationUnit
from .auxiliary import double_width


_INIT_LEN = 32
_BASE_SETTINGS = {
    # preset delays
    "DELAY_NOT": 1,
    "DELAY_AND": 1,
    "DELAY_OR": 1,
    "DELAY_NAND": 1,
    "DELAY_NOR": 1,
    "DELAY_XOR": 1,
    "DELAY_EQ": 1,

    # preset spans
    "SPAN_CLOCK": 5,
}

type UnitType = tuple[LogicOperation, int]  # operation-delay


class CircuitSimulation:

    def __init__(self):
        self._state = np.ndarray(_INIT_LEN, dtype=np.bool_)
        self._units: dict[UnitType, CircuitSimulationUnit] = {}
        self._unit_by_id: dict[int, CircuitSimulationUnit] = {}
        self._settings = _BASE_SETTINGS.copy()
        self._free_virtual_ids: set[int] = set()
        self._next_id = 0

        # initialize constants
        # constants are the only components managed directly by the main simulation class
        self._state[[0, 1]] = [False, True]
        self._next_id += 2

    def update(self, iterations = 1):
        """Update the circuit state by a certain number of iterations."""
        for _ in range(iterations):
            # update states of all units
            for unit in self._units.values():
                unit.update(self._state[:self._next_id])
            # assemble global state from unit states
            for unit in self._units.values():
                self._state[unit.ids] = unit.state

    def set_state(self, id_: int, new_state: bool, delay = 0):
        """Set the state of a circuit component to `new_state`. The effect can
        be delayed by varying `delay`, provided that the corresponding simulation
        unit supports it."""
        if delay == 0:  # perform real-time update of global state
            self._state[id_] = new_state
        else:
            # perform update of state within corresponding simulation unit
            unit = self._unit_by_id[id_]
            unit.set_state(id_, new_state, delay)

    def get_state(self, id_: int) -> bool:
        """Get the current state of a circuit component. This is equivalent to
        retrieving it by using the circuit's `state` property."""
        return self._state[id_]

    def set_input(self, id_: int, input_id: int, input_idx: int):
        """Set an input of circuit component."""
        unit = self._unit_by_id[id_]
        unit.set_input(id_, input_id, input_idx)

    def get_input_id(self, id_: int, input_idx: int) -> int:
        """Get an input id of a circuit component."""
        unit = self._unit_by_id[id_]
        return unit.get_input_id(id_, input_idx)

    def get_num_inputs(self, id_: int) -> int:
        if id_ in self._unit_by_id:
            unit = self._unit_by_id[id_]
            return unit.op.num_inputs
        return 0  # constant or virtual id

    def create_gate(
            self,
            op: LogicOperation,
            delay: int,
            inputs: Sequence[int] | None = None,
    ) -> int:
        """Create a new logic gate within the circuit."""
        new_id = self._generate_id()

        unit = self._units.setdefault((op, delay), CircuitSimulationUnit(op, delay))
        unit.create_gate(new_id)  # add gate to simulation unit
        self._unit_by_id[new_id] = unit

        for idx, id_ in enumerate(inputs or []):  # process eventual inputs
            unit.set_input(new_id, id_, idx)
        return new_id

    def create_wire(self) -> int:
        """Create a new wire within the circuit. Wires have virtual ids which are
        remapped once an input is connected."""
        if self._free_virtual_ids:  # reuse a previously generated virtual id
            return self._free_virtual_ids.pop()
        return self._generate_id()  # generate a new virtual id

    def remap_id(self, virtual_id: int, new_id: int):
        """Remap all occurences of `virtual_id` within the simulation to `new_id`."""
        for unit in self._units.values():
            unit.remap_id(virtual_id, new_id)
        self._free_virtual_ids.add(virtual_id)

    def __getitem__(self, key: str) -> int:
        return self._settings[key]

    def __setitem__(self, key: str, val: int):
        self._settings[key] = val

    def _generate_id(self) -> int:
        new_id = self._next_id
        if new_id == len(self._state):
            self._state = double_width(self._state)
        self._state[new_id] = False
        self._next_id += 1
        return new_id

    @property
    def state(self) -> np.ndarray[np.bool_]:
        """The current state of the circuit."""
        return self._state[:self._next_id]

    @property
    def ncomps(self) -> int:
        return self._next_id
