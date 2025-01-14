import numpy as np
from room import Room

class Window:
    def __init__(self, room, location, outside_temperature):
        self.room = room
        self.location = location
        self.outside_temperature = outside_temperature
    
    def release_heat(self):
        for part in self.location:
            self.room.heat_area[part] = self.outside_temperature