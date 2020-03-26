import pygame as pg
from sys import exit
from player import Player
from debug_sprites import colors
import rocks
import pickups
from rooms import MapGenerator, room_width, room_height
import globals
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

        self.floor_generator = MapGenerator()
        self.floor_generator.generate_map(20, 4)

        self.load_room(position=(0, 0))

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

    def load_room(self, *, position=None, direction=None):
        if position is None:
            offset = MapGenerator.neighbor_offsets[direction]
            position = (self.current_room.position[0] + offset[0],
                        self.current_room.position[1] + offset[1])
        index = self.floor_generator.positions[position]

        self.current_room = self.floor_generator.rooms[index]

        self.sprites.empty()
        self.objects.clear()

        for obj in self.current_room.objects:
            self.add(obj)

        self.add(Player(position=(self.width / 2, self.height / 2)))

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


game = Game((globals.TILE_SIZE * room_width, globals.TILE_SIZE * room_height))

game.run()
