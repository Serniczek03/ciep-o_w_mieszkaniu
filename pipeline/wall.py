import numpy as np
from room import Room

class Wall:
    def __init__(self, room):
        self.room = room
        m = room.m
        n = room.n

        self.upper_part = [(0, i) for i in range(0, n)]
        self.lower_part = [(m-1, i) for i in range(0, n)]
        self.left_part = [(i, 0) for i in range(1, m-1)]
        self.right_part = [(i, n-1) for i in range(1, m-1)]

        self.n_upper_part = [(1, i) for i in range(0, n)]
        self.n_lower_part = [(m-2, i) for i in range(0, n)]
        self.n_left_part = [(i, 1) for i in range(1, m-1)]
        self.n_right_part = [(i, n-2) for i in range(1, m-1)]

    def isolate_temperature(self):
        for i in range(len(self.left_part)):
            self.room.heat_area[self.left_part[i]] = self.room.heat_area[self.n_left_part[i]]
        for i in range(len(self.right_part)):
            self.room.heat_area[self.right_part[i]] = self.room.heat_area[self.n_right_part[i]]
        for i in range(len(self.upper_part)):
            self.room.heat_area[self.upper_part[i]] = self.room.heat_area[self.n_upper_part[i]]
        for i in range(len(self.lower_part)):
            self.room.heat_area[self.lower_part[i]] = self.room.heat_area[self.n_lower_part[i]]

