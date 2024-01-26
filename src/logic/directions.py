COLOR_WHITE = 0
COLOR_YELLOW = 1
COLOR_GREEN = 2
COLOR_RED = 3
COLOR_BLUE = 4
COLOR_ORANGE = 5

COLORS = {
    "white": COLOR_WHITE,
    "yellow": COLOR_YELLOW,
    "green": COLOR_GREEN,
    "red": COLOR_RED,
    "blue": COLOR_BLUE,
    "orange": COLOR_ORANGE,
}

COLORS_REV = {v: k for k, v in COLORS.items()}
colors_convert = lambda colorname: COLORS[colorname]

# upwards direction
ORDER_VERTICAL_NAMES_CYCLE1 = ["orange", "yellow", "red", "white"]
ORDER_VERTICAL_NAMES_CYCLE2 = ["blue", "yellow", "green", "white"]

ORDER_VERTICAL_CYCLE1 = list(map(colors_convert, ORDER_VERTICAL_NAMES_CYCLE1))
ORDER_VERTICAL_CYCLE2 = list(map(colors_convert, ORDER_VERTICAL_NAMES_CYCLE2))
# right-bound direction
ORDER_HORIZONTAL_NAMES_CYCLE = ["orange", "blue", "red", "green"]
ORDER_HORIZONTAL_CYCLE = list(map(colors_convert, ORDER_HORIZONTAL_NAMES_CYCLE))


def right(color: int) -> int:
    idx = ORDER_HORIZONTAL_CYCLE.index(color)
    idx_right = (idx + 1) % 4
    return ORDER_HORIZONTAL_CYCLE[idx_right]


def left(color: int) -> int:
    idx = ORDER_HORIZONTAL_CYCLE.index(color)
    idx_left = (idx - 1) % 4
    return ORDER_HORIZONTAL_CYCLE[idx_left]


def color_index(color: int) -> list[int]:
    idx = None
    if color == COLOR_WHITE or color == COLOR_YELLOW:
        raise Exception(
            "Directions are not defined for White/Yellow. They are assumed to be at the bottom/top"
        )
    try:
        idx = ORDER_VERTICAL_CYCLE1.index(color)
        whichlist = ORDER_VERTICAL_CYCLE1
    except ValueError:
        try:
            idx = ORDER_VERTICAL_CYCLE2.index(color)
            whichlist = ORDER_VERTICAL_CYCLE2
        except ValueError:
            raise Exception("Invalid color given")
    return idx, whichlist


def up(color: int) -> int:
    idx, whichlist = color_index(color)
    idx_up = (idx + 1) % 4
    return whichlist[idx_up]


def down(color: int) -> int:
    idx, whichlist = color_index(color)
    idx_down = (idx - 1) % 4
    return whichlist[idx_down]
