from game_object import GameObject
from physics import CircleCollider, KinematicBody, Vector
from debug_sprites import CircleSprite, colors
import layers


def damage_to_radius(damage):
    return int(damage / 10)


class PlayerTear(GameObject):
    def __init__(self, *, position, velocity, range, damage, **kwargs):
        radius = kwargs.get("radius", damage_to_radius(damage))

        self.body = KinematicBody(collider=CircleCollider,
                                  radius=radius,
                                  position=position,
                                  velocity=velocity)

        self.sprite = CircleSprite(colors.BLUE, radius)

        self.layer = layers.PLAYER_TEARS

        self.speed = kwargs.get("speed", Vector(*velocity).magnitude())
        self.remaining_range = range

        self.damage = damage

    def update(self, delta_time):
        self.remaining_range -= self.speed * delta_time

    def on_collide(self, other):
        if other.layer == layers.ENEMIES:
            other.do_damage(self.damage)
            self.kill()
