from physics import RectCollider, CircleCollider, Vector
from math import sin, cos, atan, pi
import layers


n = 10  # Number of vertices of the regular polygons circles are converted into


class Graph:  # bidirectional
    def __init__(self):
        self.elements = {}

    def add_vertex(self, v):
        self.elements[v] = []

    def add_edge(self, frm, to):
        self.elements[frm].append(to)
        self.elements[to].append(frm)


def create_visibility_graph(objects, *, avoid_space=5):
    polygons = get_polygons(objects, avoid_space)


def get_polygons(objects, avoid_space):
    result = []
    for obj in objects:
        if obj.layer == layers.OBSTACLES:
            collider = obj.body.collider
            result.append(polygonized[collider](collider, avoid_space))


def polygonize_AABB(collider, e):
    p = collider.top_left()
    w, h = collider.width, collider.height
    angle = atan(h / w)
    e_x, e_y = angle * cos(e), angle * sin(e)
    return (
        p + (-e_x, -e_y),
        p + (w + e_x, -e_y),
        p + (w + e_x, h + e_y),
        p + (-e_x, h + e_y)
    )


def polygonize_circle(collider, e):
    c = collider.center()
    apothem = collider.radius
    r = (apothem + e) / cos(pi / n)
    angles = [i * (2*pi / n) for i in range(n)]
    return tuple(c + (r * cos(alpha), r * sin(alpha)) for alpha in angles)


polygonized = {
    RectCollider: polygonize_AABB,
    CircleCollider: polygonize_circle
}
