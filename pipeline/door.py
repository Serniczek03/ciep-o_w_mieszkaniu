import numpy as np
from room import Room

class Door:
    def __init__(self, room_1, room_2, location_1, location_2):
        self.room_1 = room_1
        self.room_2 = room_2
        self.location_1 = location_1
        self.location_2 = location_2
    
    def average_temperature(self):
        mean_door_temperature = 0
        for part in self.location_1:
            mean_door_temperature = mean_door_temperature + self.room_1.heat_area[part]
        for part in self.location_2:
            mean_door_temperature = mean_door_temperature + self.room_2.heat_area[part]
        
        mean_door_temperature = mean_door_temperature / (len(self.location_1)+len(self.location_2))

        for part in self.location_1:
            self.room_1.heat_area[part] = mean_door_temperature
        for part in self.location_2:
            self.room_2.heat_area[part] = mean_door_temperature
        
        

