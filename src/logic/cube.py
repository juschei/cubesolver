import numpy as np
import random
from termcolor import colored


from src.logic.directions import *


def face_init(color: int) -> np.array:
    arr = np.full((3, 3), None)
    arr[1, 1] = color
    return arr


def rotate_clockwise(face: np.array, clockwise: bool) -> np.array:
    rot = 3 if clockwise else 1
    return np.rot90(face, rot)


class Cube:
    def __init__(self):
        self.faces = {color: face_init(color) for color in COLORS}
        # position of cube in hand is uniquely identified by
        # giving the front side and the up side
        self.F = COLOR_RED
        self.U = COLOR_YELLOW
        self.R = COLOR_GREEN
        self.B = COLOR_ORANGE
        self.L = COLOR_BLUE
        self.D = COLOR_WHITE

        self.move_history = []

    def set_solved(self):
        # creates a uniform array for a solved side
        def solved_side(color: int) -> np.array:
            return np.full((3, 3), color)

        self.faces = {color: solved_side(color) for color in COLORS.values()}

    def is_solved(self):
        directions = ["U", "R", "D", "L", "F", "B"]
        _faces = [
            self.faces[self.F],
            self.faces[self.L],
            self.faces[self.R],
            self.faces[self.B],
            self.faces[self.D],
            self.faces[self.U],
        ]

        for f in _faces:
            for i in range(3):
                for j in range(3):
                    if f[i, j] != f[1, 1]:
                        return False
        return True

    def print_mesh(self):
        #       ██████
        #       ██00██
        #       ██████
        # ████████████████████████
        # ██22████33████44████55██
        # ████████████████████████
        #       ██████
        #       ██11██
        #       ██████
        mesh = np.full((9, 12), None)

        mesh[0:3, 3:6] = self.faces[self.U]
        mesh[3:6, 0:3] = self.faces[self.L]
        mesh[3:6, 3:6] = self.faces[self.F]
        mesh[3:6, 6:9] = self.faces[self.R]
        mesh[3:6, 9:12] = self.faces[self.B]
        mesh[6:9, 3:6] = self.faces[self.D]

        # reverse so that white is on the bottom
        for row_array in mesh:
            for item in row_array:
                color_name = COLORS_REV
                if item is None:
                    print("  ", end="")
                else:
                    color_name = COLORS_REV[item]
                    if color_name == "orange":
                        color_name = "magenta"
                    print(colored("██", color_name), end="")
            print()

    def move_U(self, hist=True):
        face = self.faces[self.U]
        self.faces[self.U] = rotate_clockwise(face, True)

        _F_SLICE = self.faces[self.F][0, 0:3].copy()
        _L_SLICE = self.faces[self.L][0, 0:3].copy()
        # _L_SLICE = np.flip(_L_SLICE)
        _B_SLICE = self.faces[self.B][0, 0:3].copy()
        _R_SLICE = self.faces[self.R][0, 0:3].copy()

        self.faces[self.L][0, 0:3] = _F_SLICE
        self.faces[self.B][0, 0:3] = _L_SLICE
        self.faces[self.R][0, 0:3] = _B_SLICE
        self.faces[self.F][0, 0:3] = _R_SLICE

        if hist:
            self.move_history.append("U")

    def move_U_prime(self):
        self.move_U(hist=False)
        self.move_U(hist=False)
        self.move_U(hist=False)

        self.move_history.append("U'")

    def move_D(self, hist=True):
        face = self.faces[self.D]
        self.faces[self.D] = rotate_clockwise(face, True)

        _F_SLICE = self.faces[self.F][2, 0:3].copy()
        _L_SLICE = self.faces[self.L][2, 0:3].copy()
        # _L_SLICE = np.flip(_L_SLICE)
        _B_SLICE = self.faces[self.B][2, 0:3].copy()
        _R_SLICE = self.faces[self.R][2, 0:3].copy()

        self.faces[self.R][2, 0:3] = _F_SLICE
        self.faces[self.B][2, 0:3] = _R_SLICE
        self.faces[self.L][2, 0:3] = _B_SLICE
        self.faces[self.F][2, 0:3] = _L_SLICE

        if hist:
            self.move_history.append("D")

    def move_D_prime(self):
        self.move_D(hist=False)
        self.move_D(hist=False)
        self.move_D(hist=False)

        self.move_history.append("D'")

    def move_R(self, hist=True):
        face = self.faces[self.R]
        self.faces[self.R] = rotate_clockwise(face, True)

        _F_SLICE = self.faces[self.F][0:3, 2].copy()
        _U_SLICE = self.faces[self.U][0:3, 2].copy()
        _U_SLICE = np.flip(_U_SLICE)
        _B_SLICE = self.faces[self.B][0:3, 0].copy()
        _B_SLICE = np.flip(_B_SLICE)
        _D_SLICE = self.faces[self.D][0:3, 2].copy()

        self.faces[self.F][0:3, 2] = _D_SLICE
        self.faces[self.U][0:3, 2] = _F_SLICE
        self.faces[self.B][0:3, 0] = _U_SLICE
        self.faces[self.D][0:3, 2] = _B_SLICE

        if hist:
            self.move_history.append("R")

    def move_R_prime(self):
        self.move_R(hist=False)
        self.move_R(hist=False)
        self.move_R(hist=False)

        self.move_history.append("R'")

    def move_L(self, hist=True):
        face = self.faces[self.L]
        self.faces[self.L] = rotate_clockwise(face, True)

        _F_SLICE = self.faces[self.F][0:3, 0].copy()
        _U_SLICE = self.faces[self.U][0:3, 0].copy()
        _B_SLICE = self.faces[self.B][0:3, 2].copy()
        _B_SLICE = np.flip(_B_SLICE)
        _D_SLICE = self.faces[self.D][0:3, 0].copy()
        _D_SLICE = np.flip(_D_SLICE)

        self.faces[self.F][0:3, 0] = _U_SLICE
        self.faces[self.D][0:3, 0] = _F_SLICE
        self.faces[self.B][0:3, 2] = _D_SLICE
        self.faces[self.U][0:3, 0] = _B_SLICE

        if hist:
            self.move_history.append("L")

    def move_L_prime(self):
        self.move_L(hist=False)
        self.move_L(hist=False)
        self.move_L(hist=False)

        self.move_history.append("L'")

    def move_F(self, hist=True):
        face = self.faces[self.F]
        self.faces[self.F] = rotate_clockwise(face, True)

        _L_SLICE = self.faces[self.L][0:3, 2].copy()
        _L_SLICE = np.flip(_L_SLICE)
        _U_SLICE = self.faces[self.U][2, 0:3].copy()
        _R_SLICE = self.faces[self.R][0:3, 0].copy()
        _R_SLICE = np.flip(_R_SLICE)
        _D_SLICE = self.faces[self.D][0, 0:3].copy()

        self.faces[self.L][0:3, 2] = _D_SLICE
        self.faces[self.U][2, 0:3] = _L_SLICE
        self.faces[self.R][0:3, 0] = _U_SLICE
        self.faces[self.D][0, 0:3] = _R_SLICE

        if hist:
            self.move_history.append("F")

    def move_F_prime(self):
        self.move_F(hist=False)
        self.move_F(hist=False)
        self.move_F(hist=False)

        self.move_history.append("F'")

    def move_B(self, hist=True):
        face = self.faces[self.B]
        self.faces[self.B] = rotate_clockwise(face, True)

        _R_SLICE = self.faces[self.R][0:3, 2].copy()
        _U_SLICE = self.faces[self.U][0, 0:3].copy()
        _U_SLICE = np.flip(_U_SLICE)
        _L_SLICE = self.faces[self.L][0:3, 0].copy()
        _D_SLICE = self.faces[self.D][2, 0:3].copy()
        _D_SLICE = np.flip(_D_SLICE)

        self.faces[self.U][0, 0:3] = _R_SLICE
        self.faces[self.L][0:3, 0] = _U_SLICE
        self.faces[self.D][2, 0:3] = _L_SLICE
        self.faces[self.R][0:3, 2] = _D_SLICE

        if hist:
            self.move_history.append("B")

    def move_B_prime(self):
        self.move_B(hist=False)
        self.move_B(hist=False)
        self.move_B(hist=False)

        self.move_history.append("B'")

    def move_Y(self):
        _F, _R, _B, _L = self.F, self.R, self.B, self.L
        # swap colors according to rotation
        self.F, self.R, self.B, self.L = _R, _B, _L, _F

        U_FACE = self.faces[self.U]
        self.faces[self.U] = rotate_clockwise(U_FACE, True)

        D_FACE = self.faces[self.D]
        self.faces[self.D] = rotate_clockwise(D_FACE, False)

        self.move_history.append("Y")

        # update faces
        # c.faces[self.F], c.faces[self.R], c.faces[self.B], c.faces[self.L] = c.faces[_F], c.faces[_R], c.faces[_B], c.faces[_L]

    # def move_X(self):
    # 	pass

    def move_string(self, move_string, log=False):
        moves = {
            "U": self.move_U,
            "R": self.move_R,
            "D": self.move_D,
            "L": self.move_L,
            "F": self.move_F,
            "B": self.move_B,
            "u": self.move_U_prime,
            "r": self.move_R_prime,
            "d": self.move_D_prime,
            "l": self.move_L_prime,
            "f": self.move_F_prime,
            "b": self.move_B_prime,
        }

        move_string = (
            move_string.replace("U'", "u")
            .replace("R'", "r")
            .replace("D'", "d")
            .replace("L'", "l")
            .replace("F'", "f")
            .replace("B'", "b")
        )

        for c in move_string:
            if log:
                # print("Faces:")
                # print(self.faces)

                # print()
                # print(f"Executed {c}")
                # self.print_mesh()
                print(f"Executing {moves[c]}")
            moves[c]()

    def scramble(self, niter=100):
        moves = ["U", "R", "D", "L", "F", "B"]

        move_string = ""
        for _ in range(niter):
            move_char = moves[random.randrange(0, len(moves))]
            move_string += move_char
            exec(f"self.move_{move_char}()")
        return move_string

    def scramble_from_string(self, scramble_str):
        moves = {
            "U": self.move_U,
            "R": self.move_R,
            "D": self.move_D,
            "L": self.move_L,
            "F": self.move_F,
            "B": self.move_B,
        }
        for character in scramble_str:
            moves[character]()

    def reset_history(self) -> None:
        self.move_history = []

    def get_history(self) -> list[str]:
        return self.move_history
