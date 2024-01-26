Y_map = {
    "R": "B",
    "R'": "B'",
    "L": "F",
    "L'": "F'",
    "F": "R",
    "F'": "R'",
    "B": "L",
    "B'": "L'",
}


def map_Y(move: str, y_count: int):
    """
    move: the move to be mapped, allowed values: "R", "R'", "L", "L'", "F", "F'", "B", "B'" (the other moves are not affected by Y)
    y_count: the number of Y moves that have been performed before the move

    maps each move that depends on the Y-orientation to the corresponding move without a Y being performed first
    """
    if move in Y_map:
        y_count %= 4
        if y_count == 4:
            return move
        else:
            # compose map access in Y_map y_count times
            for _ in range(y_count):
                move = Y_map[move]
        return move
    return move


def remove_all_Y(moves: list[str]) -> list[str]:
    """
    moves: list of moves to be parsed
    """

    new_moves = []
    y_count = 0
    for move in moves:
        if move == "Y":
            y_count += 1
        elif move == "Y'":
            y_count -= 1
        else:
            new_moves.append(map_Y(move, y_count))

    return new_moves


def clean_move_from_string(move_string: str) -> list[str]:
    """
    move_string: the move string to be cleaned

    Removes redundant steps to make the move string shorter.
    - removes all quadruple occurrences of moves (e.g. "R R R R" -> "")
    - replaces triple occurrances by the opposite move (e.g. "R R R" -> "R'")
    """

    # apply move map to be able to use regex

    move_string = (
        move_string.replace("U'", "u")
        .replace("R'", "r")
        .replace("D'", "d")
        .replace("L'", "l")
        .replace("F'", "f")
        .replace("B'", "b")
    )

    upper_to_lower = {upper: lower for upper, lower in zip("URDLFB", "urdlfb")}
    lower_to_upper = {lower: upper for upper, lower in upper_to_lower.items()}
    # join both dictionaries
    opposites = {**upper_to_lower, **lower_to_upper}

    for move, opposite_move in opposites.items():
        # remove quadruple occurences
        move_string = move_string.replace(f"{move}{move}{move}{move}", "")
        # replace triple occurences
        move_string = move_string.replace(f"{move}{move}{move}", opposite_move)

    # revert move map to get the original moves back
    move_list = list(move_string)

    # revert character mapping in move_list
    for i, move in enumerate(move_list):
        if move == "r":
            move_list[i] = "R'"
        elif move == "l":
            move_list[i] = "L'"
        elif move == "u":
            move_list[i] = "U'"
        elif move == "d":
            move_list[i] = "D'"
        elif move == "f":
            move_list[i] = "F'"
        elif move == "b":
            move_list[i] = "B'"

    return move_list


if __name__ == "__main__":
    print(parse_move_with_y(["R", "Y", "R", "Y", "R", "Y", "R", "Y"]))
