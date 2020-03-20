from game_object import GameObject
from physics import RigidBody, CircleCollider
from debug_sprites import CircleSprite, colors
import layers


class Pickup(GameObject):
    def __init__(self, position, sprite, **kwargs):
        self.body = RigidBody(collider=CircleCollider,
                              position=position,
                              radius=10)
        self.sprite = sprite
        self.layer = layers.PICKUPS

        self.on_collide += type(self).action

    def action(self, player):
        pass


class Key(Pickup):
    def __init__(self, *, position):
        super().__init__(position, CircleSprite(colors.LIGHT_GRAY, 10))

    def action(self, player):
        player.pickups["Keys"] += 1
        self.kill()


class Bomb(Pickup):
    def __init__(self, *, position):
        super().__init__(position, CircleSprite(colors.GRAY, 10))

    def action(self, player):
        player.pickups["Bombs"] += 1
        self.kill()


class Coin(Pickup):
    def __init__(self, *, position):
        super().__init__(position, CircleSprite(colors.YELLOW, 10))

    def action(self, player):
        player.pickups["Coins"] += 1
        self.kill()


class Heart(Pickup):
    def __init__(self, *, position):
        super().__init__(position, CircleSprite(colors.DARK_RED, 10))

    def action(self, player):
        player.life += 1.0
        self.kill()
