# coding: utf-8

"""
https://adventofcode.com/2025/day/3
"""

from __future__ import annotations

from aoc2025 import Solver, Part


def solution(data: list[str], part: Part) -> int | str | None:
    n_nums = 2 if part == "a" else 12

    joltages: list[int] = []
    for line in data:
        # convert to integers (strings would work, but this is cleaner imho)
        nums = list(map(int, line))
        # iteratively find maximum in moving window that take into account a remainder to accommodate all n_nums
        max_nums: list[int] = []
        start = 0
        for i in range(n_nums - 1, -1, -1):
            # look for maximum between start and len(nums) - i, then shift start to next number
            i_max = max(range(start, len(nums) - i), key=lambda x: nums[x])
            max_nums.append(nums[i_max])
            start = i_max + 1
        # compute joltage
        joltages.append(sum(num * 10**(n_nums - i - 1) for i, num in enumerate(max_nums)))

    return sum(joltages)


if __name__ == "__main__":
    Solver(year=2025, day=3, truth_a=17_100, truth_b=170_418_192_256_861).solve(solution, part="x", submit=False)
