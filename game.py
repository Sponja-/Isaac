import pygame as pg
from sys import exit
from player import Player
from debug_sprites import colors
from game_object import Event
import obstacles
import pickups
import enemy
import rooms
import globals
import layers
import physics
from random import seed
from argparse import ArgumentParser

pg.init()


class Game:
    def __init__(self, size):
        self.size = self.width, self.height = size
        self.screen = pg.display.set_mode(size)

        self.clock = pg.time.Clock()

        self.objects = []
        self.sprites = pg.sprite.Group()

        self.timers = []

        self.floor_generator = rooms.MapGenerator()
        self.floor_generator.generate_map(20, 4)

        self.player = Player(position=(self.width / 2, self.height / 2))
        self.current_room = None
        self.enemy_count = 0

        self.on_room_complete = Event("room_complete")
        self.on_room_complete += complete_room

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

            for i, (time, function, args) in enumerate(self.timers):
                if time <= current_time:
                    result = function(*args)
                    if not result:
                        self.timers.pop(i)

            self.screen.fill(colors.WHITE)

            self.sprites.update(delta_time)
            self.sprites.draw(self.screen)

            pg.display.flip()

            self.clock.tick(60)

    def load_room(self, *, position=None, direction=None):
        if position is None:
            offset = rooms.MapGenerator.neighbor_offsets[direction]
            position = (self.current_room.position[0] + offset[0],
                        self.current_room.position[1] + offset[1])
        index = self.floor_generator.positions[position]

        if self.current_room is not None:
            self.exit_room()

        self.current_room = self.floor_generator.rooms[index]
        print(self.current_room.type)

        self.player.body.collider.move_to((self.width / 2, self.height / 2))

        self.add(self.player)

        for obj in self.current_room.objects:
            self.add(obj)

        if self.enemy_count > 0:
            self.close_doors()
            self.room_completed = False
        else:
            self.room_completed = True

    def exit_room(self):

        if self.room_completed:
            self.current_room.objects = [obj for obj in self.objects
                                         if type(obj) is not Player and
                                         obj.layer != layers.PLAYER_TEARS and
                                         obj.layer != layers.ENEMY_TEARS]

        self.sprites.empty()
        self.objects.clear()
        self.enemy_count = 0

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

        if obj.layer == layers.ENEMIES:
            self.enemy_count += 1

    def get_time(self):
        return pg.time.get_ticks() / 1000

    def add_timer(self, time, function, args=()):
        self.timers.append((self.get_time() + time, function, args))

    def find_object(self, tag):
        for obj in self.objects:
            if tag in obj.tags:
                return obj

    def find_objects(self, tag):
        return [obj for obj in self.objects if tag in obj.tags]

    def enemy_died(self):
        self.enemy_count -= 1
        if self.enemy_count <= 0:
            self.on_room_complete.dispatch(self)

    def close_doors(self):
        for obj in self.objects:
            if type(obj) is rooms.Door:
                obj.enabled = False

    def open_doors(self):
        for obj in self.objects:
            if type(obj) is rooms.Door:
                obj.enabled = True


def complete_room(self):
    self.open_doors()
    self.room_completed = True


if __name__ == "__main__":
    parser = ArgumentParser(description="Binding of Isaac clone")
    parser.add_argument('-s', type=int, help="Game seed")

    args = parser.parse_args()

    if args.s is not None:
        seed(args.s)

    game = Game((globals.TILE_SIZE * rooms.room_width,
                 globals.TILE_SIZE * rooms.room_height))

    game.run()
