# coding: utf-8

"""
https://adventofcode.com/2025/day/10
"""

from __future__ import annotations

import collections
import scipy.optimize  # type: ignore[import-untyped]

from aoc2025 import Solver, Part


def solution(data: list[str], part: Part) -> int | str | None:
    sum_presses = 0

    # part a
    def match_state(target_state: list[int], buttons: list[set[int]]) -> int:
        # strategy:
        # - interpret light and button indices as integer bits
        # - then, presses become xor operations
        # - use a bfs to find minimal number of presses to reach target state
        target = sum(1 << i for i in target_state)
        _buttons = {sum(1 << b for b in button) for button in buttons}

        # bfs with queue, remembering and not re-visiting states
        # (current state, number of presses to get there, index of last pressed button)
        q = collections.deque([(0, 0, -1)])
        visited = {0}
        while q:
            state, presses, prev_idx = q.popleft()
            # check state
            if state == target:
                break
            # shortcut: correct button can be defined, so check if it exists
            if (target ^ state) in _buttons:
                presses += 1
                break
            # check all buttons, omitting the last pressed one
            for i, button in enumerate(_buttons):
                if i == prev_idx:
                    continue
                if (new_state := state ^ button) not in visited:
                    visited.add(new_state)
                    q.append((new_state, presses + 1, i))

        return presses

    # part b
    def match_joltages(target_joltages: list[int], buttons: list[set[int]]) -> int:
        # strategy:
        # - the number of lights/joltages define the dimension of a vector space
        # - the target joltages represent a vector in that space
        # - each button b_i can be seen as a (unit) vector in that space
        # - we are looking for integer coeffs a_i so that a_i * b_i = target vector (summing over i)
        # - the constraint is that the sum of a_i is minimal
        # -> linear optimization problem with integer constraints
        #    (https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html)
        # -> A is matrix of button vectors, b is target vector, c is effect of each component on target metric (presses)

        # button matrix
        A = [
            [int(i in b) for b in buttons]
            for i in range(len(target_joltages))
        ]
        # target vector
        b = target_joltages
        # effect of components (all 1, one button press per component)
        c = [1] * len(buttons)

        res = scipy.optimize.linprog(A_eq=A, b_eq=b, c=c, bounds=(0, None), integrality=1)  # integer variable

        return int(res.fun)

    for line in data:
        # parse each line
        parts = line.split(" ")
        target_state = [i for i, c in enumerate(parts[0][1:-1]) if c == "#"]
        buttons = [set(map(int, p[1:-1].split(","))) for p in parts[1:-1]]
        target_joltages = list(map(int, parts[-1][1:-1].split(",")))

        # match either state (a) or joltages (b)
        if part == "a":
            sum_presses += match_state(target_state, buttons)
        else:  # part b
            sum_presses += match_joltages(target_joltages, buttons)

    return sum_presses


if __name__ == "__main__":
    solver = Solver(year=2025, day=10, truth_a=535, truth_b=21_021)
    solver(solution, part="x", submit=False)
