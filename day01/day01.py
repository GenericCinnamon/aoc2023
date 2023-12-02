import argparse


WORD_REPLACEMENTS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def puzzle(filename):
    sum_part1 = 0
    sum_part2 = 0
    with open(filename, "r") as f:
        for line in f:
            part1_digits = []
            part2_digits = []
            for i in range(len(line)):
                char = line[i]
                if '0' <= char <= '9':
                    value = int(char)
                    part1_digits.append(value)
                    part2_digits.append(value)
                    continue
                
                for string, digit in WORD_REPLACEMENTS.items():
                    if line[i:].startswith(string):
                        part2_digits.append(digit)
                        break

            sum_part1 += part1_digits[0] * 10 + part1_digits[-1] if part1_digits else 0
            sum_part2 += part2_digits[0] * 10 + part2_digits[-1]

    print(sum_part1)
    print(sum_part2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    puzzle(args.filename)
