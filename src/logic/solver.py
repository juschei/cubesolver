from src.logic.directions import *
from src.logic.cube import Cube
from src.logic.solvers.first_layer import white_cross
from src.logic.solvers.first_layer import insert_corners
from src.logic.solvers.second_layer import solve_second_layer
from src.logic.solvers.last_layer import solve_OLL
from src.logic.solvers.last_layer import solve_PLL


def solve(c: Cube, verbose=False):
    if verbose:
        print("Solving White Cross... ", end="")
    white_cross(c)
    if verbose:
        print("done!")
        print("Inserting Corners... ", end="")
    insert_corners(c)
    if verbose:
        print("done!")
        print("Solving Second Layer... ", end="")
    solve_second_layer(c)
    if verbose:
        print("done!")
        print("Solving OLL... ", end="")
    solve_OLL(c)
    if verbose:
        print("done!")
        print("Solving PLL... ", end="")
    solve_PLL(c)
    if verbose:
        print("done!")
