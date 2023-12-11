import argparse
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Range:
    lower: int  # inclusive
    upper: int  # not-inclusive
    length: int = field(init=False)

    def __post_init__(self):
        self.length = max(0, self.upper - self.lower)


@dataclass
class Mapping:
    destination_range: Range
    source_range: Range

    @staticmethod
    def from_line(line: str) -> "Mapping":
        dest, src, range_length = line.strip().split()
        length = int(range_length)
        dest_int = int(dest)
        src_int = int(src)
        return Mapping(
            destination_range=Range(dest_int, dest_int + length),
            source_range=Range(src_int, src_int + length),
        )

    def convert_src_to_dst(self, src: Range) -> Tuple[Range, Range, Range]:
        """
        src :            x----------------x
        source_range:        o-------o
        Divides into at most three new ranges.
        This function always returns three ranges,
        however some may have zero or negative length and should thus be ignored
        """
        lower_unmapped = Range(src.lower, min(src.upper, self.source_range.lower))
        upper_unmapped = Range(max(src.lower, self.source_range.upper), src.upper)
        to_map = Range(max(src.lower, self.source_range.lower), min(src.upper, self.source_range.upper))
        mapped = Range(
            self.destination_range.lower + (to_map.lower - self.source_range.lower),
            self.destination_range.lower + (to_map.upper - self.source_range.lower),
        )

        assert src.length == lower_unmapped.length + mapped.length + upper_unmapped.length

        return lower_unmapped, mapped, upper_unmapped


@dataclass
class Map:
    name: str
    mappings: List[Mapping]

    @staticmethod
    def from_block(block: str) -> "Map":
        name, *lines = block.split("\n")
        return Map(name.split()[0], list(map(Mapping.from_line, lines)))

    def convert_src_to_dst(self, src: Range) -> List[Range]:
        done: List[Range] = []
        todo = [src]
        for mapping in self.mappings:
            next_todo = []
            for range in todo:
                lower_unmapped, mapped, upper_unmapped = mapping.convert_src_to_dst(range)
                if mapped.length > 0:
                    done.append(mapped)
                if lower_unmapped.length > 0:
                    next_todo.append(lower_unmapped)
                if upper_unmapped.length > 0:
                    next_todo.append(upper_unmapped)
                assert lower_unmapped.length or mapped.length or upper_unmapped.length
            todo = next_todo
        done.extend(todo)

        lengths = sum((r.length for r in done))
        assert lengths == src.length, f"{lengths=} != {src.length=}"
        return done


@dataclass
class Almanac:
    part1_seeds: List[Range]
    part2_seeds: List[Range]
    maps: List[Map]

    @staticmethod
    def from_content(content: str) -> "Almanac":
        seeds_section, *map_sections = content.split("\n\n")
        seed_ints = list(map(int, seeds_section.split()[1:]))
        part1_seeds = [Range(s, s+1) for s in seed_ints]
        part2_seeds = [Range(seed_ints[i], seed_ints[i] + seed_ints[i+1]) for i in range(0, len(seed_ints), 2)]
        return Almanac(
            part1_seeds,
            part2_seeds,
            list(map(Map.from_block, map_sections)),
        )

    def convert(self, seed: Range) -> List[Range]:
        seeds = [seed]
        for mapp in self.maps:
            next_seeds = []
            for s in seeds:
                next_seeds.extend(mapp.convert_src_to_dst(s))
            seeds = next_seeds
        return seeds


def puzzle(filename):
    with open(filename, "r") as f:
        almanac = Almanac.from_content(f.read())

    part1 = min((
        result.lower
        for s in almanac.part1_seeds
        for result in almanac.convert(s)
    ))
    part2 = min((
        result.lower
        for s in almanac.part2_seeds
        for result in almanac.convert(s)
    ))

    return (part1, part2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    print(puzzle(args.filename))
