from game_object import GameObject
from physics import RigidBody, RectCollider, CircleCollider
from debug_sprites import RectangleSprite, CircleSprite, colors
from globals import types, TILE_SIZE
import layers


class Rock(GameObject):
    def __init__(self, position):
        self.body = RigidBody(collider=RectCollider,
                              position=position,
                              size=(TILE_SIZE, TILE_SIZE),
                              mass=0)

        self.sprite = RectangleSprite(colors.BLACK, self.body.collider.size())

        self.layer = layers.OBSTACLES


types["Rock"] = Rock
