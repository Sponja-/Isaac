from game_object import GameObject
from physics import RigidBody, RectCollider
from debug_sprites import RectSprite, colors
from globals import types, TILE_SIZE
from physics import CircleCollider
from debug_sprites import CircleSprite
import layers


class Destructible(GameObject):
    def destroy(self):
        self.kill()


class Rock(Destructible):
    def __init__(self, position):
        self.body = RigidBody(collider=RectCollider,
                              position=position,
                              size=(TILE_SIZE, TILE_SIZE),
                              mass=0)

        self.sprite = RectSprite(colors.BLACK, self.body.collider.size())

        self.layer = layers.OBSTACLES


types["Rock"] = Rock
