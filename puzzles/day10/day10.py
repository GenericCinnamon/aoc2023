import sys
import textwrap
from dataclasses import dataclass


NSEW_VALUES = {
    "|": (1, 1, 0, 0),
    "-": (0, 0, 1, 1),
    "J": (1, 0, 0, 1),
    "7": (0, 1, 0, 1),
    "F": (0, 1, 1, 0),
    "L": (1, 0, 1, 0),
    "S": (1, 1, 1, 1),
    ".": (0, 0, 0, 0),
}
NSEW_CHARS = {value: key for key, value in NSEW_VALUES.items()}


@dataclass
class Pipes:
    start_index: int
    north_pipes: int  # |, J, L
    east_pipes: int  # -, L, F
    south_pipes: int  # |, F, 7
    west_pipes: int  # -, J, 7
    width: int
    height: int

    @staticmethod
    def from_text(text: str) -> "Pipes":
        width = text.find("\n")
        text = text.replace("\n", "")
        start_index = -1

        north, south, east, west = NSEW_VALUES[text[0]]
        for index, char in enumerate(text[1:], 1):
            value = NSEW_VALUES[char]
            north = (north << 1) + value[0]
            south = (south << 1) + value[1]
            east = (east << 1) + value[2]
            west = (west << 1) + value[3]
            if char == "S":
                start_index = index - index // (width + 1)

        return Pipes(
            start_index=start_index,
            north_pipes=north,
            south_pipes=south,
            east_pipes=east,
            west_pipes=west,
            width=width,
            height=len(text) // width,
        )

    def __str__(self) -> str:
        north_copy = self.north_pipes
        south_copy = self.south_pipes
        east_copy = self.east_pipes
        west_copy = self.west_pipes
        result = ""
        for i in range(self.width * self.height):
            if i == self.start_index:
                result += "S"
                continue
            result += NSEW_CHARS[(north_copy & 1, south_copy & 1, east_copy & 1, west_copy & 1)]
            north_copy >>= 1
            south_copy >>= 1
            east_copy >>= 1
            west_copy >>= 1
        # result is reversed because the least significant bit is currently
        # first but it needs to instead be in the bottom right
        return "\n".join(textwrap.wrap(result[::-1], self.width))


def puzzle(filename):
    with open(filename, encoding="utf-8") as f:
        pipes = Pipes.from_text(f.read())
    print(pipes)
    return (1, 2)


def main():
    result = puzzle(sys.argv[1])
    print(f"{result[0]}, {result[1]}")


if __name__ == "__main__":
    main()
