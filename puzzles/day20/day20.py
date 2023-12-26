import argparse
import math
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Iterable, Set

LOW_PULSE = False
HIGH_PULSE = True
BUTTON = "button"
BROADCASTER = "roadcaster"


@dataclass
class Pulse:
    from_name: str
    to_name: str
    value: bool


@dataclass
class Component:
    name: str
    inputs: List[str]
    outputs: List[str]

    def pulse(self, _incoming: Pulse) -> Iterable[Pulse]:
        return []

    def reset(self) -> None:
        pass


@dataclass
class Broadcaster(Component):
    def pulse(self, incoming: Pulse) -> Iterable[Pulse]:
        return [
            Pulse(
                from_name=self.name,
                to_name=output_name,
                value=incoming.value
            )
            for output_name in self.outputs
        ]


@dataclass
class FlipFlop(Component):
    state: bool = LOW_PULSE

    def pulse(self, incoming: Pulse) -> Iterable[Pulse]:
        if incoming.value == HIGH_PULSE:
            return []

        self.state = not self.state
        return (
            Pulse(self.name, output_name, self.state)
            for output_name in self.outputs
        )

    def reset(self) -> None:
        self.state = LOW_PULSE


@dataclass
class Nand(Component):
    input_history: Dict[str, bool] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        self.reset()

    def pulse(self, incoming: Pulse) -> Iterable[Pulse]:
        self.input_history[incoming.from_name] = incoming.value
        # Using the fact that HIGH_PULSE is True, LOW_PULSE is False
        value = not all((value for value in self.input_history.values()))
        return (
            Pulse(self.name, output_name, value)
            for output_name in self.outputs
        )

    def reset(self) -> None:
        for name in self.inputs:
            self.input_history[name] = LOW_PULSE

    def time_till_next_switch(self, circuit: "Circuit") -> int:
        # If all inputs are Nands their outputs will all align once they all switch at the same time
        if set(self.inputs) <= circuit.nands:
            return math.lcm(
                *(
                    circuit.components[input_name].time_till_next_switch(circuit)  # type:ignore
                    for input_name in self.inputs
                )
            )

        # Otherwise we need to simulate the incoming circuit until it loops
        upstream_components = circuit.find_upstream_components(self.name)
        return circuit.find_subnetwork_periodicity(upstream_components)


COMPONENT_TYPES = {
    "%": FlipFlop,
    "b": Broadcaster,
    "&": Nand,
    "rx": Component,
}
COMPONENT_SYMBOLS = {value: key for key, value in COMPONENT_TYPES.items()}


@dataclass
class Circuit:
    components: Dict[str, Component]
    flip_flops: Set[str] = field(init=False)
    nands: Set[str] = field(init=False)

    @staticmethod
    def from_text(text: str) -> "Circuit":
        component_types: Dict[str, str] = {}
        component_inputs: Dict[str, List[str]] = {}
        component_outputs: Dict[str, List[str]] = {}

        for line in text.splitlines():
            # Break the line in parts: 'component_part -> output_part'
            component_part, _, output_part = line.strip().split(maxsplit=2)
            c_name = component_part[1:]  # The broadcaster's is name 'roadcaster', I'm ok with this
            component_types[c_name] = component_part[0]
            component_outputs[c_name] = output_part.split(", ")
            for output_name in output_part.split(", "):
                component_inputs.setdefault(output_name, []).append(c_name)
        component_types.setdefault("rx", "rx")

        return Circuit(
            components={
                name: COMPONENT_TYPES[typ](
                    name=name,
                    inputs=component_inputs.get(name, []),
                    outputs=component_outputs.get(name, []),
                )
                for name, typ in component_types.items()
            }
        )

    def __post_init__(self) -> None:
        self.flip_flops = {
            name
            for name, component in self.components.items()
            if isinstance(component, FlipFlop)
        }
        self.nands = {
            name
            for name, component in self.components.items()
            if isinstance(component, Nand)
        }

    def reset(self) -> None:
        for c in self.components.values():
            c.reset()

    def __str__(self) -> str:
        result = ""
        for name, component in self.components.items():
            symbol = COMPONENT_SYMBOLS[type(component)]
            inputs = ", ".join(component.inputs)
            outputs = ", ".join(component.outputs)
            result += f"{symbol}{name} -> {outputs} (receives from {inputs})\n"
        return result

    def part1(self, times: int) -> int:
        counter = {HIGH_PULSE: 0, LOW_PULSE: 0}
        for _ in range(times):
            pulse_queue = deque([Pulse(BUTTON, BROADCASTER, LOW_PULSE)])
            while pulse_queue:
                pulse: Pulse = pulse_queue.popleft()
                counter[pulse.value] += 1
                if pulse.to_name not in self.components:
                    continue
                new_pulses = self.components[pulse.to_name].pulse(pulse)
                pulse_queue.extend(new_pulses)
        return counter[HIGH_PULSE] * counter[LOW_PULSE]

    def part2(self) -> int:
        rx = self.components["rx"]
        assert len(rx.inputs) == 1, "Only works if rx has one input"
        rx_input = self.components[rx.inputs[0]]
        assert isinstance(rx_input, Nand), "Only works if rx's input is a nand"
        return rx_input.time_till_next_switch(self)

    def find_upstream_components(self, start: str) -> Set[str]:
        seen: Set[str] = set()
        queue: Set[str] = {start}
        while queue:
            item = queue.pop()
            inputs = set(self.components[item].inputs)
            queue.update(inputs - seen)
            seen.update(inputs)
        return seen

    def ff_state(self, flip_flops: List[FlipFlop]):
        state = 0
        for ff in flip_flops:
            state = (state + ff.state) << 1
            state <<= 1
        return state

    def find_subnetwork_periodicity(self, subnetwork: Set[str]) -> int:
        """
        Find how long it takes for all the flipflops in the subnetwork to start repeating
        """
        assert BROADCASTER in subnetwork, "broadcaster must be in the subnetwork"
        self.reset()
        flip_flops: List[FlipFlop] = [
            self.components[component]  # type:ignore
            for component in self.flip_flops.intersection(subnetwork)
        ]
        ff_states: Set[int] = set()

        iteration = 0
        state = 0
        while state not in ff_states:
            ff_states.add(state)
            iteration += 1

            # Run the subnetwork
            pulse_queue = deque([Pulse(BUTTON, BROADCASTER, LOW_PULSE)])
            while pulse_queue:
                pulse: Pulse = pulse_queue.popleft()
                if pulse.to_name not in subnetwork:
                    continue
                new_pulses = self.components[pulse.to_name].pulse(pulse)
                pulse_queue.extend(new_pulses)
            state = self.ff_state(flip_flops)

        return iteration


def puzzle(filename):
    with open(filename, encoding="utf-8") as f:
        circuit = Circuit.from_text(f.read())
    part1 = circuit.part1(1000)
    part2 = circuit.part2()
    return part1, part2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    result = puzzle(parser.parse_args().filename)
    print(f"{result[0]}, {result[1]}")


if __name__ == "__main__":
    main()
