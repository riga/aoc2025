# coding: utf-8

"""
https://adventofcode.com/2025/day/9
"""

from __future__ import annotations

import itertools
import collections

from aoc2025 import Solver, Part


def solution(data: list[str], part: Part) -> int | str | None:
    red_tiles = [complex(*map(int, line.split(","))) for line in data]

    # created sorted list of all square combinations with their area
    get_area = lambda p, q: int((abs(p.real - q.real) + 1) * (abs(p.imag - q.imag) + 1))
    squares = [(p, q, get_area(p, q)) for p, q in itertools.combinations(red_tiles, 2)]
    squares.sort(key=lambda tpl: tpl[2], reverse=True)

    # part a: return maximum
    if part == "a":
        return squares[0][2]

    # part b:
    # - create hashmaps to store positions of all edge tiles, associated to either x or y coordinate
    # - then, for each area check if there is an intersection with any edge _inside_ (excluding its defining border)
    # - this assumes that there are no tight turns which is true in the data

    # helper to get corner coordinates given two points
    def get_corners(p: complex, q: complex) -> tuple[int, int, int, int]:
        # x/y2 is always the larger value
        x1, x2 = (int(p.real), int(q.real)) if p.real < q.real else (int(q.real), int(p.real))
        y1, y2 = (int(p.imag), int(q.imag)) if p.imag < q.imag else (int(q.imag), int(p.imag))
        return x1, y1, x2, y2

    # scan and store edges as 2-tuples (both sides inclusive)
    v_edges: dict[int, set[tuple[int, int]]] = collections.defaultdict(set)
    h_edges: dict[int, set[tuple[int, int]]] = collections.defaultdict(set)
    for p, q in zip(red_tiles, red_tiles[1:] + red_tiles[:1]):
        x1, y1, x2, y2 = get_corners(p, q)
        if y1 == y2:  # horizontal edge
            h_edges[y1].add((x1, x2))
        else:  # vertical edge
            v_edges[x1].add((y1, y2))

    # helper to check for intersection of a single square with any edge
    def intersects_edge(p: complex, q: complex) -> bool:
        x1, y1, x2, y2 = get_corners(p, q)
        # check horizontal edges
        for ey, edges in h_edges.items():
            if not (y1 < ey < y2):
                continue
            for ex1, ex2 in edges:
                if ex2 > x1 and ex1 < x2:
                    return True
        # check vertical edges
        for ex, edges in v_edges.items():
            if not (x1 < ex < x2):
                continue
            for ey1, ey2 in edges:
                if ey2 > y1 and ey1 < y2:
                    return True
        # no collision found
        return False

    # check each square for intersections
    for p, q, area in squares:
        if not intersects_edge(p, q):
            return area

    raise RuntimeError("no solution found")


if __name__ == "__main__":
    solver = Solver(year=2025, day=9, truth_a=4_782_896_435, truth_b=1_540_060_480)
    solver(solution, part="x", submit=False)
