import argparse
import math
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple


RULE_RE = re.compile(r"(?P<name>[A-Z0-9]+) = \((?P<left_name>[A-Z0-9]+), ?(?P<right_name>[A-Z0-9]+)\)")


@dataclass
class Rule:
    name: str
    left_name: str
    right_name: str
    left: "Rule" = field(init=False)
    right: "Rule" = field(init=False)

    @staticmethod
    def from_lines(lines: List[str]) -> List["Rule"]:
        rules: Dict[str, Rule] = {}
        for line in lines:
            match = RULE_RE.match(line)
            assert match
            groups = match.groupdict()
            rules[groups["name"]] = Rule(**groups)

        for rule in rules.values():
            rule.left = rules[rule.left_name]
            rule.right = rules[rule.right_name]

        return list(rules.values())

    def __eq__(self, other: Any) -> bool:
        if type(other) is not Rule:
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"{self.name} = ({self.left_name}, {self.right_name})"


@dataclass
class PathTracker:
    starting_rule: Rule
    ending_rule: Rule
    index_of_start: int
    start_of_repeat: Rule
    last_rule_before_repeat: Rule
    length_of_loop: int
    finish_offset: int


def puzzle(filename):
    with open(filename, "r") as f:
        instructions, _, *rule_lines = f.read().split("\n")
    instruction_count = len(instructions)
    rules = Rule.from_lines(rule_lines)

    start_rules = [
        rule
        for rule in rules
        if rule.name.endswith("A")
    ]

    part1 = 0
    path_lengths = []

    for start_rule in start_rules:
        node = start_rule
        instruction_index = 0
        seen: Dict[Tuple[Rule, int], int] = {}
        while True:
            if node == node.left == node.right:
                break
            instruction_offset = instruction_index % instruction_count
            instruction = instructions[instruction_offset]
            state = (node, instruction_offset)
            if state in seen:
                break
            seen[state] = instruction_index
            node = node.left if instruction == "L" else node.right
            instruction_index += 1
            if node.name.endswith("Z"):
                path_lengths.append(instruction_index)
                if node.name.endswith("ZZZ"):
                    part1 = instruction_index

    part2 = math.lcm(*path_lengths)

    return (part1, part2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    print(puzzle(args.filename))
