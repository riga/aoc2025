# coding: utf-8

"""
https://adventofcode.com/2025/day/7
"""

from __future__ import annotations

import functools

from aoc2025 import Solver, Part


def solution(data: list[str], part: Part) -> int | str | None:
    # initial beam position and splitters per line
    beams: set[int] = {data[0].index("S")}
    splitter_lines: list[set[int]] = [
        set(i for i, c in enumerate(line) if c == "^")
        for line in data[1:]
    ]

    # part a: get number of splits
    if part == "a":
        n_splits = 0
        for splitters in splitter_lines:
            # use set arithmetic
            hits = beams & splitters
            beams -= splitters
            if hits:
                n_splits += len(hits)
                beams |= set.union(*({b - 1, b + 1} for b in hits))  # no splitters at boundaries in data

        return n_splits

    # part b: backtracking with memoization
    @functools.cache
    def count_paths(line_idx: int, pos: int) -> int:
        # end reached, count single beam
        if line_idx >= len(splitter_lines):
            return 1
        # no splitter, continue beam
        if pos not in splitter_lines[line_idx]:
            return count_paths(line_idx + 1, pos)
        # look ahead both directions and count, again, no splitters at boundaries in data
        return count_paths(line_idx + 1, pos - 1) + count_paths(line_idx + 1, pos + 1)

    # start at top at initial beam position
    return count_paths(0, beams.pop())


if __name__ == "__main__":
    solver = Solver(year=2025, day=7, truth_a=1_594, truth_b=15_650_261_281_478)
    solver(solution, part="x", submit=False)
