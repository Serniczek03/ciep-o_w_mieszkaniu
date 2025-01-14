import numpy as np
from radiator import Radiator
from door import Door
from window import Window
from wall import Wall
from room import Room

class House:
    def __init__(self, initial_temperature, density, specific_heat, outside_temperature, 
                 radiator_location_1, radiator_location_2, radiator_location_3, radiator_location_4, 
                 radiators_power, h):
        self.h = h
        
        Room_1 = Room((19,17), initial_temperature, density, specific_heat)
        Room_2 = Room((13,10), initial_temperature, density, specific_heat)
        Room_3 = Room((11,13), initial_temperature, density, specific_heat)
        Room_4 = Room((11,5), initial_temperature, density, specific_heat)
        Room_5 = Room((6,10), initial_temperature, density, specific_heat)
        self.rooms = [Room_1, Room_2, Room_3, Room_4, Room_5]

        Wall_1 = Wall(Room_1)
        Wall_2 = Wall(Room_2)
        Wall_3 = Wall(Room_3)
        Wall_4 = Wall(Room_4)
        Wall_5 = Wall(Room_5)
        self.walls = [Wall_1, Wall_2, Wall_3, Wall_4, Wall_5]

        Window_1 = Window(Room_1, [(0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,9), (0,10), (0,11), (0,12), (0,13)], outside_temperature)
        Window_2 = Window(Room_2, [(0,3), (0,4), (0,5), (0,6), (0,7)], outside_temperature)
        Window_3 = Window(Room_3, [(10,3), (10,4), (10,5), (10,6), (10,7), (10,8), (10,9)], outside_temperature)
        Window_4 = Window(Room_4, [(10,1), (10,2), (10,3)], outside_temperature)
        self.windows = [Window_1, Window_2, Window_3, Window_4]

        Door_1 = Door(Room_2, Room_5, [(12,2), (12,3)], [(0,2), (0,3)])
        Door_2 = Door(Room_1, Room_5, [(15,16), (16,16)], [(2,0), (3,0)])
        Door_3 = Door(Room_3, Room_5, [(0,10), (0,11)], [(5,2), (5,3)])
        Door_4 = Door(Room_4, Room_5, [(0,2), (0,3)], [(5,7), (5,8)])
        self.doors = [Door_1, Door_2, Door_3, Door_4]

        Radiator_1 = Radiator(Room_1, radiator_location_1, radiators_power, h)
        Radiator_2 = Radiator(Room_2, radiator_location_2, radiators_power, h)
        Radiator_3 = Radiator(Room_3, radiator_location_3, radiators_power, h)
        Radiator_4 = Radiator(Room_4, radiator_location_4, radiators_power, h)
        self.radiators = [Radiator_1, Radiator_2, Radiator_3, Radiator_4]

        for wall in [Wall_1, Wall_2, Wall_3, Wall_4, Wall_5]:
            wall.isolate_temperature()

        for window in [Window_1, Window_2, Window_3, Window_4]:
            window.release_heat()
        
        for door in [Door_1, Door_2, Door_3, Door_4]:
            door.average_temperature()

    def update_house_temperature(self, alpha, time_delta):
        for radiator in self.radiators:
            radiator.heating(time_delta)

        for room in self.rooms:
            room.update_temperature(alpha, time_delta, self.h)
        
        for wall in self.walls:
            wall.isolate_temperature()

        for window in self.windows:
            window.release_heat()
        
        for door in self.doors:
            door.average_temperature()
    
    def used_energy(self):
        sum_used_energy = 0
        for radiator in self.radiators:
            sum_used_energy = sum_used_energy + radiator.used_energy()
        return(sum_used_energy)
    
    def get_house(self):
        house_heat_area = np.full((self.rooms[0].m + self.rooms[2].m, self.rooms[0].n + self.rooms[1].n), None, dtype=object)
        
        house_heat_area[:self.rooms[0].m, :self.rooms[0].n] = self.rooms[0].heat_area

        house_heat_area[:self.rooms[1].m, self.rooms[0].n:] = self.rooms[1].heat_area

        house_heat_area[self.rooms[1].m:(self.rooms[1].m + self.rooms[4].m), self.rooms[0].n:] = self.rooms[4].heat_area

        house_heat_area[self.rooms[0].m:, 
        (self.rooms[0].n + self.rooms[1].n - self.rooms[2].n - self.rooms[3].n):(self.rooms[0].n + self.rooms[1].n - self.rooms[3].n)] = self.rooms[2].heat_area

        house_heat_area[self.rooms[0].m:, (self.rooms[0].n + self.rooms[1].n - self.rooms[3].n):] = self.rooms[3].heat_area

        house_heat_area = np.array([[float(x) if x is not None else np.nan for x in row] for row in house_heat_area])

        return(house_heat_area)