import numpy as np


class Vector:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __itruediv__(self, other):
        self.x /= other
        self.y /= other
        return self

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def sqr_magnitude(self):
        return self.x * self.x + self.y * self.y

    def magnitude(self):
        return np.sqrt(self.sqr_magnitude)


class RigidBody:
    def __init__(self, **kwargs):
        self.size = tuple(kwargs.get("size"))
        self.position = Vector(*kwargs.get("position", (0, 0)))
        self.velocity = Vector(0, 0)
        self.total_force = Vector(0, 0)

        self.mass = kwargs.get("mass", 1.0)
        self.damping = kwargs.get("damping", 0.5)

    def update(self, delta_time):
        self.velocity += delta_time * self.total_force / self.mass
        self.position += delta_time * self.velocity
        self.total_force = Vector(0, 0)

        self.add_force(-self.velocity * self.damping)

    def add_force(self, force):
        self.total_force += force
