import pygame as pg
from sys import exit
from player import Player
from debug_sprites import colors
from pickups import Coin
from rocks import Rock, CircleRock
import layers
import physics

pg.init()


class Game:
    def __init__(self, size):
        self.size = self.width, self.height = size
        self.screen = pg.display.set_mode(size)

        self.clock = pg.time.Clock()

        self.objects = []
        self.sprites = pg.sprite.Group()

        self.waits = []

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

            self.compute_collisions(delta_time)

            current_time = self.get_time()

            for i, (time, function, args) in enumerate(self.waits):
                if time <= current_time:
                    function(*args)
                    self.waits.pop(i)

            self.screen.fill(colors.WHITE)

            self.sprites.update(delta_time)
            self.sprites.draw(self.screen)

            pg.display.flip()

            self.clock.tick(60)

    def compute_collisions(self, delta_time):
        for i, obj in enumerate(self.objects):
            for other in self.objects[i + 1:]:
                if layers.collisions[obj.layer][other.layer]:
                    if obj.body.collider.is_colliding(other.body.collider):
                        obj.collide(other)
                        other.collide(obj)
                        physics.resolveCollision(obj.body, other.body, delta_time)

    def add(self, obj):
        obj.game = self

        obj.on_mount.dispatch(obj)

        self.objects.append(obj)
        if obj.sprite is not None:
            self.sprites.add(obj.sprite)

    def get_time(self):
        return pg.time.get_ticks() / 1000

    def add_wait(self, time, function, args=()):
        self.waits.append((self.get_time() + time, function, args))


game = Game((800, 600))

game.add(Coin(position=(200, 200)))
game.add(Rock(position=(100, 30)))
game.add(CircleRock(position=(500, 500)))

game.run()
