import importlib
import sys
from unittest.mock import ANY


def test(day, filename, answer):
    padded_day = str(day).zfill(2)
    puzzle = importlib.import_module(f"day{padded_day}.day{padded_day}").puzzle
    full_filename = f"puzzles/day{padded_day}/{filename}"

    full_result = puzzle(full_filename)
    for part, part_answer, result in zip([1, 2], answer, full_result):
        if part_answer == result:
            verdict = "PASS"
        else:
            verdict = f"FAIL for {filename} - {result=} != {part_answer}"
        print(f"Day {padded_day} Part {part}: {verdict}")
    return full_result == answer


if __name__ == "__main__":
    all_correct = all((
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
        # Day 04
        test(4, "test_input.txt", (13, 30)),
        test(4, "input.txt", (23441, 5923918)),
        # Day 05
        test(5, "test_input.txt", (35, 46)),
        test(5, "input.txt", (388071289, 84206669)),
        # Day 06
        test(6, "test_input.txt", (288, 71503)),
        test(6, "input.txt", (219849, 29432455)),
        # Day 07
        test(7, "test_input.txt", (6440, 5905)),
        test(7, "input.txt", (247815719, 248747492)),
        # Day 08
        test(8, "test_input.txt", (2, ANY)),
        test(8, "test_input2.txt", (6, ANY)),
        test(8, "test_input3.txt", (ANY, 6)),
        test(8, "input.txt", (17287, 18625484023687)),
        # Day 09
        test(9, "test_input.txt", (114, 2)),
        test(9, "input.txt", (1882395907, 1005)),
        # Day 10
        test(10, "test_input.txt", (8, 1)),
        test(10, "input.txt", (6931, 357)),
        # Day 14
        test(14, "test_input.txt", (136, 64)),
        test(14, "input.txt", (105208, 102943)),
        # Day 20
        test(20, "test_input.txt", (32000000, ANY)),
        test(20, "input.txt", (818723272, None)),
    ))
    sys.exit(0 if all_correct else 1)
