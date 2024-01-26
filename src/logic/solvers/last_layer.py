import numpy as np
import os

from src.logic.directions import *
from src.logic.cube import Cube


def init_patterns():
    pattern_file_path = os.path.join(os.path.dirname(__file__), "patterns_OLL.txt")
    OLL_pattern_strings = open(pattern_file_path).read().split("\n\n")

    OLL_patterns = []
    for s in OLL_pattern_strings:
        split = s.split("\n")
        assert len(split) == 5
        assert len(split[2]) == 5
        top_pattern = np.zeros((3, 3), dtype=np.int8) - 1
        B_pattern = np.zeros(3, dtype=np.int8) - 1
        L_pattern = np.zeros(3, dtype=np.int8) - 1
        F_pattern = np.zeros(3, dtype=np.int8) - 1
        R_pattern = np.zeros(3, dtype=np.int8) - 1

        # parse top pattern
        for i in range(1, len(split) - 1):
            for j in range(1, len(split) - 1):
                if split[i][j] == "x":
                    top_pattern[i - 1, j - 1] = COLOR_YELLOW

        # parse side patterns
        for j in range(1, 4):
            if split[0][j] == "x":
                B_pattern[j - 1] = COLOR_YELLOW

        for j in range(1, 4):
            if split[4][j] == "x":
                F_pattern[j - 1] = COLOR_YELLOW

        for i in range(1, 4):
            if split[i][0] == "x":
                L_pattern[i - 1] = COLOR_YELLOW

        for i in range(1, 4):
            if split[i][4] == "x":
                R_pattern[i - 1] = COLOR_YELLOW

        OLL_patterns.append((top_pattern, B_pattern, L_pattern, F_pattern, R_pattern))

    return OLL_patterns


def nr_yellow_edges(c: Cube):
    f = c.faces[c.U]
    edges = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
    return sum([int(f[e]) == COLOR_YELLOW for e in edges])


def has_cross(c: Cube):
    return nr_yellow_edges(c) == 5


# checks for cross / bar to for first look OLL
def match_pattern_first_look_OLL(c: Cube):
    top_layer = c.faces[c.U]

    if top_layer[0, 1] == COLOR_YELLOW and top_layer[1, 0] == COLOR_YELLOW:
        return 0
    elif top_layer[1, 0] == COLOR_YELLOW and top_layer[1, 2] == COLOR_YELLOW:
        return 1
    return -1


def first_look_OLL(c: Cube):
    while not has_cross(c):
        res = match_pattern_first_look_OLL(c)
        match res:
            case 0:
                c.move_string("FRUR'U'RUR'U'F'")
            case 1:
                c.move_string("FRUR'U'F'")
            case _:
                if nr_yellow_edges(c) == 1:
                    c.move_string("FRUR'U'F'")
                else:
                    c.move_Y()


def OLL_solved(c: Cube):
    return (c.faces[c.U] == COLOR_YELLOW).all()


# determines whether the cube in its current configuration matches
# a given pattern given a 5-tuple
# (top_pattern, B_pattern, L_pattern, F_pattern, R_pattern)
# where top_pattern is a size 3x3 np.array (int8) and the others are
# size 3 np.array (int8)
# in the pattern COLOR_YELLOW is used for yellow and -1 for other colors
def match_pattern(c: Cube, pattern: tuple):
    fU = c.faces[c.U]
    fB = np.flip(c.faces[c.B][0, :])
    fL = c.faces[c.L][0, :]
    fF = c.faces[c.F][0, :]
    fR = np.flip(c.faces[c.R][0, :])

    def _format(face_slice):
        f = face_slice.copy()
        f[f != COLOR_YELLOW] = -1
        return f

    cube_configuration = list(map(_format, [fU, fB, fL, fF, fR]))

    for idx, (f_pattern, f_cube) in enumerate(zip(pattern, cube_configuration)):
        if not (f_pattern == f_cube).all():
            # if idx != 0:
            #     print("Missmatch at index", idx)
            #     print("Pattern:")
            #     print(f_pattern)
            #     print("Cube:")
            #     print(f_cube)
            return False
    return True


def second_look_OLL(c: Cube, pattern_list):
    for pattern in pattern_list:
        has_match = match_pattern(c, pattern)
        if has_match:
            c.move_string("RUR'URUUR'")
            return True
    return False


def solve_OLL(c: Cube):
    OLL_patterns = init_patterns()
    first_look_OLL(c)

    while not OLL_solved(c):
        if second_look_OLL(c, OLL_patterns):
            continue
        c.move_U()


def all_edges_solved(c: Cube):
    return all(
        [c.faces[side][0, 1] == c.faces[side][1, 1] for side in [c.F, c.R, c.B, c.L]]
    )


def all_corners_solved(c: Cube):
    return all(
        [
            c.faces[side][0, 0] == c.faces[side][1, 1]
            and c.faces[side][0, 2] == c.faces[side][1, 1]
            for side in [c.F, c.R, c.B, c.L]
        ]
    )


def edges_PLL(c: Cube):
    while not c.faces[c.F][0, 1] == c.faces[c.F][1, 1]:
        c.move_U()

    while not all_edges_solved(c):
        # if c.faces[c.B][0,1] == c.faces[c.B][1,1]:
        #     c.move("")
        if c.faces[c.L][0, 1] == c.faces[c.L][1, 1]:
            c.move_string("UUR'UR'U'R'U'R'URURRU")
        if c.faces[c.R][0, 1] == c.faces[c.R][1, 1]:
            c.move_string("UUR'UR'U'R'U'R'URURRU'")
        else:
            c.move_string("R'UR'U'R'U'R'URURR")


# check if any corner already solved
def exists_solved_corner(c: Cube):
    colors = [c.L, c.F, c.R, c.B]
    for col in colors:
        right_adj = right(col)
        if (
            c.faces[col][0, 2] == c.faces[col][1, 1]
            and c.faces[right_adj][0, 0] == c.faces[right_adj][1, 1]
        ):
            return True
    return False


def corners_PLL(c: Cube):
    while not all_corners_solved(c):
        # check if any corner already solved and transport
        # it to the top right
        if exists_solved_corner(c):
            while not (
                c.faces[c.L][0, 0] == c.faces[c.L][1, 1]
                and c.faces[c.B][0, 2] == c.faces[c.B][1, 1]
            ):
                c.move_Y()

        # now either no corner is solved yet or the solved one
        # is in the top left corner
        c.move_string("RB'RFFR'BRFFRR")


def solve_PLL(c: Cube):
    edges_PLL(c)
    corners_PLL(c)
