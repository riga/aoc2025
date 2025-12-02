# coding: utf-8

"""
https://adventofcode.com/2025/day/2
"""

from __future__ import annotations

import itertools

from aoc2025 import Solver, Part


def solution(data: list[str], part: Part) -> int | str | None:
    # parse ranges (no need to merge ranges afterwards, they look rather disjoint)
    ranges = (d.split("-") for d in data[0].split(","))

    # keep track of invalid ids
    invalid_ids: set[int] = set()

    # loop
    for start, stop in ranges:
        for i in range(int(start), int(stop) + 1):
            s = str(i)

            # part a: check halves
            if part == "a":
                if len(s) % 2 == 0 and s[:len(s) // 2] == s[len(s) // 2:]:
                    invalid_ids.add(i)

            # part b: check all possible repeating blocks
            if part == "b":
                # check all possible block sizes
                for block_size in range(1, len(s) // 2 + 1):
                    # must be even divisor
                    if len(s) % block_size != 0:
                        continue
                    # check if all blocks are identical
                    if len(set(itertools.batched(s, block_size))) == 1:
                        invalid_ids.add(i)
                        break

    # compute and return sum
    return sum(invalid_ids)


if __name__ == "__main__":
    Solver(year=2025, day=2, truth_a=30_599_400_849, truth_b=46_270_373_595).solve(solution, part="x", submit=False)
