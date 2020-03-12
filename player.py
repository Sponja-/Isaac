import pygame as pg
from game_object import GameObject
from physics import RigidBody, Vector, RectCollider
from debug_sprites import RectangleSprite, colors
from tears import PlayerTear
import layers

SQRT_2 = 2 ** .5


class Player(GameObject):
    def __init__(self):
        self.body = RigidBody(collider=RectCollider,
                              position=(50, 50),
                              size=(30, 50),
                              damping=3.5)

        self.sprite = RectangleSprite(colors.BLACK, self.body.collider.size())
        self.layer = layers.PLAYER

        # Stats
        self.stats = {
            "Speed": 60000,
            "Damage": 50,
            "Shot Speed": 400,
            "Range": 300,
            "Tears": 10
        }

        self.tear_delay = 0

    def update(self, delta_time):
        keys = pg.key.get_pressed()

        if self.tear_delay > 0:
            self.tear_delay -= delta_time

        moved = self.do_movement(delta_time, keys)
        fired = self.do_fire(delta_time, keys)

    def do_movement(self, delta_time, keys):
        movement_axes = 0
        move_force = Vector(0, 0)
        speed = self.stats["Speed"]

        if keys[pg.K_w]:
            movement_axes += 1
            move_force += (0, -speed * delta_time)
        elif keys[pg.K_s]:
            movement_axes += 1
            move_force += (0, speed * delta_time)
        if keys[pg.K_a]:
            movement_axes += 1
            move_force += (-speed * delta_time, 0)
        elif keys[pg.K_d]:
            movement_axes += 1
            move_force += (speed * delta_time, 0)

        if movement_axes == 2:
            move_force /= SQRT_2

        if movement_axes:
            self.body.add_force(move_force)
            return True
        else:
            return False

    def do_fire(self, delta_time, keys):
        if self.tear_delay > 0:
            return False

        shot_speed = self.stats["Shot Speed"]
        if keys[pg.K_UP]:
            velocity = Vector(0, -shot_speed)
        elif keys[pg.K_DOWN]:
            velocity = Vector(0, shot_speed)
        elif keys[pg.K_LEFT]:
            velocity = Vector(-shot_speed, 0)
        elif keys[pg.K_RIGHT]:
            velocity = Vector(shot_speed, 0)
        else:
            return False

        tear = PlayerTear(position=self.body.collider.center(),
                          velocity=velocity,
                          range=self.stats["Range"],
                          damage=self.stats["Damage"])
        self.game.add(tear)
        self.tear_delay = self.stats["Tears"] / 10  # Temporary
        return True
