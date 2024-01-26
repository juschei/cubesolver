from src.logic.cube import Cube
import src.logic.solver as solver

import time


def test(niter):
    for _ in range(niter):
        c = Cube()
        c.set_solved()
        scramble_string = c.scramble()
        print(f"Scramble: {scramble_string}")

        # solve the cube and measure the time
        start_time = time.time()
        solver.solve(c, verbose=True)
        end_time = time.time()
        print(f"Solved cube in {(end_time - start_time):.1f}s")

        if not c.is_solved():
            exit(-1)


if __name__ == "__main__":
    # test(1)
    c = Cube()
    c.set_solved()

    c.print_mesh()
    print()

    c.move_Y()
    c.print_mesh()

    # m = "LLBLULDUUUBDLDRLRDUFFDLLFRLBLBDDLDUBLLDFLDFDRFRRUFBFUULRRFDDDRFURDLLDDLRURUBRLLFLULUBFLFFBBBDRRBDLFD"
    # c = Cube()
    # c.set_solved()
    # c.move_string(m)
    # solver.solve(c, verbose=False)
