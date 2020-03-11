import pygame as pg


class colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)


class RectangleSprite(pg.sprite.Sprite):
    def __init__(self, color, size):
        super().__init__()
        self.image = pg.Surface(list(size))
        self.image.fill(color)

        self.rect = self.image.get_rect()
