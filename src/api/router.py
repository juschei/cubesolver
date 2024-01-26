from fastapi import APIRouter, HTTPException
import re

from src.logic.cube import Cube
import src.logic.solver as solver
from src.util.parsing import clean_move_from_string, remove_all_Y

router = APIRouter(tags=["Cube Solver Endpoints"])


@router.get("/SolveCube", response_model=list[str])
def solve_cube(scramble_string: str):
    """
    Solve a cube from a scramble string, returning a list of moves to solve the cube.
    Assumes that no rotational moves are present in the scramble string. The initial position of the cube assumes
    that white is on the bottom and red is facing the user.

    The allowed parts of the scramble string are:
    - R: right face clockwise
    - R': right face counter-clockwise
    - L: left face clockwise
    - L': left face counter-clockwise
    - U: upper face clockwise
    - U': upper face counter-clockwise
    - D: down face clockwise
    - D': down face counter-clockwise
    - F: front face clockwise
    - F': front face counter-clockwise
    - B: back face clockwise
    - B': back face counter-clockwise

    """

    # validate that input is a scramble string
    pattern = re.compile(r"^([RLUDFB]'?)*$")
    if not pattern.match(scramble_string):
        raise HTTPException(status_code=422, detail="Invalid scramble string")

    c = Cube()
    c.set_solved()
    c.move_string("".join(scramble_string), log=True)

    print(f"History: {c.get_history()}")

    c.reset_history()
    solver.solve(c, verbose=True)

    _move_list = c.get_history()
    _move_list = clean_move_from_string("".join(_move_list))
    move_list = remove_all_Y(_move_list)

    return move_list
