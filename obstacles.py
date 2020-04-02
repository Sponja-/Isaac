from game_object import GameObject, Event
from physics import RigidBody, RectCollider
from debug_sprites import RectSprite, colors
from globals import types, TILE_SIZE
import layers


class Destructible(GameObject):
    def __init__(self):
        self.on_destroy = Event("destroy")

    def destroy(self):
        self.on_destroy.dispatch(self)
        self.kill()


class Rock(Destructible):
    def __init__(self, position):
        super().__init__()
        self.body = RigidBody(collider=RectCollider,
                              position=position,
                              size=(TILE_SIZE, TILE_SIZE),
                              mass=0)

        self.sprite = RectSprite(colors.BLACK, self.body.collider.size())

        self.layer = layers.OBSTACLES


types["Rock"] = Rock
