import numpy as np
from room import Room
from functions import Celsius_to_Kelvin, surroundings

f = lambda P,d,c,S: P/(d*S*c)

class Radiator:
    def __init__(self, room, location, power, h, level=0):
        self.min_temperatures = [Celsius_to_Kelvin(i) for i in [4, 12, 16, 20, 23, 26]]
        self.max_temperatures = [Celsius_to_Kelvin(i) for i in [5, 14, 18, 21, 24, 28]]
        self.level = level
        self.room = room
        self.location = location

        neighbors = []
        for part in location:
            neighbors =  [*neighbors, *surroundings(room.m, room.n, part)]
        self.surroundings = list(set([part for part in neighbors if part not in location]))

        self.size = len(location) * h**2
        self.power = power*len(location)
        self.work_time = 0
        self.On = True

    def heating(self, time_delta):
        if (self.room.local_mean_temperature(self.surroundings) < self.max_temperatures[self.level]) and (self.On == True):
            for part in self.location:
                self.room.heat_area[part] = (self.room.heat_area[part] + 
                                             time_delta * f(self.power, self.room.density, self.room.specific_heat, self.size))
            self.work_time = self.work_time + time_delta
        if self.room.local_mean_temperature(self.surroundings) >= self.max_temperatures[self.level]:
            self.On = False
        if self.room.local_mean_temperature(self.surroundings) < self.min_temperatures[self.level]:
            self.On = True
    
    def used_energy(self):
        return(self.work_time * (f(self.power, self.room.density, self.room.specific_heat, self.size) * self.size))


    