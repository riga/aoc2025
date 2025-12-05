# coding: utf-8

"""
https://adventofcode.com/2025/day/5
"""

from __future__ import annotations

from aoc2025 import Solver, Part


def solution(data: list[str], part: Part) -> int | str | None:
    # parse input
    id_ranges: list[tuple[int, int]] = []
    available_ids: list[int] = []
    for line in data:
        if (idx := line.find("-")) != -1:
            id_ranges.append((int(line[:idx]), int(line[idx + 1:])))
        else:
            available_ids.append(int(line))

    # merge ranges
    id_ranges.sort(key=lambda tpl: tpl[0])
    merged_id_ranges = [id_ranges[0]]
    for start, stop in id_ranges[1:]:
        last_start, last_stop = merged_id_ranges[-1]
        if start > last_stop:
            merged_id_ranges.append((start, stop))
        elif stop > last_stop:
            merged_id_ranges[-1] = (last_start, stop)

    # part a: count occurrences
    if part == "a":
        return sum(
            1 for a in available_ids
            if any(start <= a <= stop for start, stop in id_ranges)
        )

    # part b: sum extents
    return sum(stop - start + 1 for start, stop in merged_id_ranges)


if __name__ == "__main__":
    Solver(year=2025, day=5, truth_a=885, truth_b=348_115_621_205_535).solve(solution, part="x", submit=False)
