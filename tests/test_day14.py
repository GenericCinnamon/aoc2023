import pytest

from puzzles.day14.day14 import Grid


@pytest.fixture
def example_input():
    return """\
        O....#....
        O.OO#....#
        .....##...
        OO.#O....O
        .O.....O#.
        O.#..O.#.#
        ..O..#O..O
        .......O..
        #....###..
        #OO..#....""".replace(" ", "")


def test_loading(example_input):
    assert str(Grid.from_text(example_input)) == example_input
