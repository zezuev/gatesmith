
from ..engine import circuit, LogicOperation
from .bit import Bit
from .gate import Not


class Switch(Bit):

    def __init__(self):
        super().__init__(circuit.create_gate(LogicOperation.create_id(), 0))
        self._set_input(self._id, 0)

    def toggle(self):
        self._set_state(not self.state)

    def power_on(self):
        if not self.state:
            self.toggle()

    def power_off(self):
        if self.state:
            self.toggle()


def create_switches(n: int) -> tuple[Switch, ...]:
    return tuple(Switch() for _ in range(n))


class Clock(Bit):

    def __init__(self, span: int | None = None):
        super().__init__()
        # construct clock from inverter masked with a switch
        not_0 = Not(delay=span if span is not None else circuit["SPAN_CLOCK"])
        not_0.in_0 = not_0
        self._s_0 = Switch()
        and_0 = self._s_0 & not_0
        self._set_id(and_0.id_)

    def toggle(self):
        self._s_0.toggle()

    def power_on(self):
        self._s_0.power_on()

    def power_off(self):
        self._s_0.power_off()
