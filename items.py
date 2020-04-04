from game_object import GameObject
from physics import RigidBody, CircleCollider
from debug_sprites import CircleSprite, colors
from globals import types
import health
import layers

from abc import abstractmethod
from random import randint


class Pedestal(GameObject):
    def __init__(self, *, position, item=None, pool=None):
        self.body = RigidBody(collider=CircleCollider,
                              position=position,
                              radius=20,
                              mass=0)

        self.sprite = CircleSprite(colors.YELLOW, 20)

        self.layer = layers.OBSTACLES

        if item is not None:
            self.item = item
        else:
            self.item = pools[pool].get()

        self.on_collide += pedestal_collide


def pedestal_collide(self, other):
    if other.layer == layers.PLAYER:
        self.item = other.acquire_item(self.item)
        if self.item is None:
            self.kill()


class ItemPool:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def get(self):
        if self.items:
            i = randint(0, len(self.items) - 1)
            return self.items.pop(i)()
        else:
            return Breakfast()


pools = {
    "gold": ItemPool(),
    "boss": ItemPool()
}


class ItemCreator(type):
    id = 0
    items = []
    item_dict = {}

    def __init__(self, name, bases, dict):
        if "pools" in dict:
            self.id = ItemCreator.id
            ItemCreator.id += 1
            ItemCreator.items.append(self)
            self.name = name
            ItemCreator.item_dict[name] = self

            for pool_name in dict["pools"]:
                pools[pool_name].add(self)


class Item(metaclass=ItemCreator):
    @abstractmethod
    def on_pickup(self, player):
        pass


class ActiveItem(Item):
    @abstractmethod
    def on_use(self, player):
        pass


class Breakfast(Item):
    pools = ["gold", "boss"]

    def on_pickup(self, player):
        player.add_hearts(1)
        player.heal(health.RED_HEART)


types["Pedestal"] = Pedestal
