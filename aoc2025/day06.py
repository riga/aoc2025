# coding: utf-8

"""
https://adventofcode.com/2025/day/6
"""

from __future__ import annotations

import functools
import operator
from typing import Callable

from aoc2025 import Solver, Part


def solution(data: list[str], part: Part) -> int | str | None:
    ops_line, num_lines = data[-1], data[:-1]

    # locate all op positions and convert into index ranges for parsing other lines
    ranges: list[tuple[int, int]] = []
    for pos in list(i for i, c in enumerate(ops_line) if c in {"+", "*"})[1:] + [len(ops_line) + 1]:
        ranges.append((ranges[-1][1] + 1 if ranges else 0, pos - 1))

    # parse ops and nums
    ops: list[Callable] = []
    nums: list[list[str]] = []
    for i, (start, end) in enumerate(ranges):
        ops.append(operator.add if ops_line[start] == "+" else operator.mul)
        block = [num_line[start:end] for num_line in num_lines]
        # part b: replace spaces with zeros and transpose
        if part == "b":
            block = ["".join(chars).strip() for chars in zip(*block)]
        nums.append(block)

    # parse problem numbers in proper groups
    return sum(
        functools.reduce(op, map(int, _nums))
        for op, _nums in zip(ops, nums)
    )


if __name__ == "__main__":
    solver = Solver(year=2025, day=6, truth_a=4_387_670_995_909, truth_b=9_625_320_374_409)
    solver(solution, strip=False, part="x", submit=False)
