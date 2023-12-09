import argparse
from collections import Counter
from dataclasses import dataclass

# Converts 2-9,T,J,Q,K,A to 2-9,a,b,c,d,e so that strings
# can be sorted according to value. i.e. A < K < Q < J < T etc.
SORTABLE_CARD_TRANSLATION = {
    ord('T'): ord('a'),
    ord('J'): ord('b'),
    ord('Q'): ord('c'),
    ord('K'): ord('d'),
    ord('A'): ord('e'),
}


FIVE_OF_A_KIND = '7'
FOUR_OF_A_KIND = '6'
FULL_HOUSE = '5'
THREE_OF_A_KIND = '4'
TWO_PAIR = '3'
ONE_PAIR = '2'
HIGH_CARD = '1'


def hand_type(card_counter: Counter) -> str:
    most_common = card_counter.most_common()
    unique_cards = len(most_common)
    if unique_cards == 5:
        return HIGH_CARD
    elif unique_cards == 4:
        return ONE_PAIR
    elif unique_cards == 3:
        # Either two pair, or three of a kind
        _, cards_in_best_group = most_common[0]
        if cards_in_best_group == 2:
            return TWO_PAIR
        assert cards_in_best_group == 3
        return THREE_OF_A_KIND
    elif unique_cards == 2:
        # Either a full house, or four of a kind
        _, cards_in_best_group = most_common[0]
        if cards_in_best_group == 3:
            return FULL_HOUSE

        assert cards_in_best_group == 4
        return FOUR_OF_A_KIND

    # Five of a kind
    assert unique_cards == 1
    return FIVE_OF_A_KIND


@dataclass
class Hand:
    cards: str
    sortable_cards_part1: str
    sortable_cards_part2: str
    bid: int

    @staticmethod
    def from_line(line: str) -> "Hand":
        # Example line: '32T3K 765'
        cards, bid = line.strip().split()
        card_counter = Counter(cards)
        translated_cards = cards.translate(SORTABLE_CARD_TRANSLATION)
        # Part 1, prefix hand with the type of hand it is to make it sortable
        hand_type_part1 = hand_type(card_counter)
        sortable_cards_part1 = hand_type_part1 + translated_cards

        # Part 2, count the jokers and add them to the most common other card
        joker_count = card_counter["J"]
        if joker_count == 0:
            hand_type_part2 = hand_type_part1
        elif joker_count == 5:
            hand_type_part2 = FIVE_OF_A_KIND
        else:
            del card_counter["J"]
            card_counter[card_counter.most_common()[0][0]] += joker_count
            hand_type_part2 = hand_type(card_counter)
        sortable_cards_part2 = hand_type_part2 + translated_cards.replace("b", "0")  # Jokers are now worth the least

        return Hand(
            cards=cards,
            sortable_cards_part1=sortable_cards_part1,
            sortable_cards_part2=sortable_cards_part2,
            bid=int(bid),
        )


def puzzle(filename):
    with open(filename, "r") as f:
        hands = [Hand.from_line(line) for line in f.readlines()]

    part1_sorted = sorted(hands, key=lambda h: h.sortable_cards_part1)
    part1 = sum((
        (index+1) * hand.bid
        for index, hand in enumerate(part1_sorted)
    ))

    part2_sorted = sorted(hands, key=lambda h: h.sortable_cards_part2)
    part2 = sum((
        (index+1) * hand.bid
        for index, hand in enumerate(part2_sorted)
    ))

    return (part1, part2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    print(puzzle(args.filename))
