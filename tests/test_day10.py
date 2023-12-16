import pytest

from puzzles.day10.day10 import Pipes


@pytest.fixture
def example_input():
    return """\
        7-F7-
        .FJ|7
        SJLL7
        |F--J
        LJ.LJ\
        """.replace(" ", "")


@pytest.fixture
def pipes(example_input):
    return Pipes.from_text(example_input)


def test_loading(example_input):
    pipes = Pipes.from_text(example_input)
    pipes.start_index = -1
    assert str(pipes) == example_input
