# coding: utf-8

"""
https://adventofcode.com/2025/day/4
"""

from __future__ import annotations

import collections

from aoc2025 import Solver, Part


def solution(data: list[str], part: Part) -> int | str | None:
    # keep set of role positions
    rolls = {
        complex(x, y)
        for x in range(len(data[0]))
        for y in range(len(data))
        if data[y][x] == "@"
    }

    # possible directions to check
    directions = [-1, +1, -1j, +1j, -1 - 1j, -1 + 1j, 1 - 1j, 1 + 1j]

    # work queue with positions left to check
    n_accessible = 0
    q = collections.deque(rolls)
    while q:
        r = q.popleft()
        if r not in rolls:  # protection for part b
            continue

        # get coordinates of neighbor rolls
        neighbors = {n for d in directions if (n := r + d) in rolls}
        if len(neighbors) < 4:
            n_accessible += 1

            # addition part b: remove from rolls once accessed and add back neighbors to re-check
            if part == "b":
                rolls.remove(r)
                q.extendleft(neighbors)

    return n_accessible


if __name__ == "__main__":
    Solver(year=2025, day=4, truth_a=1_537, truth_b=8_707).solve(solution, part="x", example=False, submit=False)
