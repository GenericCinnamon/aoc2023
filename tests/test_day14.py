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
        #OO..#....\
        """.replace(" ", "")


@pytest.fixture
def grid(example_input):
    return Grid.from_text(example_input)


def test_loading(example_input):
    assert str(Grid.from_text(example_input)) == example_input


def test_shift_noth(grid):
    grid.step_north()
    assert str(grid) == """\
    O.OO.#....
    O...#....#
    OO..O##..O
    ...#...O..
    OO...O..#.
    ..#...O#.#
    ..O..#.O.O
    ..........
    #OO..###..
    #....#....\
    """.replace(" ", "")


def test_shift_south(grid):
    grid.step_south()
    assert str(grid) == """\
    O....#....
    ....#....#
    O.OO.##...
    .O.#......
    O...O..O#O
    .O#..O.#.#
    O....#....
    ..O...OO.O
    #....###..
    #OO..#....\
    """.replace(" ", "")


def test_shift_east(grid):
    grid.step_east()
    assert str(grid) == """\
    .O...#....
    .OOO#....#
    .....##...
    O.O#.O...O
    ..O....O#.
    .O#...O#.#
    ...O.#.O.O
    ........O.
    #....###..
    #O.O.#....\
    """.replace(" ", "")


def test_shift_west(grid):
    grid.step_west()
    assert str(grid) == """\
    O....#....
    OO.O#....#
    .....##...
    OO.#O...O.
    O.....O.#.
    O.#.O..#.#
    .O...#O.O.
    ......O...
    #....###..
    #OO..#....\
    """.replace(" ", "")
