import argparse
import textwrap
from dataclasses import dataclass, field


SLIDER_CHAR = "O"
BLOCKER_CHAR = "#"


@dataclass
class Grid:
    """
    The approach here is to store the positions of round rocks (sliders) and cube rocks (blockers)
    in binary where a 1 implies the presence of an object and a 0 implies there's no object there.
    Sliding round rocks involves bit shifting the integer representing the slider rocks and then
    using otherwise bitwise operators to cut and paste the results in a way that allows only
    unblocked rocks to slide.

    Example grid, sliders, blockers, not_blockers:
    ###           000      111       000
    .O.           010      000       111
    O.#           100      001       110
    """
    width: int
    height: int
    sliders: int
    not_blockers: int  # The inverse of the '#' locations
    first_row_mask: int = field(init=False)
    last_row_mask: int = field(init=False)
    last_col_mask: int = field(init=False)

    @staticmethod
    def from_text(content: str) -> "Grid":
        width = content.find("\n")
        content = content.replace("\n", "")

        grid_sliders = int(content[0] == SLIDER_CHAR)
        grid_blockers = int(content[0] == BLOCKER_CHAR)

        for char in content[1:]:
            grid_sliders <<= 1
            grid_blockers <<= 1
            if char == SLIDER_CHAR:
                grid_sliders += 1
            elif char == BLOCKER_CHAR:
                grid_blockers += 1

        return Grid(
            width=width,
            height=len(content) // width,
            sliders=grid_sliders,
            not_blockers=~grid_blockers,
        )

    def __post_init__(self):
        self.last_row_mask = pow(2, self.width) - 1
        self.first_row_mask = self.last_row_mask << self.width * (self.height - 1)
        self.last_col_mask = 1
        for _ in range(self.height-1):
            self.last_col_mask = (self.last_col_mask << self.width) + 1

    def __str__(self) -> str:
        sliders_copy = self.sliders
        blockers_copy = ~self.not_blockers
        result = ""
        for _ in range(self.width * self.height):
            if sliders_copy & 1:
                result += SLIDER_CHAR
            elif blockers_copy & 1:
                result += BLOCKER_CHAR
            else:
                result += "."
            sliders_copy >>= 1
            blockers_copy >>= 1
        # result is reversed because the least significant bit is currently
        # first but it needs to instead be in the bottom right
        return "\n".join(textwrap.wrap(result[::-1], self.width))

    def tilt(self, func):
        """
        Call 'func' until slider state stops changing
        """
        previous_state = 0
        while previous_state != self.sliders:
            previous_state = self.sliders
            func()

    def cycle(self):
        self.tilt(self.step_north)
        self.tilt(self.step_west)
        self.tilt(self.step_south)
        self.tilt(self.step_east)

    def step_north(self):
        # Store the first row as it will slide off the edge and otherwise be lost
        first_row = self.sliders & self.first_row_mask
        # Slide everything north, ignoring collisions for the moment
        # '^ first_row' removes the first row to prevent it overflowing the grid
        naive_slide_north = (self.sliders ^ first_row) << self.width
        # Note which slides had no collisions
        keep = naive_slide_north & self.not_blockers & ~self.sliders
        # Subtract moved pieces, add keep, add back first row
        self.sliders = self.sliders & ~(keep >> self.width) | keep | first_row

    def step_south(self):
        # Store the last row as it will slide off the edge
        last_row = self.sliders & self.last_row_mask
        # Slide everything south, ignoring collisions for the moment
        # Note there's no overflow when shifting right
        naive_slide_south = self.sliders >> self.width
        # Note which slides had no collisions
        keep = naive_slide_south & self.not_blockers & ~self.sliders
        # Subtract moved pieces, add keep, add bac last row
        self.sliders = self.sliders & ~(keep << self.width) | keep | last_row

    def step_west(self):
        # Store the first row as it will slide off the edge
        first_col = self.sliders & (self.last_col_mask << self.width - 1)
        # Slide everything north, ignoring collisions for the moment
        # '^ first_col' removes the left column to prevent overflow and wrapping
        naive_slide_west = (self.sliders ^ first_col) << 1
        # Note which slides had no collisions
        keep = naive_slide_west & self.not_blockers & ~self.sliders
        # Subtract moved pieces, add keep, add back first column
        self.sliders = self.sliders & ~(keep >> 1) | keep | first_col

    def step_east(self):
        # Store the first row as it will slide off the edge
        last_col = self.sliders & self.last_col_mask
        # Slide everything north, ignoring collisions for the moment
        # '^ last_col' removes the right column to prevent wrapping
        naive_slide_east = (self.sliders ^ last_col) >> 1
        # Note which slides had no collisions
        keep = naive_slide_east & self.not_blockers & ~self.sliders
        # Subtract moved pieces, add keep, add back last column
        self.sliders = self.sliders & ~(keep << 1) | keep | last_col

    def north_load(self) -> int:
        """
        Calculate the load by counting how many bits are set in each row
        """
        total = 0
        grid_copy = self.sliders
        for row in range(self.height, 0, -1):
            total += (grid_copy & self.first_row_mask).bit_count() * row
            grid_copy = (grid_copy & ~self.first_row_mask) << self.width
        return total


def puzzle(filename):
    with open(filename, encoding="utf-8") as f:
        grid = Grid.from_text(f.read())

    # Part 1 + reset
    initial_state = grid.sliders
    grid.tilt(grid.step_north)
    part1 = grid.north_load()
    grid.sliders = initial_state

    # Part 2
    state_lookup = {}
    iterations = int(1e9)
    iteration = 0
    while iteration < iterations:
        if grid.sliders in state_lookup:
            length = iteration - state_lookup[grid.sliders]
            iteration += ((iterations - iteration) // length) * length
        else:
            state_lookup[grid.sliders] = iteration
        grid.cycle()
        iteration += 1
    part2 = grid.north_load()

    return (part1, part2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    result = puzzle(args.filename)
    print(f"{result[0]}, {result[1]}")


if __name__ == "__main__":
    main()
