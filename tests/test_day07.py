from collections import Counter

from puzzles.day07 import day07
from puzzles.day07.day07 import hand_type, Hand, SORTABLE_CARD_TRANSLATION


def test_card_translation_sorting():
    chars = [
        h.translate(SORTABLE_CARD_TRANSLATION)
        for h in [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "T",
        "J",
        "Q",
        "K",
        "A"
    ]]
    assert chars == sorted(chars)


def test_five_of_a_kind():
    assert hand_type(Counter("11111")) == day07.FIVE_OF_A_KIND


def test_four_of_a_kind():
    assert hand_type(Counter("11112")) == day07.FOUR_OF_A_KIND


def test_full_house():
    assert hand_type(Counter("11122")) == day07.FULL_HOUSE


def test_three_of_a_kind():
    assert hand_type(Counter("11123")) == day07.THREE_OF_A_KIND


def test_two_pair():
    assert hand_type(Counter("11223")) == day07.TWO_PAIR


def test_one_pair():
    assert hand_type(Counter("11234")) == day07.ONE_PAIR


def test_high_card():
    assert hand_type(Counter("12345")) == day07.HIGH_CARD


def test_ordering():
    assert day07.FIVE_OF_A_KIND > day07.FOUR_OF_A_KIND > day07.FULL_HOUSE > day07.TWO_PAIR > day07.ONE_PAIR > day07.HIGH_CARD
