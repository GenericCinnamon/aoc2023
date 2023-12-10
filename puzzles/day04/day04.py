import argparse
from dataclasses import dataclass, field
from typing import List


@dataclass
class Card:
    card_number: int
    winning_numbers: List[int]
    our_numbers: List[int]
    wins: int = field(init=False)
    score: int = field(init=False)
    count: int = field(init=False, default=1)

    def __post_init__(self):
        self.wins = sum((
            1 if num in self.winning_numbers else 0
            for num in self.our_numbers
        ))
        self.score = 2**(self.wins-1) if self.wins else 0

    @staticmethod
    def from_line(line: str) -> "Card":
        card_info, numbers = line.strip().split(":")
        _, card_number = card_info.split()
        winning_numbers, our_numbers = numbers.split("|")
        winning_numbers_split = winning_numbers.split()
        our_numbers_split = our_numbers.split()

        return Card(
            card_number=int(card_number),
            winning_numbers=[int(n) for n in winning_numbers_split],
            our_numbers=[int(n) for n in our_numbers_split],
        )


def puzzle(filename):
    with open(filename, "r") as f:
        cards = [Card.from_line(line) for line in f.readlines()]
    part1 = sum((card.score for card in cards))

    for index, card in enumerate(cards):
        for bonus_card in cards[index+1:index+1+card.wins]:
            bonus_card.count += card.count
    part2 = sum((card.count for card in cards))

    return (part1, part2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    print(puzzle(args.filename))
