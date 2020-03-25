from game_object import GameObject
from physics import RigidBody, RectCollider, CircleCollider
from debug_sprites import RectangleSprite, CircleSprite, colors
import layers


class Rock(GameObject):
    def __init__(self, position):
        self.body = RigidBody(collider=RectCollider,
                              position=position,
                              size=(30, 30),
                              mass=0)

        self.sprite = RectangleSprite(colors.BLACK, self.body.collider.size())

        self.layer = layers.OBSTACLES


class CircleRock(GameObject):
    def __init__(self, position):
        self.body = RigidBody(collider=CircleCollider,
                              position=position,
                              radius=20,
                              mass=0)

        self.sprite = CircleSprite(colors.BLACK, self.body.collider.radius)

        self.layer = layers.OBSTACLES
