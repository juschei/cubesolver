from src.logic.directions import *
from src.logic.cube import Cube


def white_cross_done(c: Cube):
    edges_white = [(0, 1), (1, 0), (1, 2), (2, 1)]
    side_faces = [c.faces[c.F], c.faces[c.L], c.faces[c.R], c.faces[c.B]]

    for e in edges_white:
        if c.faces[c.D][e] != COLOR_WHITE:
            return False

    for f in side_faces:
        if f[2, 1] != f[1, 1]:
            return False
    return True


# stage 0: orient one edge on the white side, rescue all others to the to
def stage_0(c: Cube):
    edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    adjacent_faces = [c.faces[c.F], c.faces[c.L], c.faces[c.R], c.faces[c.B]]
    white_face = c.faces[c.D]
    # if there are any white edges on the white face, rotate until at least one
    # is correctly oriented
    if any([white_face[edge] == COLOR_WHITE for edge in edges]):
        done = False
        for _ in range(4):
            white_face = c.faces[c.D]

            for e, f in zip(edges, adjacent_faces):
                if white_face[e] == COLOR_WHITE and f[2, 1] == f[1, 1]:
                    # print(f"{e} piece has {COLORS_REV[f[2,1]]} edge on {COLORS_REV[f[1,1]]} side")
                    done = True
                    break
            if done:
                break
            c.move_D()


# stage 1: scan for white edges facing upwards, insert them at correct face
def stage_1(c: Cube):
    edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    adjacent_faces = [c.faces[c.B], c.faces[c.L], c.faces[c.R], c.faces[c.F]]
    moves = {(0, 1): c.move_B, (1, 0): c.move_L, (1, 2): c.move_R, (2, 1): c.move_F}
    yellow_face = c.faces[c.U]

    # if not any([yellow_face[edge] == COLOR_WHITE for edge in edges]):
    #     return

    while True:
        # print("in stage 1 loop")
        yellow_face = c.faces[c.U]
        for e, f in zip(edges, adjacent_faces):
            if yellow_face[e] == COLOR_WHITE and f[0, 1] == f[1, 1]:
                move = moves[e]
                # print(f"{e} piece has {COLORS_REV[f[0,1]]} edge on {COLORS_REV[f[1,1]]} side, flipping over! (via {move})")
                move()
                move()
        if any([yellow_face[edge] == COLOR_WHITE for edge in edges]):
            c.move_U()
        else:
            break


# stage 2: rotate outwards-facing white edges in the yellow layer so that they face upwards
# -> return to stage 1
# we only consider the front face and rotate the cube
def stage_2(c: Cube):
    algo = "FRU'R'F'"

    while True:
        # print("in stage 2 loop")
        faces = [c.faces[c.L], c.faces[c.F], c.faces[c.R], c.faces[c.B]]
        if c.faces[c.F][0, 1] == COLOR_WHITE:
            # print("white face detected in the front")
            c.move_string(algo)
            stage_1(c)
            continue
        if not any([f[0, 1] == COLOR_WHITE for f in faces]):
            break
        c.move_Y()


# stage 3: look for white side edges and bring them up -> return to stage 1
# we only consider the front face and rotate the cube
def stage_3(c: Cube):
    faces = [c.faces[c.L], c.faces[c.F], c.faces[c.R], c.faces[c.B]]
    edges = [(1, 0), (1, 2)]
    algos = ["L'U'L", "RUR'"]

    while True:
        # print("in stage 3 loop")
        for e, a in zip(edges, algos):
            if c.faces[c.F][e] == COLOR_WHITE:
                # print(f"{e} is white!")
                # c.print_mesh()
                # print()
                c.move_string(a)
                stage_1(c)
        if not any([f[e] == COLOR_WHITE for f in faces for e in edges]):
            break
        c.move_Y()


# stage 4: look for white side edges on the bottom layer
# and bring them up -> return to stage 1
# we only consider the front face and rotate the cube
def stage_4(c: Cube):
    algo = "F'RU'R'F"

    while True:
        faces = [c.faces[c.L], c.faces[c.F], c.faces[c.R], c.faces[c.B]]
        # print("in stage 4 loop")
        if c.faces[c.F][2, 1] == COLOR_WHITE:
            c.move_string(algo, log=False)
            stage_1(c)

        # print()
        # c.print_mesh()

        if not any(f[2, 1] == COLOR_WHITE for f in faces):
            break
        c.move_Y()


# stage 5: turn up white edges that are facing down but whose
# other color is not matching -> return to stage 1
def stage_5(c: Cube):
    edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    adjacent_faces = [c.faces[c.F], c.faces[c.L], c.faces[c.R], c.faces[c.B]]
    moves = {(0, 1): c.move_F, (1, 0): c.move_L, (1, 2): c.move_R, (2, 1): c.move_B}

    for e, f in zip(edges, adjacent_faces):
        white_face = c.faces[c.D]
        if white_face[e] == COLOR_WHITE and f[2, 1] != f[1, 1]:
            moves[e]()
            stage_1(c)


def white_cross(c: Cube):
    while not white_cross_done(c):
        stage_0(c)
        stage_1(c)
        stage_2(c)
        stage_3(c)
        stage_4(c)
        stage_5(c)


def inserts_done(c: Cube):
    white_corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    side_corners = [(2, 0), (2, 2)]
    adjacent_faces = [c.faces[c.F], c.faces[c.L], c.faces[c.R], c.faces[c.B]]
    white_face = c.faces[c.D]

    for c in white_corners:
        if white_face[c] != COLOR_WHITE:
            return False
    for a in adjacent_faces:
        for c in side_corners:
            if a[c] != a[1, 1]:
                return False
    return True


# insert white corners from the top layer facing sideways
def normal_inserts(c: Cube):
    algos = ["FUF'", "F'UF", "LUL'", "L'U'L", "RUR'", "R'U'R", "BUB'", "B'U'B"]

    corners = [(0, 0), (0, 2)]

    def init_corners():
        corners_on_faces = [
            (c.faces[c.F], (0, 0)),
            (c.faces[c.F], (0, 2)),
            (c.faces[c.L], (0, 0)),
            (c.faces[c.L], (0, 2)),
            (c.faces[c.R], (0, 0)),
            (c.faces[c.R], (0, 2)),
            (c.faces[c.B], (0, 0)),
            (c.faces[c.B], (0, 2)),
        ]

        corresponding_corners = [
            (c.faces[c.L], (0, 2)),
            (c.faces[c.R], (0, 0)),
            (c.faces[c.B], (0, 2)),
            (c.faces[c.F], (0, 0)),
            (c.faces[c.F], (0, 2)),
            (c.faces[c.B], (0, 0)),
            (c.faces[c.R], (0, 2)),
            (c.faces[c.L], (0, 0)),
        ]

        adjacent_faces = [c.faces[c.L], c.faces[c.F], c.faces[c.R], c.faces[c.B]]

        return corners_on_faces, corresponding_corners, adjacent_faces

    corners_on_faces, corresponding_corners, adjacent_faces = init_corners()
    counter = 0
    while any([f[c] == COLOR_WHITE for f, c in corners_on_faces]):
        corners_on_faces, corresponding_corners, adjacent_faces = init_corners()
        # print([f[c] == COLOR_WHITE for f, c in corners_on_faces])
        # print()
        # c.print_mesh()

        for pair1, pair2, algo in zip(corners_on_faces, corresponding_corners, algos):
            f1, c1 = pair1
            f2, c2 = pair2

            if f1[c1] == COLOR_WHITE and f2[c2] == f2[1, 1]:
                # print()
                # c.print_mesh()
                # print(f"{c1} white, executing {algo}")
                c.move_string(algo)
                # print()
                # c.print_mesh()

        c.print_mesh()
        c.move_U()
        counter += 1
        if counter > 20:
            import sys

            sys.exit(1)


# orient white corners from the top layer facing upwards
# calls normal_inserts
def up_facing_inserts(c: Cube):
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    while True:
        yellow_face = c.faces[c.U]
        if yellow_face[2, 2] == COLOR_WHITE:
            c.move_string("RUUR'")
            normal_inserts(c)
        if yellow_face[2, 0] == COLOR_WHITE:
            c.move_string("L'UUL")
            normal_inserts(c)
        yellow_face = c.faces[c.U]
        if not any([yellow_face[c] == COLOR_WHITE for c in corners]):
            break
        c.move_U()


# bring white corners form the bottom layer back to the top of white faces sideways
# calls normal_inserts
def fix_side_corners(c: Cube):
    corners = [(2, 0), (2, 2)]
    while True:
        # print("in side")
        # print()
        # c.print_mesh()
        if c.faces[c.R][2, 0] == COLOR_WHITE:
            c.move_string("RUR'")
            normal_inserts(c)
        if c.faces[c.F][2, 2] == COLOR_WHITE:
            c.move_string("F'U'F")
            normal_inserts(c)

        adjacent_faces = [c.faces[c.L], c.faces[c.F], c.faces[c.R], c.faces[c.B]]
        if not any([f[c] == COLOR_WHITE for f in adjacent_faces for c in corners]):
            break
        c.move_Y()


# bring white corners from the buttom layers in the wrong slots back up
# calls normal_inserts
def fix_down_corners(c: Cube):
    corners = [(2, 0), (2, 2)]
    while True:
        white_face = c.faces[c.D]
        right_face = c.faces[c.R]
        left_face = c.faces[c.L]
        if right_face[2, 0] != right_face[1, 1] and white_face[2, 2] == COLOR_WHITE:
            c.move_string("RUR'")
            normal_inserts(c)
        if left_face[2, 2] != left_face[1, 1] and white_face[2, 0] == COLOR_WHITE:
            c.move_string("L'U'L")
            normal_inserts(c)

        adjacent_faces = [c.faces[c.L], c.faces[c.F], c.faces[c.R], c.faces[c.B]]
        if not any([f[c] != f[1, 1] for f in adjacent_faces for c in corners]):
            break
        c.move_Y()


def insert_corners(c: Cube):
    # print(inserts_done(c))

    while not inserts_done(c):
        # print()
        # c.print_mesh()
        # print("Doing normal Inserts")
        normal_inserts(c)
        # print()
        # c.print_mesh()
        # print("Normal Inserts done")
        # print("Fixing white-up corners")
        up_facing_inserts(c)
        # print()
        # c.print_mesh()
        # print("Fixed white-up corners")
        # print("Fixing side-white corners")
        print("Starting side corners")
        fix_side_corners(c)
        # print()
        # c.print_mesh()
        # print("Fixed side-white corners")
        # print("Fixing wrongly oriented white-down corners")
        print("Starting down corners")
        fix_down_corners(c)
        # print()
        # c.print_mesh()
        # print("Fixed wrongly oriented white-down corners")
