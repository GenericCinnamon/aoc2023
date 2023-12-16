import sys
from typing import List


def get_diffs(history: List[int]) -> List:
    return [history[i+1] - history[i] for i in range(len(history)-1)]


def generate_derivatives(history: List[int]) -> List[List[int]]:
    history_derivatives = [history]
    # Calculate each derivative until everything is zero or we're out of numbers
    while True:
        next_derivative = get_diffs(history_derivatives[-1])
        if not next_derivative or not any(next_derivative):
            break
        history_derivatives.append(next_derivative)
    return history_derivatives


def predict_forwards(history_derivatives) -> List[List[int]]:
    # In reverse, add a number to each derivative using the higher order one
    for order, derivative in enumerate(reversed(history_derivatives)):
        if order == 0:
            continue
        next_order_derivative = history_derivatives[-order]
        derivative.append(derivative[-1] + next_order_derivative[-1])
    return history_derivatives


def predict_backwards(history_derivatives) -> List[List[int]]:
    # In reverse, prepend a number to each derivative using the higher order one
    for order, derivative in enumerate(reversed(history_derivatives)):
        if order == 0:
            continue
        next_order_derivative = history_derivatives[-order]
        derivative.insert(0, derivative[0] - next_order_derivative[0])
    return history_derivatives


def puzzle(filename):
    with open(filename, encoding="utf-8") as f:
        histories = [[int(part) for part in line.strip().split()] for line in f.readlines()]

    for history in histories:
        history_derivatives = generate_derivatives(history)
        history_derivatives = predict_forwards(history_derivatives)
        history_derivatives = predict_backwards(history_derivatives)

    part1 = sum(history[-1] for history in histories)
    part2 = sum(history[0] for history in histories)
    return (part1, part2)


def main():
    result = puzzle(sys.argv[1])
    print(f"{result[0]}, {result[1]}")


if __name__ == "__main__":
    main()
