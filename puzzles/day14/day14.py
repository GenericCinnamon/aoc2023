import argparse
from dataclasses import dataclass, field


SLIDER_CHAR = "O"
BLOCKER_CHAR = "#"


def grid_to_string(grid: int, width: int, height: int) -> str:
    num_digits = width * height
    binary_string = "{:b}".format(grid).zfill(num_digits)
    return "\n".join(binary_string[i:i+width] for i in range(0, num_digits, width))


@dataclass
class Grid:
    width: int
    height: int
    sliders: int
    blockers: int
    grid_mask: int = field(init=False)
    first_row_mask: int = field(init=False)

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
            blockers=grid_blockers,
        )

    def __post_init__(self):
        self.grid_mask = pow(2, self.width * self.height) - 1
        self.first_row_mask = (pow(2, self.width) - 1) << self.width * (self.height - 1)

    def __str__(self) -> str:
        result = ""
        for y in range(self.height):
            for x in range(self.width):
                bit_mask = pow(2, y * self.height + x)
                if self.sliders & bit_mask:
                    result += SLIDER_CHAR
                elif self.blockers & bit_mask:
                    result += BLOCKER_CHAR
                else:
                    result += "."
            result += "\n"
        # Reverse the string since the least significant bit is the start
        return result[::-1].strip()

    def step_north(self):
        """
        Slide north, find what hit a blocker, use the result to wipe out anything
        """
        # Store the first row as it will slide off the edge
        first_row = self.sliders & self.first_row_mask
        # Slide everything north, ignoring collisions for the moment
        naive_slide_north = (self.sliders ^ first_row) << self.width
        # Note which slides had no collisions
        keep = naive_slide_north & ~self.blockers & ~self.sliders
        # Remove anything which had no collisions from the original state
        self.sliders &= ~(keep >> self.width)
        # Add in things that had no collisions and add back in the first row
        self.sliders |= keep | first_row

    def north_load(self) -> int:
        total = 0
        grid_copy = self.sliders
        for row in range(self.height, 0, -1):
            total += (grid_copy & self.first_row_mask).bit_count() * row
            grid_copy = (grid_copy & ~self.first_row_mask) << self.width
        return total


def puzzle(filename):
    with open(filename) as f:
        grid = Grid.from_text(f.read())

    previous_state = 0
    while previous_state != grid.sliders:
        previous_state = grid.sliders
        grid.step_north()
    part1 = grid.north_load()

    return (part1, 2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    result = puzzle(args.filename)
    print(f"{result[0]}, {result[1]}")
