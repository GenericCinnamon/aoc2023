import argparse
from dataclasses import dataclass
from typing import List


@dataclass
class Mapping:
    destination_range_start: int
    source_range_start: int
    range_length: int

    @staticmethod
    def from_line(line: str) -> "Mapping":
        dest, src, length = line.strip().split()
        return Mapping(
            destination_range_start=int(dest),
            source_range_start=int(src),
            range_length=int(length),
        )

    def __contains__(self, value: int):
        return self.source_range_start <= value < self.source_range_start + self.range_length

    def convert_src_to_dst(self, src: int) -> int:
        assert src in self
        return self.destination_range_start + (src - self.source_range_start)


@dataclass
class Map:
    name: str
    mappings: List[Mapping]

    @staticmethod
    def from_block(block: str) -> "Map":
        name, *lines = block.split("\n")
        return Map(name.split()[0], list(map(Mapping.from_line, lines)))

    def convert_src_to_dst(self, src: int):
        for mapping in self.mappings:
            if src in mapping:
                return mapping.convert_src_to_dst(src)
        return src


@dataclass
class Almanac:
    seeds: List[int]
    maps: List[Map]

    @staticmethod
    def from_content(content: str) -> "Almanac":
        seeds_section, *map_sections = content.split("\n\n")
        return Almanac(
            list(map(int, seeds_section.split()[1:])),
            list(map(Map.from_block, map_sections)),
        )

    def convert(self, src: int):
        for mapp in self.maps:
            src = mapp.convert_src_to_dst(src)
        return src


def puzzle(filename):
    with open(filename, "r") as f:
        almanac = Almanac.from_content(f.read())

    part1 = min((almanac.convert(s) for s in almanac.seeds))

    return (part1, 2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    print(puzzle(args.filename))
