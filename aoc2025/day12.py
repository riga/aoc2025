# coding: utf-8

"""
https://adventofcode.com/2025/day/12
"""

from __future__ import annotations

from aoc2025 import Solver, Part


Matrix = list[list[int]]


def solution(data: list[str], part: Part) -> int | str | None:
    # parse shapes
    shapes: list[Matrix] = []
    for i, line in enumerate(data):
        if line.endswith(":"):
            shapes.append([
                [int(c == "#") for c in data[i + j + 1]]
                for j in range(3)  # all presents are 3 in height
            ])

    # parse regions
    regions: list[tuple[tuple[int, int], list[int]]] = []
    for line in data:
        if "x" in line:
            parts = line.split()
            regions.append((  # type: ignore[arg-type]
                tuple(map(int, parts[0][:-1].split("x", 1))),  # dimensions
                list(map(int, parts[1:])),  # present counts
            ))

    # lazy assumption / guess: per region, try to just check if the area is in principle large enough
    # (and yes, that was sufficient ...)
    shape_counts = [sum(sum(shape, [])) for shape in shapes]
    return sum(
        int(sum(c * shape_counts[i] for i, c in enumerate(counts)) <= h * w)
        for (h, w), counts in regions
    )


if __name__ == "__main__":
    solver = Solver(year=2025, day=12, truth_a=472, truth_b=None)
    solver(solution, strip=False, part="a", submit=False)
