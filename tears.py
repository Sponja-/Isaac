from game_object import GameObject
from physics import CircleCollider, KinematicBody, Vector
from debug_sprites import CircleSprite, colors
import layers


def damage_to_radius(damage):
    return int(damage / 5)


class PlayerTear(GameObject):
    def __init__(self, *, position, velocity, range, damage, **kwargs):
        radius = kwargs.get("radius", damage_to_radius(damage))

        self.body = KinematicBody(collider=CircleCollider,
                                  radius=radius,
                                  position=position,
                                  velocity=velocity,
                                  disable_collide=True)

        self.sprite = CircleSprite(colors.BLUE, radius)

        self.layer = layers.PLAYER_TEARS

        self.speed = kwargs.get("speed", Vector(*velocity).magnitude())
        self.remaining_range = range

        self.damage = damage

        self.on_update += check_range
        self.on_collide += collision


def collision(self, other):
    if other.layer == layers.ENEMIES:
        other.do_damage(self.damage)
        self.kill()
    if other.layer == layers.OBSTACLES:
        self.kill()


def check_range(self, delta_time):
    self.remaining_range -= self.speed * delta_time
    if self.remaining_range <= 0:
        self.kill()
