from collections import Counter

from puzzles.day04 import day04


def test_card_parsing():
    card = day04.Card.from_line("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19")
    assert card.card_number == 2
    assert card.winning_numbers == [13, 32, 20, 16, 61]
    assert card.our_numbers == [61, 30, 68, 82, 17, 32, 24, 19]
    assert card.wins == 2
    assert card.score == 2