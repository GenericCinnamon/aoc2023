import importlib
from unittest.mock import ANY


def test(day, filename, answer):
    padded_day = str(day).zfill(2)
    puzzle = importlib.import_module(f"day{padded_day}.day{padded_day}").puzzle
    full_filename = f"puzzles/day{padded_day}/{filename}"

    full_result = puzzle(full_filename)
    for part, part_answer, result in zip([1, 2], answer, full_result):
        verdict = "PASS" if part_answer == result else "FAIL" + f" for {filename} - {result=} != {part_answer}"
        print(f"Day {padded_day} Part {part}: {verdict}")
    return full_result == answer


if __name__ == "__main__":
    exit(int(not all((
        # Day 01
        test(1, "test_input1.txt", (142, 142)),
        test(1, "test_input2.txt", (ANY, 281)),
        test(1, "input.txt", (57346, 57345)),
        # Day 02
        test(2, "test_input1.txt", (8, 2286)),
        test(2, "input.txt", (2237, 66681)),
        # Day 03
        test(3, "test_input.txt", (4361, 467835)),
        test(3, "input.txt", (531561, 83279367)),
        # Day 07
        test(7, "test_input.txt", (6440, 5905)),
        test(7, "input.txt", (247815719, 248747492)),
    ))))
