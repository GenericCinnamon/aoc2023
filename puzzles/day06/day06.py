import argparse
import math


def get_score_for_hold_time(race_time, hold_time):
    return (float(race_time) - float(hold_time)) * float(hold_time)


def get_hold_times_for_score(race_time, score):
    race_time = float(race_time)
    modifier = math.sqrt(race_time*race_time - 4.0 * score)
    return (race_time - modifier) / 2.0, (race_time + modifier) / 2.0


def get_best_hold_time(race_time):
    best_hold_float = float(race_time) / 2.0
    floor = math.floor(best_hold_float)
    ceil = math.ceil(best_hold_float)

    score_for_floor = get_score_for_hold_time(race_time, floor)
    score_for_ceil = get_score_for_hold_time(race_time, ceil)

    if score_for_floor > score_for_ceil:
        return floor
    else:
        return ceil


def get_distance_for_best_hold_time(race_time):
    # Theoretically it is race_time * race_time / 4, however we are limited to integer holding times
    return get_score_for_hold_time(race_time, get_best_hold_time(race_time))


def get_better_hold_times(race_time, distance_record):
    record_hold_times = get_hold_times_for_score(race_time, distance_record)
    best_score_possible = get_distance_for_best_hold_time(race_time)

    if best_score_possible <= distance_record:
        return 0

    # Doesn't seem to hold for record hold times both at the same number, ceil(4-1) = 3, floor(4+1) = 5
    return math.ceil(record_hold_times[1] - 1) - math.floor(record_hold_times[0] + 1) + 1


def puzzle(filename):
    with open(filename, "r") as f:
        _, *times = f.readline().strip().split()
        _, *distances = f.readline().strip().split()
    part1_times = map(int, times)
    part2_time = int("".join(times))
    part1_distances = map(int, distances)
    part2_distance = int("".join(distances))

    part1 = 1
    for (race_time, distance_record) in zip(part1_times, part1_distances):
        part1 *= get_better_hold_times(race_time, distance_record)

    part2 = get_better_hold_times(part2_time, part2_distance)

    return (part1, part2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    print(puzzle(args.filename))
