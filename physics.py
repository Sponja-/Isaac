import numpy as np
from functools import wraps
from copy import copy
from abc import ABC, abstractmethod


def vector_argument(function):
    @wraps(function)
    def vector_arg_only(self, arg):
        if type(arg) is not Vector:
            arg = Vector(*arg)
        return function(self, arg)
    return vector_arg_only


class Vector:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    @vector_argument
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    @vector_argument
    def __radd__(self, other):
        return self.__add__(other)

    @vector_argument
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    @vector_argument
    def __rsub__(self, other):
        return other.__sub__(self)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    @vector_argument
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    @vector_argument
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

    def __iter__(self):
        yield self.x
        yield self.y

    def __copy__(self):
        return Vector(self.x, self.y)

    def sqr_magnitude(self):
        return self.x * self.x + self.y * self.y

    def magnitude(self):
        return np.sqrt(self.sqr_magnitude())


class IBody(ABC):
    def __init__(self, collider, **kwargs):
        if isinstance(collider, type):
            self.collider = collider(**kwargs)
        elif isinstance(collider, ICollider):
            self.collider = collider
        else:
            raise TypeError(collider)

    @abstractmethod
    def update(self, delta_time):
        pass


class RigidBody(IBody):
    def __init__(self, *, collider, **kwargs):
        super().__init__(collider, **kwargs)

        self.velocity = Vector(0, 0)
        self.total_force = Vector(0, 0)

        self.mass = kwargs.get("mass", 1.0)
        self.damping = kwargs.get("damping", 0.5)

    def update(self, delta_time):
        self.velocity += delta_time * self.total_force / self.mass
        self.collider.move(delta_time * self.velocity)

        self.total_force = Vector(0, 0)
        self.add_force(-self.velocity * self.damping)

    @vector_argument
    def add_force(self, force):
        self.total_force += force


class KinematicBody(IBody):
    def __init__(self, *, collider, **kwargs):
        super().__init__(collider, **kwargs)
        self.velocity = Vector(*kwargs["velocity"])

    def update(self, delta_time):
        self.collider.move(delta_time * self.velocity)


class ICollider(ABC):
    @abstractmethod
    def top_left(self):
        pass

    @abstractmethod
    def center(self):
        pass

    @abstractmethod
    def is_colliding(self, other):
        pass

    @abstractmethod
    def move(self, move_vector):
        pass

    @abstractmethod
    def move_to(self, new_center):
        pass


class RectCollider(ICollider):
    def __init__(self, size, position, **kwargs):
        self.width, self.height = size
        self._position = position - self._half_diagonal()

    def _half_diagonal(self):
        return Vector(self.width / 2, self.height / 2)

    def size(self):
        return (self.width, self.height)

    @vector_argument
    def move(self, move_vector):
        self._position += move_vector

    @vector_argument
    def move_to(self, new_center):
        self._position = new_center - self._half_diagonal()

    def top_left(self):
        return self._position

    def center(self):
        return self._position + self._half_diagonal()

    def is_colliding(self, other):
        if type(other) is RectCollider:
            return collisionRectRect(self, other)
        if type(other) is CircleCollider:
            return collisionRectCircle(self, other)


class CircleCollider(ICollider):
    def __init__(self, radius, position, **kwargs):
        self.radius = radius
        self._position = position

    @vector_argument
    def move(self, move_vector):
        self._position += move_vector

    @vector_argument
    def move_to(self, new_center):
        self._position = new_center

    def top_left(self):
        return self._position - (self.radius, self.radius)

    def center(self):
        return self._position

    def is_colliding(self, other):
        if type(other) is RectCollider:
            return collisionRectCircle(other, self)
        if type(other) is CircleCollider:
            return collisionCircleCircle(self, other)


def collisionRectRect(r1, r2):
    return (r1.top_left().x < r2.top_left().x + r2.width and
            r1.top_left().x + r1.width > r2.top_left().x and
            r1.top_left().y < r2.top_left().y + r2.height and
            r1.top_left().y + r1.height > r2.top_left().y)


def collisionCircleCircle(c1, c2):
    return (c1.center() - c2.center()).sqr_magnitude() <= (c1.radius + c2.radius) ** 2


def collisionRectCircle(r, c):
    closest_point = copy(c.center())
    if closest_point.x < r.top_left().x:
        closest_point.x = r.top_left().x
    elif closest_point.x > r.top_left().x + r.width:
        closest_point.x = r.top_left().x + r.width
    if closest_point.y < r.top_left().y:
        closest_point.y = r.top_left().y
    elif closest_point.y > r.top_left().y + r.height:
        closest_point.y = r.top_left().y + r.height

    return (closest_point - c.center()).sqr_magnitude() <= c.radius ** 2
