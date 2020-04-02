from game_object import GameObject
from physics import RigidBody, KinematicBody, CircleCollider, normalized_direction
from debug_sprites import CircleSprite, colors
from obstacles import Destructible
import layers


class PlacedBomb(GameObject):
    def __init__(self, *, blast_radius=80, delay=3, damage=100, position):
        self.body = RigidBody(collider=CircleCollider,
                              position=position,
                              radius=10,
                              mass=.5)
        self.sprite = CircleSprite(colors.DARK_GRAY, 10)

        self.layer = layers.OBSTACLES

        self.on_mount += bomb_mounted
        self.on_kill += bomb_explode

        self.body.disable_collide = True
        self.delay = delay
        self.blast_radius = blast_radius
        self.damage = damage


def bomb_mounted(self):
    def enable_collide():
        self.body.disable_collide = False

    self.game.add_timer(1, enable_collide)
    self.game.add_timer(self.delay, self.kill)


def bomb_explode(self):
    self.game.add(Explosion(radius=self.blast_radius,
                            damage=self.damage,
                            position=self.body.collider.center()))


class Explosion(GameObject):
    def __init__(self, *, radius, damage, position):
        self.body = KinematicBody(collider=CircleCollider,
                                  position=position,
                                  radius=radius,
                                  velocity=(0, 0))

        self.sprite = CircleSprite(colors.LIGHT_GRAY, radius)

        self.layer = layers.EXPLOSIONS

        self.on_update += explosion_update
        self.on_collide += explosion_collide

        self.remaining_ticks = 2
        self.damage = damage


def explosion_collide(self, other):
    if self.remaining_ticks == 1:
        if other.layer == layers.PLAYER:
            other.damage()
        elif other.layer == layers.ENEMIES:
            other.damage(self.damage)
        elif other.layer == layers.OBSTACLES and isinstance(other, Destructible):
            other.destroy()

        if isinstance(other.body, RigidBody):
            other.body.add_force(normalized_direction(self, other) * 20000)


def explosion_update(self, delta_time):
    self.remaining_ticks -= 1
    if self.remaining_ticks == 0:
        self.kill()
