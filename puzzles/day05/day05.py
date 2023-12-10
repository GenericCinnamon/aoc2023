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
        dest, src, length = line.split()
        return Mapping(
            destination_range_start=int(dest),
            source_range_start=int(src),
            length=int(length),
        )

    def __contains__(self, value: int):
        return self.source_range_start <= value <= self.source_range_start + value

    def convert_src_to_dst(self, src: int) -> int:
        assert src in self
        return self.destination_range_start + (src - self.source_range_start)


@dataclass
class Map:
    mappings: List[Mapping]

    @staticmethod
    def from_block(self, block: str) -> "Map":
        pass


def puzzle(filename):
    return (1, 2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    print(puzzle(args.filename))
