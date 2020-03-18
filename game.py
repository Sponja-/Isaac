import pygame as pg
from sys import exit
from player import Player
from debug_sprites import colors
import layers

pg.init()


class Game:
    def __init__(self, size):
        self.size = self.width, self.height = size
        self.screen = pg.display.set_mode(size)

        self.clock = pg.time.Clock()

        self.objects = []
        self.sprites = pg.sprite.Group()

        self.player = Player()
        self.add(self.player)

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            delta_time = self.clock.get_time() / 1000

            for i, obj in enumerate(self.objects):
                obj.physics_update(delta_time)
                obj.update(delta_time)

                if obj.to_kill:
                    self.objects.pop(i)
                    if obj.sprite is not None:
                        self.sprites.remove(obj.sprite)

            self.screen.fill(colors.WHITE)

            self.sprites.update(delta_time)
            self.sprites.draw(self.screen)

            pg.display.flip()

            self.clock.tick(60)

    def compute_collisions(self):
        for i, obj in enumerate(self.objects):
            for other in self.objects[i + 1:]:
                if layers.collisions[obj][other]:
                    if obj.body.collider.is_colliding(other):
                        obj.collide(other)
                        other.collide(obj)

    def add(self, obj):
        obj.game = self

        obj.on_mount.dispatch(obj)

        self.objects.append(obj)
        if obj.sprite is not None:
            self.sprites.add(obj.sprite)


game = Game((800, 600))

game.run()
