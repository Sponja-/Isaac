import pygame as pg
from game_object import GameObject
from rigidbody import RigidBody, Vector
from debug_sprites import RectangleSprite, colors


class Player(GameObject):
    def __init__(self):
        self.body = RigidBody(size=(30, 50), position=(50, 50), damping=2)

        self.sprite = RectangleSprite(colors.BLACK, self.body.size)

        # Stats
        self.speed = 10000

    def update(self, delta_time):
        print(self.body.position)
        keys = pg.key.get_pressed()

        self.do_movement(delta_time, keys)
        self.do_fire(delta_time, keys)

        super().update(delta_time)

    def do_movement(self, delta_time, keys):
        if keys[pg.K_w]:
            self.body.add_force(Vector(0, -self.speed * delta_time))  # Moving diagonally is faster, change magnitude
        elif keys[pg.K_s]:
            self.body.add_force(Vector(0, self.speed * delta_time))
        if keys[pg.K_d]:
            self.body.add_force(Vector(self.speed * delta_time, 0))
        elif keys[pg.K_a]:
            self.body.add_force(Vector(-self.speed * delta_time, 0))

    def do_fire(self, delta_time, keys):
        pass
