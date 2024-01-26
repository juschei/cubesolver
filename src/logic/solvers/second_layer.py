from src.logic.directions import *
from src.logic.cube import Cube


# checks if all edges in the second layer are inserted correctly
def edges_done(c: Cube):
    side_faces = [c.faces[c.L], c.faces[c.F], c.faces[c.R], c.faces[c.B]]
    edges = [(1, 0), (1, 2)]

    for f in side_faces:
        for e in edges:
            if f[e] != f[1, 1]:
                return False
    return True


# returns a list of useful (non-yellow) edges on the top
# given via their outward-facing colors
def retrieve_useful_edge(c: Cube):
    edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    adjacent_faces = [c.faces[c.B], c.faces[c.L], c.faces[c.R], c.faces[c.F]]

    useful_edges = []
    for e, a in zip(edges, adjacent_faces):
        if c.faces[c.U][e] != COLOR_YELLOW and a[0, 1] != COLOR_YELLOW:
            return a[0, 1]

    return None


# inserts all useful edges that are currently on the top layer
# (and ones that possibly come up in the process)
def insert_useful_edges(c: Cube):
    useful_edge = retrieve_useful_edge(c)

    while useful_edge is not None:
        # bring the edge over the approriate middle stone,
        # so that everything is in the front
        while c.faces[c.F][1, 1] != useful_edge:
            c.move_Y()
        while c.faces[c.F][0, 1] != useful_edge or c.faces[c.U][2, 1] == COLOR_YELLOW:
            c.move_U()

        # print(f"ready to insert {COLORS_REV[useful_edge]}")
        # print()
        # c.print_mesh()

        # insertion to the left
        if c.faces[c.U][2, 1] == c.faces[c.L][1, 1]:
            # print("insertion to the left")
            c.move_string("U'L'U'LUFUF'")
            # print("insertion complete")
        # insertion to the right
        elif c.faces[c.U][2, 1] == c.faces[c.R][1, 1]:
            # print("insertion to the right")
            c.move_string("URUR'U'F'U'F")
            # print("insertion complete")

        # retrieve new edge
        useful_edge = retrieve_useful_edge(c)

        # print()
        # c.print_mesh()


# detect non-yellow edges that are stuck at the wrong place in
# the second layer and bring them up to the top
def produce_useful_edge(c: Cube):
    while not edges_done(c):
        if c.faces[c.F][1, 0] != c.faces[c.F][1, 1]:
            c.move_string("U'L'U'LUFUF'")
            return
        elif c.faces[c.F][1, 2] != c.faces[c.F][1, 1]:
            c.move_string("URUR'U'F'U'F")
            return
        c.move_Y()


def solve_second_layer(c: Cube):
    while not edges_done(c):
        insert_useful_edges(c)
        produce_useful_edge(c)
