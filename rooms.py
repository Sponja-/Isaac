from random import random, randint, choice
import matplotlib.pyplot as plt
import numpy as np

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


class Room:
    def __init__(self, position):
        self.position = position
        self.neighbors = [None, None, None, None]
        self.available = [True, True, True, True]


class MapGenerator:
    neighbor_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    directions = [DOWN, UP, RIGHT, LEFT]

    def __init__(self, **kwargs):
        self.rooms = [Room((0, 0))]
        self.positions = {(0, 0): 0}

    def generate_neighbor(self, index):
        room = self.rooms[index]
        if room.position == (0, 0):
            direction = choice(MapGenerator.directions)
        else:
            if random() > .4:
                direction = choice(MapGenerator.directions)
            else:
                direction = choice([mirror[i]
                                   for i, neighbor in enumerate(room.neighbors)
                                   if neighbor is not None])
        if room.neighbors[direction] is not None:
            return None
        return Room((room.position[0] + MapGenerator.neighbor_offsets[direction][0],
                     room.position[1] + MapGenerator.neighbor_offsets[direction][1]))

    def next_room(self):
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
            return self.next_room()
        pos = new_room.position
        for direction, offset in enumerate(MapGenerator.neighbor_offsets):
            index = self.positions.get((pos[0] + offset[0], pos[1] + offset[1]), None)
            if index is None:
                continue
            other = self.rooms[index]
            if not other.available[mirror[direction]]:
                return self.next_room()
            new_room.neighbors[direction] = other
            other.neighbors[mirror[direction]] = new_room
        self.positions[pos] = len(self.rooms) - 1
        return new_room

    def generate(self, amount):
        while len(self.rooms) < amount:
            self.rooms.append(self.next_room())
        return self.rooms
