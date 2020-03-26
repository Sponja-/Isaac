import pygame as pg
from game_object import GameObject, Event
from physics import RigidBody, Vector, CircleCollider
from debug_sprites import CircleSprite,  colors
from tears import PlayerTear
import layers

SQRT_2 = 2 ** .5
INVULNERABLE_TIME = 1


class Player(GameObject):
    def __init__(self, *, position):
        self.body = RigidBody(collider=CircleCollider,
                              position=position,
                              radius=20,
                              damping=3.5)

        self.sprite = CircleSprite(colors.BLACK, self.body.collider.radius)
        self.layer = layers.PLAYER

        # Stats
        self.stats = {
            "Speed": 1000,
            "Damage": 50,
            "Shot Speed": 300,
            "Range": 600,
            "Tears": 10
        }

        self.pickups = {
            "Coins": 0,
            "Bombs": 0,
            "Keys": 0
        }

        self.on_move = Event("move")
        self.on_fire = Event("fire")
        self.on_heal = Event("heal")
        self.on_damage = Event("damage")

        self.on_update += move
        self.on_update += fire

        self.life = 3
        self.can_shoot = True
        self.invulnerable = False

    def damage(self, amount=.5):
        if self.invulnerable:
            return False

        self.life -= amount
        self.invulnerable = True

        def reset_invulnerable():
            self.invulnerable = False

        self.game.add_wait(INVULNERABLE_TIME, reset_invulnerable)

        self.on_damage.dispatch(self, amount)
        return True

    def heal(self, amount):
        self.life += amount
        self.on_heal.dispatch(self, amount)


def move(self, delta_time):
    keys = pg.key.get_pressed()
    movement_axes = 0
    move_force = Vector(0, 0)
    speed = self.stats["Speed"]

    if keys[pg.K_w]:
        movement_axes += 1
        move_force += (0, -speed)
    elif keys[pg.K_s]:
        movement_axes += 1
        move_force += (0, speed)
    if keys[pg.K_a]:
        movement_axes += 1
        move_force += (-speed, 0)
    elif keys[pg.K_d]:
        movement_axes += 1
        move_force += (speed, 0)

    if movement_axes == 2:
        move_force /= SQRT_2

    if movement_axes:
        self.body.add_force(move_force)
        self.on_move.dispatch(self, delta_time)


def fire(self, delta_time):
    keys = pg.key.get_pressed()
    if not self.can_shoot:
        return

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
        return

    tear = PlayerTear(position=self.body.collider.center(),
                      velocity=velocity,
                      range=self.stats["Range"],
                      damage=self.stats["Damage"])
    self.game.add(tear)
    self.can_shoot = False

    def reset_shoot():
        self.can_shoot = True

    self.game.add_wait(self.stats["Tears"] / 10, reset_shoot)

    self.on_fire.dispatch(self, tear)
