# coding: utf-8

"""
https://adventofcode.com/2025/day/8
"""

from __future__ import annotations

import itertools

from aoc2025 import Solver, Part


def solution(data: list[str], part: Part) -> int | str | None:
    # create list of 3d points
    points = [tuple(map(int, line.split(","))) for line in data]

    # compute distance brute force for all combinations and sort
    closest_pairs = sorted(
        (
            (p1, p2, ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)**0.5)
            for p1, p2 in itertools.combinations(points, 2)
        ),
        key=(lambda item: item[2]),
    )

    # create connections, keepin track of all clusters
    clusters: dict[tuple, set[tuple]] = {point: {point} for point in points}
    last_product = 0  # part b: keep track of x-product of last connected points
    for p1, p2, _ in closest_pairs[slice(None, 1_000 if part == "a" else None)]:
        if p1 not in clusters[p2]:
            # merge into p1 clusters
            clusters[p1].update(clusters[p2])
            # update all cluster references in p2
            for p in clusters[p2]:
                clusters[p] = clusters[p1]
            last_product = p1[0] * p2[0]  # part b

    # part b
    if part == "b":
        return last_product

    # part a: make clusters unique and sort by size
    largest_clusters = sorted(set(map(frozenset, clusters.values())), key=len, reverse=True)
    return len(largest_clusters[0]) * len(largest_clusters[1]) * len(largest_clusters[2])


if __name__ == "__main__":
    solver = Solver(year=2025, day=8, truth_a=122_636, truth_b=9_271_575_747)
    solver(solution, part="x", submit=False)
