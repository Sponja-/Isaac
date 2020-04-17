from abc import ABC, abstractmethod
from physics import Vector
import pygame as pg

pg.font.init()

SMALL = 0
NORMAL = 1
LARGE = 2

fonts = [
    pg.font.Font(pg.font.get_default_font(), 12),
    pg.font.Font(pg.font.get_default_font(), 24),
    pg.font.Font(pg.font.get_default_font(), 36)
]


DEFAULT_ALPHA = (255, 0, 255)


class TriggerGetImage:
    def __init__(self, prop_name):
        self.prop_name = prop_name

    def __get__(self, instance):
        return getattr(instance, self.prop_name)

    def __set__(self, instance, value):
        setattr(instance, self.prop_name, value)
        instance.image = instance.get_image()


class UIElement(ABC):
    def __init__(self, name, *, position):
        self.name = name
        self.position = position
        self.enabled = True

    @abstractmethod
    def get_render(self):
        pass

    def on_mount(self):
        pass


class StaticImage(UIElement):
    def __init__(self, name, *, position, image):
        super().__init__(name, position=position)
        self.image = image

    def get_render(self):
        return self.image


class Text(StaticImage):
    text = TriggerGetImage("_text")
    color = TriggerGetImage("_color")
    bg_color = TriggerGetImage("_bg_color")

    def __init__(self, name, *, position, text, type=1, color=(0, 0, 0), bg_color=None):
        self._text = text
        self._color = color
        self._bg_color = bg_color
        self.type = type
        super().__init__(name, position=position, image=self.get_image())

    def get_image(self):
        if self.bg_color is None:
            return fonts[self.type].render(self.text, True, self.color)
        else:
            surface = fonts[self.type].render(self.text, True, self.color)
            surface.set_colorkey(self.bg_color)
            return surface


class UIGroup(UIElement):
    def __init__(self, name, *, position, size, bg_color=DEFAULT_ALPHA, alpha=True, static=True):
        super().__init__(name, position=position)
        self.bg_color = bg_color
        self.size = size
        self.alpha = alpha
        self.static = static
        self.elements = {}
        self.update()

    def add(self, element, *, global_position=False):
        self.elements[element.name] = element
        if global_position:
            element.position = (element.position[0] - self.position[0],
                                element.position[1] - self.position[1])

        if type(element) is Text and self.alpha:
            element.bg_color = self.bg_color

        self.update()

    def remove(self, name):
        del self.element[name]
        self.update()

    def move_element(self, name, new_position, *, global_position=False):
        element = self.elements[name]
        if global_position:
            element.position = (element.position[0] - new_position[0],
                                element.position[1] - new_position[1])
        else:
            element.position = new_position

        self.update()

    def get_image(self):
        result = pg.Surface(self.size)
        result.fill(self.bg_color)
        if self.alpha:
            result.set_colorkey(self.bg_color)

        for name, element in self.elements.items():
            result.blit(element.get_render(), element.position)

        return result

    def update(self):
        self.image = self.get_image()

    def get_render(self):
        if self.static:
            return self.image
        else:
            return self.get_image()


class PlayerPickups(UIGroup):
    def __init__(self, *, position):
        super().__init__("pickups",
                         position=position,
                         size=(30, 60),
                         alpha=True,
                         static=True)
        self.add(Text("coins", position=(0, 0), text="0", type=SMALL))
        self.add(Text("bombs", position=(0, 20), text="1", type=SMALL))
        self.add(Text("keys", position=(0, 40), text="0", type=SMALL))

    def set_stats(self, pickups):
        for name, value in pickups.items():
            self.elements[name].text = str(value)

        self.update()


class DebugUI(UIElement):
    def __init__(self, name, *, position):
        super().__init__("debug_" + name, position=position)

    def on_mount(self):
        self.enabled = self.game.debug


class StaticDebugUI(UIElement):
    def __init__(self, name, *, position, image):
        super().__init__(name, position=position)
        self.image = image


class DebugLine(StaticDebugUI):
    frm = TriggerGetImage("_frm")
    to = TriggerGetImage("_to")
    color = TriggerGetImage("_color")

    def __init__(self, name, frm, to, *, color):
        self._frm = Vector(*frm)
        self._to = Vector(*to)
        self._color = color
        super().__init__(name, position=None, image=self.get_image())

    def get_image(self):
        width = abs(self.to.x - self.frm.x)
        height = abs(self.to.y - self.frm.y)

        result = pg.Surface((width, height))
        result.fill(DEFAULT_ALPHA)
        result.set_colorkey(DEFAULT_ALPHA)

        x0, x1 = 0, width
        if self.frm.x > self.to.x:
            x0, x1 = x1, x0
        y0, y1 = 0, height
        if self.frm.y > self.to.y:
            y0, y1 = y1, y0

        pg.draw.line(result, self.color, (x0, y0), (x1, y1))
        self.position = self.frm - (x0, y0)
