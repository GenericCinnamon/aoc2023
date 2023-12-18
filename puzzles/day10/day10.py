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
    "S": (0, 0, 0, 0),
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
        start_index = 0

        north, south, east, west = NSEW_VALUES[text[0]]
        for index, char in enumerate(text[1:], 1):
            value = NSEW_VALUES[char]
            north = (north << 1) + value[0]
            south = (south << 1) + value[1]
            east = (east << 1) + value[2]
            west = (west << 1) + value[3]
            if char == "S":
                start_index = len(text) - index - 1

        # This is buggy, details around shifts are wrong
        start_mask = 1 << start_index
        south |= start_mask & (north << width)
        north |= start_mask & (south >> width)
        if start_index % width > 0:
            east |= start_mask & (west << 1)
        if start_index % width < width - 1:
            west |= start_mask & (east >> 1)

        return Pipes(
            start_index=start_index,
            north_pipes=north,
            south_pipes=south,
            east_pipes=east,
            west_pipes=west,
            width=width,
            height=len(text) // width,
        )

    def int_grid(self, value: int) -> str:
        length = self.width * self.height
        return "\n".join(textwrap.wrap(f"{value:b}".zfill(length), self.width))

    def __str__(self) -> str:
        north_copy = self.north_pipes
        south_copy = self.south_pipes
        east_copy = self.east_pipes
        west_copy = self.west_pipes
        result = ""
        for i in range(self.width * self.height):
            if i == self.start_index:
                result += "S"
            else:
                result += NSEW_CHARS.get((north_copy & 1, south_copy & 1, east_copy & 1, west_copy & 1), "*")
            north_copy >>= 1
            south_copy >>= 1
            east_copy >>= 1
            west_copy >>= 1
        # length = self.width * self.height
        # # n = "\n".join(textwrap.wrap(f"{self.north_pipes:b}".zfill(length), self.width))
        # # s = "\n".join(textwrap.wrap(f"{self.south_pipes:b}".zfill(length), self.width))
        # # e = "\n".join(textwrap.wrap(f"{self.east_pipes:b}".zfill(length), self.width))
        # # w = "\n".join(textwrap.wrap(f"{self.west_pipes:b}".zfill(length), self.width))
        # # return f"n\n{n}\ns\n{s}\ne\n{e}\nw\n{w}\n" + '\n'.join(textwrap.wrap(result[::-1], self.width))
        return "\n".join(textwrap.wrap(result[::-1], self.width))

    def fill(self) -> int:
        bottom_row = pow(2, self.width) - 1
        top_row = bottom_row << (self.height - 1) * self.width
        right_col = 1
        for _ in range(self.height-1):
            right_col <<= self.width
            right_col += 1
        left_col = right_col << self.width - 1

        fill = 1 << self.start_index
        previous_fill = 0
        while fill != previous_fill:
            previous_fill = fill
            # print(self.int_grid(fill & ~right_col & self.east_pipes))
            # Go east
            fill |= (fill & ~right_col & self.east_pipes) >> 1 & self.west_pipes
            # Go west
            fill |= (fill & ~left_col & self.west_pipes) << 1 & self.east_pipes
            # Go north
            fill |= (fill & ~top_row & self.north_pipes) << self.width & self.south_pipes
            # Go south
            fill |= (fill & ~bottom_row & self.south_pipes) >> self.width & self.north_pipes

        # Starting with the left column
        
        # Chickened out a did this bit by bit, there's surely a way to do this in one sweep
        # Track whether there's an even or odd number of | pipes hit at each stage
        # Crossing a | means you're inside, crossing the next means outside, then repeat for - and &
        # TODO BUGGY
        horizontal_sweep = 0
        vertical_pipes = self.north_pipes | self.south_pipes
        for x in range(self.width-1):
            current_col = left_col >> x
            horizontal_sweep |= current_col & ((current_col & horizontal_sweep) >> 1) ^ (current_col & vertical_pipes & fill)
        vertical_sweep = 0
        horizontal_pipes = self.east_pipes | self.west_pipes
        for y in range(self.height-1):
            current_row = top_row >> (self.width * y)
            vertical_sweep |=current_row & ((vertical_sweep >> self.width) ^ (current_row & horizontal_pipes & fill))

        inside = horizontal_sweep & vertical_sweep & ~fill
        part1 = fill.bit_count() // 2
        part2 = inside.bit_count()

        print("Path/fill")
        print(self.int_grid(fill))
        print("horizontal sweep")
        print(self.int_grid(horizontal_sweep))
        print("vertical sweep")
        print(self.int_grid(vertical_sweep))
        print("inside")
        print(self.int_grid(inside))

        return part1, part2


def puzzle(filename):
    with open(filename, encoding="utf-8") as f:
        pipes = Pipes.from_text(f.read())
    return (pipes.fill())


def main():
    result = puzzle(sys.argv[1])
    print(f"{result[0]}, {result[1]}")


if __name__ == "__main__":
    main()
