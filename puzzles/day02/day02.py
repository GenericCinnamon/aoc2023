import argparse
from dataclasses import dataclass
from typing import List, Type


@dataclass
class CubeSet:
    red: int
    green: int
    blue: int

    @classmethod
    def from_string(cls: Type["CubeSet"], cube_string: str) -> "CubeSet":
        amount_color_pairs = (
            part.strip().split(" ", maxsplit=1)
            for part in cube_string.strip().split(",")
        )
        values = {
            color: int(amount)
            for amount, color in amount_color_pairs
        }
        return CubeSet(
            red=values.get("red", 0),
            green=values.get("green", 0),
            blue=values.get("blue", 0),
        )

    def has_fewer_or_equal_cubes(self, other: "CubeSet") -> bool:
        return self.red <= other.red and self.green <= other.green and self.blue <= other.blue

    @property
    def power(self) -> int:
        return self.red * self.green * self.blue


@dataclass
class Game:
    game_id: int
    cube_sets: List[CubeSet]

    @classmethod
    def from_string(cls: Type["Game"], game_string: str) -> "Game":
        game_id_str, cube_sets_str = game_string.split(":")

        return Game(
            game_id=int(game_id_str.split(" ")[1]),
            cube_sets=[CubeSet.from_string(set_str) for set_str in cube_sets_str.split(";")],
        )

    def cube_set_is_possible(self, cubeset: CubeSet) -> bool:
        return all((
            c.has_fewer_or_equal_cubes(cubeset) for c in self.cube_sets
        ))

    def minimum_cubeset_required(self) -> CubeSet:
        return CubeSet(
            red=max((c.red for c in self.cube_sets)),
            green=max((c.green for c in self.cube_sets)),
            blue=max((c.blue for c in self.cube_sets)),
        )


def puzzle(filename):
    with open(filename, "r") as f:
        games = [
            Game.from_string(line.strip())
            for line in f
        ]
    part1_cubeset = CubeSet(red=12, green=13, blue=14)
    part1 = sum((
        g.game_id
        for g in games
        if g.cube_set_is_possible(part1_cubeset)
    ))
    part2 = sum((
        g.minimum_cubeset_required().power
        for g in games

    ))
    return (part1, part2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    print(puzzle(args.filename))
