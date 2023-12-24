import sys
import textwrap
from dataclasses import dataclass
from typing import List, Tuple


# North, South, East, West
UP = 0b1000
DOWN = 0b0100
LEFT = 0b0001
RIGHT = 0b0010
UP_DOWN = UP | DOWN
LEFT_RIGHT = LEFT | RIGHT
UP_RIGHT = UP | RIGHT
UP_LEFT = UP | LEFT
DOWN_RIGHT = DOWN | RIGHT
DOWN_LEFT = DOWN | LEFT
EMPTY = 0


NSEW_VALUES = {
    "|": UP_DOWN,
    "-": LEFT_RIGHT,
    "J": UP_LEFT,
    "7": DOWN_LEFT,
    "F": DOWN_RIGHT,
    "L": UP_RIGHT,
    ".": EMPTY,
    "S": EMPTY,
}
NSEW_CHARS = {value: key for key, value in NSEW_VALUES.items()}


@dataclass
class Network:
    pipes: List[int]
    width: int
    height: int
    start_index: int

    @staticmethod
    def from_text(text: str) -> "Network":
        width = text.find("\n") + 2
        text = text.replace("\n", "..")
        text = f"{'.' * width}.{text}.{'.' * width}"
        height = len(text) // width
        start_index = text.find("S")
        pipes: List[int] = []

        for char in text:
            pipes.append(NSEW_VALUES[char])

        left = bool(pipes[start_index-1] & RIGHT)
        right = bool(pipes[start_index+1] & LEFT)
        up = bool(pipes[start_index-width] & DOWN)
        down = bool(pipes[start_index+width] & UP)
        pipes[start_index] = left * LEFT | right * RIGHT | up * UP | down * DOWN

        return Network(
            pipes=pipes,
            width=width,
            height=height,
            start_index=start_index,
        )

    def int_grid(self, value: int) -> str:
        length = self.width * self.height
        return "\n".join(textwrap.wrap(f"{value:b}".zfill(length)[::-1], self.width))

    def __str__(self) -> str:
        result = ""
        for i, pipe in enumerate(self.pipes):
            if i and i % self.width == 0:
                result += "\n"
            result += NSEW_CHARS[pipe]
        return result

    def fill(self) -> Tuple[int, int]:
        cursor_pos = self.start_index
        fill_grid = 0
        left_grid = 0
        right_grid = 0
        previous_dir = 0

        # Trace out the whole path, keeping track of what is on the left and right
        while not fill_grid & (1 << cursor_pos):
            fill_grid |= 1 << cursor_pos
            pipe = self.pipes[cursor_pos]
            if pipe & UP and previous_dir != DOWN:
                # Move up
                left_grid |= (1 << cursor_pos - 1)
                right_grid |= (1 << cursor_pos + 1)
                cursor_pos -= self.width
                previous_dir = UP
            elif pipe & DOWN and previous_dir != UP:
                # Move down
                left_grid |= (1 << cursor_pos + 1)
                right_grid |= (1 << cursor_pos - 1)
                cursor_pos += self.width
                previous_dir = DOWN
            elif pipe & RIGHT and previous_dir != LEFT:
                # Move right
                left_grid |= (1 << cursor_pos - self.width)
                right_grid |= (1 << cursor_pos + self.width)
                cursor_pos += 1
                previous_dir = RIGHT
            else:
                assert pipe & LEFT and previous_dir != RIGHT
                # Move left
                left_grid |= (1 << cursor_pos + self.width)
                right_grid |= (1 << cursor_pos - self.width)
                cursor_pos -= 1
                previous_dir = LEFT

        # part 1 is half the length of the path
        part1 = fill_grid.bit_count() // 2
        part2 = self.count_inside(fill_grid, left_grid, right_grid)

        return part1, part2

    def count_inside(self, fill_grid, left_grid, right_grid):
        # For part 2, flood fill the left and right paths
        bottom_row = pow(2, self.width) - 1
        top_row = bottom_row << (self.height - 1) * self.width
        right_col = 1
        for _ in range(self.height-1):
            right_col <<= self.width
            right_col += 1
        left_col = right_col << self.width - 1

        left_grid &= ~fill_grid
        right_grid &= ~fill_grid

        for _ in range(self.width):
            left_grid |= (left_grid & ~right_col) >> 1
            left_grid |= (left_grid & ~left_col) << 1
            left_grid |= (left_grid & ~bottom_row) >> self.width
            left_grid |= (left_grid & ~top_row) << self.width
            left_grid &= ~fill_grid
            right_grid |= (right_grid & ~right_col) >> 1
            right_grid |= (right_grid & ~left_col) << 1
            right_grid |= (right_grid & ~bottom_row) >> self.width
            right_grid |= (right_grid & ~top_row) << self.width
            right_grid &= ~fill_grid

        # Part 2 is now the number of bits in the inside fill
        if left_grid & 1:
            return right_grid.bit_count()
        assert right_grid & 1
        return left_grid.bit_count()


def puzzle(filename):
    with open(filename, encoding="utf-8") as f:
        pipes = Network.from_text(f.read())
    return pipes.fill()


def main():
    result = puzzle(sys.argv[1])
    print(f"{result[0]}, {result[1]}")


if __name__ == "__main__":
    main()
