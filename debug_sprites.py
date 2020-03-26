import pygame as pg


class colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (192, 192, 192)
    DARK_RED = (128, 16, 16)


class RectangleSprite(pg.sprite.Sprite):
    def __init__(self, color, size):
        super().__init__()
        size = (int(size[0]), int(size[1]))
        self.image = pg.Surface(size)
        self.image.fill(color)

        self.rect = self.image.get_rect()


class CircleSprite(pg.sprite.Sprite):
    def __init__(self, color, radius):
        super().__init__()
        radius = int(radius)
        self.image = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
        pg.draw.circle(self.image, color, (radius, radius), radius)

        self.rect = self.image.get_rect()
