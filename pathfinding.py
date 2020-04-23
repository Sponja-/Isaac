from physics import Vector
from globals import TILE_SIZE
from numpy import sign


def line_tiles(start, end):  # Bresenham's line rasterization only for 1st octant
    delta = end - start
    delta_err = abs(delta.y / delta.x)
    error = 0
    result = []
    y = start.y
    print(delta)
    for x in range(start.x, end.x + 1, sign(delta.x)):
        result.append((x, y))
        error += delta_err
        if error >= .5:
            y += sign(delta.y)
            error -= 1
    return result

