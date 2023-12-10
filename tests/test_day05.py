import pytest

from puzzles.day05.day05 import Almanac, Map, Mapping


@pytest.fixture
def almanac() -> Almanac:
    with open("puzzles/day05/test_input.txt") as f:
        return Almanac.from_content(f.read())


def test_almanac_parsing(almanac: Almanac):
    assert almanac.maps[0].name == "seed-to-soil"
    assert almanac.maps[1].name == "soil-to-fertilizer"

    mappings = almanac.maps[0].mappings
    assert mappings[0].destination_range_start == 50
    assert mappings[0].source_range_start == 98
    assert mappings[0].range_length == 2

    assert mappings[1].destination_range_start == 52
    assert mappings[1].source_range_start == 50
    assert mappings[1].range_length == 48


def test_mapping():
    assert 10 in Mapping(0, 0, 100)
    assert 10 not in Mapping(11, 5, 4)
    assert 10 in Mapping(0, 10, 1)
    assert 10 not in Mapping(0, 9, 1)

    assert Mapping(0, 0, 100).convert_src_to_dst(10) == 10
    assert Mapping(0, 10, 100).convert_src_to_dst(10) == 0
    assert Mapping(10, 0, 100).convert_src_to_dst(20) == 30


def test_map():
    m = Map("", [Mapping(5, 10, 10), Mapping(100, 200, 1)])
    assert m.convert_src_to_dst(-1) == -1
    assert m.convert_src_to_dst(15) == 10


def test_conversion(almanac: Almanac):
    assert almanac.convert(79) == 82
    assert almanac.convert(14) == 43
    assert almanac.convert(55) == 86
    assert almanac.convert(13) == 35
