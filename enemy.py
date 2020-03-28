from game_object import GameObject
from physics import RigidBody, CircleCollider
from debug_sprites import CircleSprite, colors
from globals import types
import layers


class Enemy(GameObject):
    def __init__(self, *, health):
        self.layer = layers.ENEMIES
        self.health = health

        self.on_collide += enemy_damage
        self.on_kill += lambda self: self.game.enemy_died()

    def damage(self, amount):
        self.health -= amount

        if self.health <= 0:
            self.kill()
            self.game.player.on_enemy_kill.dispatch(self)


def enemy_damage(self, other):
    if other.layer == layers.PLAYER:
        other.damage()


class Fly(Enemy):
    def __init__(self, *, position):
        super().__init__(health=100.0)
        self.body = RigidBody(collider=CircleCollider,
                              position=position,
                              radius=10,
                              mass=1,
                              damping=2)

        self.sprite = CircleSprite(colors.DARK_RED, self.body.collider.radius)
        self.speed = 300

        self.on_update += fly_ai


def fly_ai(self, delta_time):
    player = self.game.player
    vec = (player.body.collider.center() - self.body.collider.center()).normal()
    self.body.add_force(vec * self.speed)


types["Fly"] = Fly
