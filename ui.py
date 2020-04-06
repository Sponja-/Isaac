import pygame as pg

pg.font.init()

TextSmall = pg.font.Font(pg.font.get_default_font(), 12)
TextNormal = pg.font.Font(pg.font.get_default_font(), 24)
TextLarge = pg.font.Font(pg.font.get_default_font(), 36)

SMALL = 0
NORMAL = 1
LARGE = 2

fonts = [TextSmall, TextNormal, TextLarge]


class UIElement:
    def __init__(self, name, *, position, image):
        self.name = name
        self.image = image
        self.position = position
        self.enabled = True

    def get_render(self):
        return self.image


class Text(UIElement):
    def __init__(self, name, *, position, text, type=1, color=(0, 0, 0)):
        self._text = text
        self._color = color
        self.type = type
        super().__init__(name, position=position, image=self.get_surface())

    def get_surface(self):
        return fonts[self.type].render(self.text, True, self.color)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.image = self.get_surface()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self.image = self.get_surface()
