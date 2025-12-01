# coding: utf-8

"""
https://adventofcode.com/2025/day/1
"""

from __future__ import annotations

from aoc2025 import Solver, Part


def solution(data: list[str], part: Part) -> int | None:
    pos = 50  # current position
    n = 0  # number of times at position 0

    for line in data:
        direction = 1 if line[0] == "R" else -1
        distance = int(line[1:])
        # edge case
        if not distance:
            continue
        # advance position
        new_pos = pos + direction * distance
        # count 0 crossings, part b
        if part == "b":
            if direction == 1:  # moving right
                n += new_pos // 100
            elif new_pos == 0:  # moving left, landing exactly on 0
                n += 1
            elif new_pos < 0:  # moving left, having crossed 0 and checking if not started from 0
                n += int(pos != 0) + abs(new_pos) // 100
        # update position
        pos = new_pos % 100
        # count 0 crossings, part a
        if part == "a":
            n += int(pos == 0)

    # return answer
    return n


if __name__ == "__main__":
    Solver(year=2025, day=1, truth_a=1150, truth_b=6_738).solve(solution, part="x", example=False, submit=False)
