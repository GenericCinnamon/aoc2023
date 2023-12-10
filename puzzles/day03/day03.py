import argparse
from typing import List, Set


class PartNumber:
    max_part_id: int = 0

    def __init__(self):
        self.value = 0
        self.part_id = self.max_part_id
        PartNumber.max_part_id += 1

    @classmethod
    def reset(cls):
        cls.max_part_id = 0

    def __repr__(self) -> str:
        return f"{self.value:3d} ({self.part_id:03d})"

    def __hash__(self) -> int:
        return self.part_id


class Symbol:
    symbols: List["Symbol"] = []

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.adjacent_parts: Set[PartNumber] = set()
        Symbol.symbols.append(self)

    @classmethod
    def reset(cls):
        cls.symbols = []

    def __repr__(self) -> str:
        return self.symbol


def puzzle(filename: str):
    PartNumber.reset()
    Symbol.reset()
    null_part = PartNumber()
    null_symbol = Symbol('')
    part_map: List[List[PartNumber]] = []
    symbol_map: List[List[Symbol]] = []

    with open(filename, "r") as f:
        lines = f.readlines()

    width = len(lines[0].strip())

    for y, line in enumerate(lines):
        part_map.append([])
        symbol_map.append([])
        current_part: PartNumber = null_part
        for x, char in enumerate(line.strip()):
            if '0' <= char <= '9':
                symbol_map[-1].append(null_symbol)
                if current_part == null_part:
                    current_part = PartNumber()
                current_part.value = current_part.value*10 + (ord(char) - ord('0'))
                for check_x, check_y in ((x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y)):
                    if check_x < 0 or check_y < 0 or check_x >= width:
                        continue
                    symbol = symbol_map[check_y][check_x]
                    if symbol == null_symbol:
                        continue
                    symbol.adjacent_parts.add(current_part)
            else:
                symbol = Symbol(char)
                for check_x, check_y in ((x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y)):
                    if check_x < 0 or check_y < 0 or check_x >= width:
                        continue
                    part = part_map[check_y][check_x]
                    if part == null_part:
                        continue
                    symbol.adjacent_parts.add(part)
                symbol_map[-1].append(symbol)
                current_part = null_part
            part_map[-1].append(current_part)

    all_adjacent = {
        part
        for symbol in Symbol.symbols
        for part in symbol.adjacent_parts
        if symbol.symbol != '.' and symbol != null_symbol
    }
    part1 = sum((part.value for part in all_adjacent))

    part2 = 0
    for symbol in Symbol.symbols:
        if symbol.symbol != "*":
            continue
        if len(symbol.adjacent_parts) != 2:
            continue
        a, b = list(symbol.adjacent_parts)
        part2 += a.value * b.value

    return (part1, part2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    print(puzzle(args.filename))
