from game_object import GameObject
from physics import KinematicBody, CircleCollider
from debug_sprites import CircleSprite, colors
from items import Item
from pickups import Pickup
import layers


class SellingPedestal(GameObject):
    def __init__(self, *, position, object, cost):
        self.body = KinematicBody(collider=CircleCollider,
                                  position=position,
                                  radius=20)

        self.sprite = CircleSprite(colors.BLACK, 20)

        self.layer = layers.OBSTACLES
        self.object = object
        self.cost = cost

        self.on_collide += sell_collide


def sell_collide(self, player):
    if player.layer == layers.PLAYER:
        if player.coins >= self.cost:
            player.coins -= self.cost
            if isinstance(self.object, Item):
                player.acquire_item(self.object)
            elif isinstance(self.object, Pickup):
                self.object.do_pickup(player)
            self.kill()