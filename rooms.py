from random import random, randint, choice
import numpy as np
import matplotlib.pyplot as plt
from game_object import GameObject
from physics import RigidBody, RectCollider, Vector
from debug_sprites import colors, RectangleSprite
from globals import TILE_SIZE, types
import layers
import os
import json

room_size = room_width, room_height = (20, 15)

DOWN = 0
UP = 1
RIGHT = 2
LEFT = 3

mirror = {
    DOWN: UP,
    RIGHT: LEFT,
    UP: DOWN,
    LEFT: RIGHT
}

templates = []

for file_name in os.listdir("templates"):
    print(f"Loading templates from {file_name}")
    with open(os.path.join("templates", file_name), 'r') as file:
        templates.extend(json.load(file))


class Door(GameObject):
    positions = [
        (room_width * TILE_SIZE / 2, room_height * TILE_SIZE),
        (room_width * TILE_SIZE / 2, 0),
        (room_width * TILE_SIZE, room_height * TILE_SIZE / 2),
        (0, room_height * TILE_SIZE / 2)
    ]
    size = (2 * TILE_SIZE, TILE_SIZE / 4)

    def __init__(self, direction):
        position = Door.positions[direction]
        size = Door.size if direction in (DOWN, UP) else Door.size[::-1]

        self.body = RigidBody(collider=RectCollider,
                              position=position,
                              size=size,
                              mass=0)

        self.sprite = RectangleSprite(colors.BLACK, size)

        self.layer = layers.OBSTACLES

        self.direction = direction

        self.enabled = True

        self.on_collide += enter_door


def enter_door(self, player):
    if player.layer == layers.PLAYER and self.enabled:
        self.body.disable_collide = True
        self.game.load_room(direction=self.direction)


class Room:
    def __init__(self, position):
        self.position = position
        self.objects = []

    def populate(self, neighbors):
        template = choice(templates)
        if not all(available or not actual
                   for available, actual
                   in zip(template["neighbors"], neighbors)):
            return False

        for obj in template["objects"]:
            self.objects.append(types[obj["type"]](position=Vector(*obj["position"]) * TILE_SIZE,
                                                   **obj["params"]))

        for direction in MapGenerator.directions:
            if neighbors[direction]:
                self.objects.append(Door(direction))

        return True

    def __repr__(self):
        return f"Room({str(self.position)})"


class DeadendRoom(Room):
    def __init__(self, position):
        super().__init__(position)


class MapGenerator:
    neighbor_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    directions = [DOWN, UP, RIGHT, LEFT]

    def __init__(self, **kwargs):
        self.rooms = [Room((0, 0))]
        self.positions = {(0, 0): 0}
        self.deadend_sorted_lengths = []

    def get_surrounding(self, position):
        return [self.positions.get((position[0] + offset[0],
                                    position[1] + offset[1]), None) is not None
                for offset in MapGenerator.neighbor_offsets]

    def generate_neighbor(self, index):
        room = self.rooms[index]
        neighbors = self.get_surrounding(room.position)
        if room.position == (0, 0):
            direction = choice(MapGenerator.directions)
        else:
            if random() > .4:
                direction = choice(MapGenerator.directions)
            else:
                direction = choice([mirror[i]
                                   for i, neighbor in enumerate(neighbors)
                                   if neighbor])
        if neighbors[direction]:
            return None
        return Room((room.position[0] + MapGenerator.neighbor_offsets[direction][0],
                     room.position[1] + MapGenerator.neighbor_offsets[direction][1]))

    def new_room(self):
        n = random()
        if n > .4:
            new_room = self.generate_neighbor(-1)
        elif n > .2 and len(self.rooms) > 1:
            new_room = self.generate_neighbor(-2)
        elif len(self.rooms) > 2:
            new_room = self.generate_neighbor(randint(0, len(self.rooms) - 3))
        else:
            new_room = None
        if new_room is None:
            return None
        self.positions[new_room.position] = len(self.rooms)
        return new_room

    def add_rooms(self, amount):
        while len(self.rooms) < amount:
            new_room = self.new_room()
            while new_room is None:
                new_room = self.new_room()
            self.positions[new_room.position] = len(self.rooms)
            self.rooms.append(new_room)

    def new_deadend(self):
        index = randint(0, len(self.rooms) - 1)
        if type(self.rooms[index]) is not Room:
            return None
        possible_directions = [i for i, neighbor in
                               enumerate(self.get_surrounding(self.rooms[index].position))
                               if not neighbor]
        if len(possible_directions) == 0:
            return None
        direction = choice(possible_directions)
        pos = (self.rooms[index].position[0] + MapGenerator.neighbor_offsets[direction][0],
               self.rooms[index].position[1] + MapGenerator.neighbor_offsets[direction][1])
        neighbor_rooms_total = sum(self.get_surrounding(pos))
        if neighbor_rooms_total != 1:
            return None
        else:
            return DeadendRoom(pos)

    def add_deadends(self, amount):
        start_len = len(self.rooms)
        while len(self.rooms) - amount < start_len:
            new_room = self.new_deadend()
            while new_room is None:
                new_room = self.new_deadend()
            self.positions[new_room.position] = len(self.rooms)
            self.rooms.append(new_room)

    def populate_rooms(self):
        for room in self.rooms:
            populated = False
            while not populated:
                populated = room.populate(self.get_surrounding(room.position))

    def generate_map(self, amount, deadends):
        self.add_rooms(amount - deadends)
        self.add_deadends(deadends)
        self.populate_rooms()


if __name__ == "__main__":
    mg = MapGenerator()
    mg.generate_map(20, 5)

    img = np.full((25, 25, 3), 0)

    for r in mg.rooms:
        index = (r.position[1] + 13, r.position[0] + 13)
        if type(r) is Room:
            img[index] = (255, 255, 255)
        if type(r) is DeadendRoom:
            img[index] = (255, 255, 0)

    plt.imshow(img)
    plt.show()
