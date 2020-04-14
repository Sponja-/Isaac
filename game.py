import pygame as pg
from sys import exit
from player import Player
from debug_sprites import colors
from physics import Vector, resolveCollision
from game_object import Event
import rooms
import globals
import layers
import ui
import assets
from random import seed, choice
from argparse import ArgumentParser

pg.init()


class Game:
    def __init__(self, size):
        self.size = self.width, self.height = size
        self.screen = pg.display.set_mode(size)

        self.clock = pg.time.Clock()

        self.objects = []
        self.ui_objects = {}
        self.sprites = pg.sprite.Group()

        self.timers = {}
        self.timer_index = 0

        self.floor_generator = rooms.MapGenerator()
        self.floor_generator.generate_map(20, 4)

        self.player = Player(position=(self.width / 2, self.height / 2))
        self.current_room = None
        self.enemy_count = 0

        self.on_room_complete = Event("room_complete")
        self.on_room_complete += complete_room

        self.load_room(position=(0, 0))

        self.add_ui(ui.PlayerPickups(position=(10, 40)))

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_f:
                        self.player.body.collider.move_to((self.width / 2, self.height / 2))

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
            to_remove = []

            for id, (time, function, args) in self.timers.items():
                if time <= current_time:
                    result = function(*args)
                    if not result:
                        to_remove.append(id)

            for id in to_remove:
                self.remove_timer(id)

            self.screen.fill(colors.WHITE)

            self.sprites.update(delta_time)
            self.sprites.draw(self.screen)

            for name, element in self.ui_objects.items():
                self.screen.blit(element.get_render(), element.position)

            pg.display.flip()

            self.clock.tick(60)

    def load_room(self, *, position=None, direction=None):
        player_pos = None

        if self.current_room is not None:
            self.exit_room()

        if position is None:
            self.current_room = self.floor_generator.get_neighbor(self.current_room, direction)
            player_pos = rooms.player_room_positions[rooms.mirror[direction]]

        if direction is None:
            first_room = self.current_room is None
            self.current_room = self.floor_generator.get_from_pos(position)
            if not first_room:
                player_pos = rooms.player_room_positions[choice(self.current_room.door_directions)]
            else:
                player_pos = Vector(self.width / 2, self.height / 2)

        self.player.body.collider.move_to(player_pos)

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
                        resolveCollision(obj.body, other.body, delta_time)

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
        self.timers[self.timer_index] = (self.get_time() + time, function, args)
        self.timer_index += 1
        return self.timer_index - 1

    def remove_timer(self, id):
        del self.timers[id]

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

    def add_ui(self, element):
        self.ui_objects[element.name] = element
        element.game = self
        element.on_mount()


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
