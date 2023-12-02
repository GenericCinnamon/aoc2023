import importlib
from unittest.mock import ANY


def test(day, filename, answer):
    padded_day = str(day).zfill(2)
    puzzle = importlib.import_module(f"day{padded_day}.day{padded_day}").puzzle
    result = puzzle(filename)
    if result == answer:
        print(f"Day {padded_day}: PASS for {filename}")
    else:
        print(f"Day {padded_day}: FAIL for {filename} : {result=} != {answer}")


if __name__ == "__main__":
    # Day 01
    test(1, "puzzles/day01/test_input1.txt", (142, 142))
    test(1, "puzzles/day01/test_input2.txt", (ANY, 281))
    test(1, "puzzles/day01/input.txt", (57346, 57345))
    # Day 02
    test(2, "puzzles/day02/test_input1.txt", (8, 2286))
    test(2, "puzzles/day02/input.txt", (2237, 2286))
