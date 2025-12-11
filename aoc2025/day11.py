# coding: utf-8

"""
https://adventofcode.com/2025/day/11
"""

from __future__ import annotations

import functools

from aoc2025 import Solver, Part


def solution(data: list[str], part: Part) -> int | str | None:
    # build graph
    devices: dict[str, set[str]] = {
        parts[0][:-1]: set(parts[1:])
        for parts in (line.split() for line in data)
    }

    # part a: simple dp to count paths in graph
    if part == "a":
        @functools.cache
        def count_paths(device: str) -> int:
            if device == "out":
                return 1
            return sum(map(count_paths, devices[device]))

        return count_paths("you")

    # part b: dp again, but only when reaching end, check for validity of path via flags (to use caching)
    @functools.cache
    def count_valid_paths(device: str, visited_dac: bool, visited_fft: bool) -> int:
        if device == "out":
            return int(visited_dac and visited_fft)
        return sum(
            count_valid_paths(n, visited_dac or n == "dac", visited_fft or n == "fft")
            for n in devices[device]
        )

    return count_valid_paths("svr", False, False)


if __name__ == "__main__":
    solver = Solver(year=2025, day=11, truth_a=497, truth_b=358_564_784_931_864)
    solver(solution, part="x", submit=False)
