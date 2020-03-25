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

    def normal(self):
        return self / self.magnitude()

    def normalize(self):
        mag = self.magnitude()
        self.x /= mag
        self.y /= mag

    @vector_argument
    def dot(self, other):
        return self.x * other.x + self.y * other.y


class IBody(ABC):
    def __init__(self, collider, **kwargs):
        if isinstance(collider, type):
            self.collider = collider(**kwargs)
        elif isinstance(collider, ICollider):
            self.collider = collider
        else:
            raise TypeError(collider)

        self.disable_collide = False

    @abstractmethod
    def update(self, delta_time):
        pass

    def do_collision(self, other):
        if not self.disable_collide:
            self.collide(other)


class RigidBody(IBody):
    def __init__(self, *, collider, **kwargs):
        super().__init__(collider, **kwargs)

        self.velocity = Vector(0, 0)
        self.total_force = Vector(0, 0)

        mass = kwargs.get("mass", 1.0)
        self.inverse_mass = 1 / kwargs.get("mass", 1.0) if mass != 0 else 0
        self.damping = kwargs.get("damping", 0.5)
        self.restitution = kwargs.get("restitution", -.7)
        self.disable_collide = kwargs.get("disable_collide", False)

    def update(self, delta_time):
        self.velocity += delta_time * self.total_force * self.inverse_mass
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

    def bottom_right(self):
        return self._position + (self.width, self.height)

    def center(self):
        return self._position + self._half_diagonal()

    def is_colliding(self, other):
        if type(other) is RectCollider:
            return detectCollisionRectRect(self, other)
        if type(other) is CircleCollider:
            return detectCollisionRectCircle(self, other)


class CircleCollider(ICollider):
    def __init__(self, radius, position, **kwargs):
        self.radius = radius
        self._position = copy(position)

    @vector_argument
    def move(self, move_vector):
        self._position += move_vector

    @vector_argument
    def move_to(self, new_center):
        self._position = new_center

    def top_left(self):
        return self._position - (self.radius, self.radius)

    def bottom_right(self):
        return self._position + (self.radius, self.radius)

    def center(self):
        return self._position

    def is_colliding(self, other):
        if type(other) is RectCollider:
            return detectCollisionRectCircle(other, self)
        if type(other) is CircleCollider:
            return detectCollisionCircleCircle(self, other)


def clamp(n, low, high):
    return max(low, min(n, high))


def findClosest(r, c):
    closest_point = copy(c.center())
    closest_point.x = clamp(closest_point.x, r.top_left().x, r.top_left().x + r.width)
    closest_point.y = clamp(closest_point.y, r.top_left().y, r.top_left().y + r.height)
    return closest_point


def detectCollisionRectRect(r1, r2):
    return (r1.top_left().x < r2.top_left().x + r2.width and
            r1.top_left().x + r1.width > r2.top_left().x and
            r1.top_left().y < r2.top_left().y + r2.height and
            r1.top_left().y + r1.height > r2.top_left().y)


def detectCollisionCircleCircle(c1, c2):
    return (c1.center() - c2.center()).sqr_magnitude() <= (c1.radius + c2.radius) ** 2


def detectCollisionRectCircle(r, c):
    return (findClosest(r, c) - c.center()).sqr_magnitude() <= c.radius ** 2


#  Returns (normal, penetration)
def resolveCollisionCircleCircle(c1, c2):
    vec = c1.center() - c2.center()
    distance = vec.magnitude()
    return (vec / distance, c1.radius + c2.radius - distance)


def resolveCollisionRectRect(r1, r2):
    vec = r2.top_left() - r1.top_left()
    x_overlap = r1.width / 2 + r2.width / 2 - abs(vec.x)
    y_overlap = r1.height / 2 + r2.height / 2 - abs(vec.y)
    if x_overlap > y_overlap:
        if vec.x < 0:
            normal = Vector(-1, 0)
        else:
            normal = Vector(1, 0)
        penetration = x_overlap
    else:
        if vec.y < 0:
            normal = Vector(0, -1)
        else:
            normal = Vector(0, 1)
        penetration = y_overlap
    return (normal, penetration)


def resolveCollisionRectCircle(r, c):
    rect_center = r.center()

    difference = c.center() - rect_center
    closest = findClosest(r, c)

    if closest == c.center():
        inside = True
        if abs(difference.x) > abs(difference.y):
            if closest.x > r.top_left().x + r.width / 2:
                closest.x = r.top_left().x + r.width
            else:
                closest.x = r.top_left().x
        else:
            if closest.y > r.top_left().y + r.height / 2:
                closest.y = r.top_left().y + r.height
            else:
                closest.y = r.top_left().y
    else:
        inside = False

    normal = closest - c.center()
    penetration = c.radius - normal.magnitude()
    return (normal if not inside else -normal, penetration)


def resolveCollision(a, b, delta_time):
    if type(a) is KinematicBody or type(b) is KinematicBody:
        return
    if type(a.collider) is RectCollider:
        if type(b.collider) is RectCollider:
            normal, penetration = resolveCollisionRectRect(a.collider, b.collider)
        elif type(b.collider) is CircleCollider:
            normal, penetration = resolveCollisionRectCircle(a.collider, b.collider)
    elif type(a.collider) is CircleCollider:
        if type(b.collider) is CircleCollider:
            normal, penetration = resolveCollisionCircleCircle(a.collider, b.collider)
        elif type(b.collider) is RectCollider:
            normal, penetration = resolveCollisionRectCircle(b.collider, a.collider)
            normal *= -1

    relative_velocity = a.velocity - b.velocity
    velocity_on_normal = relative_velocity.dot(normal)

    #e = min(a.restitution, b.restitution)

    #j = -(1 + e) * velocity_on_normal
    #j /= a.inverse_mass + b.inverse_mass

    #impulse = j * normal
    #a.velocity += impulse * a.inverse_mass * delta_time
    #b.velocity -= impulse * b.inverse_mass * delta_time

    percent = .1
    correction = (penetration / (a.inverse_mass + b.inverse_mass)) * percent * normal
    a.collider.move(a.inverse_mass * correction)
    b.collider.move(-b.inverse_mass * correction)
