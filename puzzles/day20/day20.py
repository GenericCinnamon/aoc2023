import argparse
import itertools
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

LOW_PULSE = False
HIGH_PULSE = True


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

    def pulse(self, incoming: Pulse) -> List[Pulse]:
        return []


@dataclass
class Broadcaster(Component):
    def pulse(self, incoming: Pulse) -> List[Pulse]:
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
    changes: int = 0

    def pulse(self, incoming: Pulse) -> List[Pulse]:
        self.changes += 1
        if incoming.value == HIGH_PULSE:
            return []

        self.state = not self.state
        return [
            Pulse(self.name, output_name, self.state)
            for output_name in self.outputs
        ]


@dataclass
class Nand(Component):
    input_history: Dict[str, bool] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        for name in self.inputs:
            self.input_history[name] = LOW_PULSE

    def pulse(self, incoming: Pulse):
        self.input_history[incoming.from_name] = incoming.value
        # Using the fact that HIGH_PULSE is True, LOW_PULSE is False
        value = not all((value for value in self.input_history.values()))
        return [
            Pulse(self.name, output_name, value)
            for output_name in self.outputs
        ]


COMPONENT_TYPES = {
    "%": FlipFlop,
    "b": Broadcaster,
    "&": Nand,
    "rx": Component,
}


@dataclass
class Circuit:
    components: Dict[str, Component]
    flip_flop_count: int

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
            },
            flip_flop_count=len([name for name, typ in component_types.items() if typ == "%"]),
        )

    def __str__(self) -> str:
        result = ""
        for name, component in self.components.items():
            inputs = ", ".join(component.inputs)
            outputs = ", ".join(component.outputs)
            result += f"{name} -> {outputs} (receives from {inputs})\n"
        return result

    def flop_state(self) -> str:
        result = 0
        change_counts = []
        for name, component in self.components.items():
            if type(component) is FlipFlop:
                result <<= 1
                result += int(component.state)
                change_counts.append(component.changes)
        return result, change_counts

    def part1(self, times: int) -> Tuple[int, int]:
        counter = {HIGH_PULSE: 0, LOW_PULSE: 0}
        for _ in range(times):
            pulse_queue = deque([Pulse("button", "roadcaster", LOW_PULSE)])
            while pulse_queue:
                pulse: Pulse = pulse_queue.popleft()
                counter[pulse.value] += 1
                if pulse.to_name not in self.components:
                    continue
                new_pulses = self.components[pulse.to_name].pulse(pulse)
                pulse_queue.extend(new_pulses)
        return counter[HIGH_PULSE] * counter[LOW_PULSE]


def puzzle(filename):
    with open(filename, encoding="utf-8") as f:
        circuit = Circuit.from_text(f.read())
    part1 = circuit.part1(1000)
    part2 = None
    return part1, part2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    result = puzzle(args.filename)
    print(f"{result[0]}, {result[1]}")


if __name__ == "__main__":
    main()
