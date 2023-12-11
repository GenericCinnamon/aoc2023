from unittest.mock import ANY

import pytest

from puzzles.day05.day05 import Almanac, Map, Mapping, Range


@pytest.fixture
def almanac() -> Almanac:
    with open("puzzles/day05/test_input.txt") as f:
        return Almanac.from_content(f.read())


def test_almanac_parsing(almanac: Almanac):
    assert almanac.maps[0].name == "seed-to-soil"
    assert almanac.maps[1].name == "soil-to-fertilizer"

    mappings = almanac.maps[0].mappings
    assert mappings[0].destination_range.lower == 50
    assert mappings[0].destination_range.upper == 52

    assert mappings[0].source_range.lower == 98
    assert mappings[0].source_range.upper == 100

    assert mappings[1].destination_range.lower == 52
    assert mappings[1].destination_range.upper == 100
    assert mappings[1].source_range.lower == 50
    assert mappings[1].source_range.upper == 98


def test_mapping():
    mapped = Mapping(Range(0, 100), Range(0, 100)).convert_src_to_dst(Range(10, 11))
    assert mapped[0].length == mapped[2].length == 0
    assert mapped[1] == Range(10, 11)

    mapped = Mapping(Range(1000, 1050), Range(100, 150)).convert_src_to_dst(Range(50, 200))
    assert mapped[0] == Range(50, 100)
    assert mapped[1] == Range(1000, 1050)
    assert mapped[2] == Range(150, 200)


def test_map():
    m = Map(
        "",
        [
            Mapping(Range(1000, 1050), Range(100, 150)),
            Mapping(Range(0, 1), Range(1001, 1002)),
        ]
    )
    assert m.convert_src_to_dst(Range(101, 102)) == [Range(1001, 1002)]
    assert m.convert_src_to_dst(Range(149, 151)) == [Range(1049, 1050), Range(150, 151)]


def test_conversion(almanac: Almanac):
    assert almanac.convert(Range(79, 80)) == [Range(82, 83)]
    assert almanac.convert(Range(14, 15)) == [Range(43, 44)]
    assert almanac.convert(Range(55, 56)) == [Range(86, 87)]
    assert almanac.convert(Range(13, 14)) == [Range(35, 36)]
