import sys
from collections import Counter


# Converts 2-9,T,J,Q,K,A to 2-9,a,b,c,d,e so that strings
# can be sorted according to value. i.e. A < K < Q < J < T etc.
SORTABLE_CARD_TRANSLATION = {
    ord('T'): ord('a'),
    ord('J'): ord('b'),
    ord('Q'): ord('c'),
    ord('K'): ord('d'),
    ord('A'): ord('e'),
}
# For part 2 the joker is converted to the lowest value
PART2_JOKER_TRANSLATION = {
    ord('b'): ord('0'),
}


FIVE_OF_A_KIND = '7'
FOUR_OF_A_KIND = '6'
FULL_HOUSE = '5'
THREE_OF_A_KIND = '4'
TWO_PAIR = '3'
ONE_PAIR = '2'
HIGH_CARD = '1'


def hand_type(card_counter):
    most_common = card_counter.most_common()
    unique_cards = len(most_common)
    cards_in_best_group = most_common[0][1]

    # The type of hand can be identified by the number of unique cards
    # and how many cards are in the largest group
    match unique_cards, cards_in_best_group:
        case 5, _:
            return HIGH_CARD
        case 4, _:
            return ONE_PAIR
        case 1, _:
            return FIVE_OF_A_KIND
        case 3, 2:
            return TWO_PAIR
        case 3, 3:
            return THREE_OF_A_KIND
        case 2, 3:
            return FULL_HOUSE
        case 2, 4:
            return FOUR_OF_A_KIND
        case _, _:
            # Should be impossible unless given an invalid hand
            assert False, "Unknown hand type"


class Hand:
    def __init__(self, line):
        # Example line: '32T3K 765'
        cards, bid = line.split()
        self.bid = int(bid)
        translated_cards = cards.translate(SORTABLE_CARD_TRANSLATION)

        # Part 1, prefix hand type to translated cards to make a value which can be used to sort
        card_counter = Counter(cards)
        hand_type_part1 = hand_type(card_counter)
        self.sortable_cards_part1 = hand_type_part1 + translated_cards

        # Part 2, add the joker count to the most common other card, then do the same thing as part 1
        joker_count = card_counter["J"]
        if joker_count == 0:
            # No changes, re-use result
            self.sortable_cards_part2 = self.sortable_cards_part1
        elif joker_count == 5:
            # All jokers, 5 of a kind
            self.sortable_cards_part2 = FIVE_OF_A_KIND + '00000'
        else:
            del card_counter["J"]
            card_counter[card_counter.most_common()[0][0]] += joker_count
            hand_type_part2 = hand_type(card_counter)
            self.sortable_cards_part2 = hand_type_part2 + translated_cards.translate(PART2_JOKER_TRANSLATION)


def puzzle(filename):
    with open(filename, "r") as f:
        hands = [Hand(line) for line in f.readlines()]

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
    if len(sys.argv) != 2:
        print("Usage: day07.py FILENAME\nPrints '(part 1 answer, part 2 answer)'")
        sys.exit(1)
    print(puzzle(sys.argv[1]))
