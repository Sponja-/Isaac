from game_object import GameObject
from physics import RigidBody, CircleCollider
from debug_sprites import CircleSprite, colors
from globals import types
import health
import layers


class Pickup(GameObject):
    def __init__(self, position, sprite, **kwargs):
        self.body = RigidBody(collider=CircleCollider,
                              position=position,
                              radius=10,
                              mass=.2)
        self.sprite = sprite
        self.layer = layers.PICKUPS

        def do_pickup(self, player):
            if not self.action(player):
                self.kill()

        self.on_collide += do_pickup

    def action(self, player):
        pass


class Key(Pickup):
    def __init__(self, *, position):
        super().__init__(position, CircleSprite(colors.LIGHT_GRAY, 10))

    def action(self, player):
        player.pickups["Keys"] += 1


class Bomb(Pickup):
    def __init__(self, *, position):
        super().__init__(position, CircleSprite(colors.GRAY, 10))

    def action(self, player):
        player.pickups["Bombs"] += 1


class Coin(Pickup):
    def __init__(self, *, position):
        super().__init__(position, CircleSprite(colors.YELLOW, 10))

    def action(self, player):
        player.pickups["Coins"] += 1


class Heart(Pickup):
    def __init__(self, *, position):
        super().__init__(position, CircleSprite(colors.DARK_RED, 10))

    def action(self, player):
        return not player.heal(health.RED_HEART)


types["Key"] = Key
types["Bomb"] = Bomb
types["Coin"] = Coin
types["Heart"] = Heart
