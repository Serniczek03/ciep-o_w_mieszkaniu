import numpy as np
from house import House
import matplotlib.pyplot as plt
from functions import Celsius_to_Kelvin, Kelvin_to_Celsius, converting_hours_into_iteration_steps, converting_iteration_steps_into_hours, give_second_column_when_first_is_equal

class Experiment:
    def __init__(self, initial_temperature, density, specific_heat, outside_temperature, 
                 radiator_location_1, 
                 radiator_location_2, 
                 radiator_location_3, 
                 radiator_location_4, 
                 radiators_power, alpha, reduse_heating,
                 time_delta, h):
        
        self.initial_temperature = initial_temperature
        self.density = density
        self.specific_heat = specific_heat
        self.outside_temperature = outside_temperature
        self.radiator_location_1 = radiator_location_1
        self.radiator_location_2 = radiator_location_2
        self.radiator_location_3 = radiator_location_3
        self.radiator_location_4 = radiator_location_4
        self.radiators_power = radiators_power
        self.alpha = alpha
        self.reduse_heating = reduse_heating
        self.time_delta = time_delta
        self.h = h
        
        self.apartment = House(initial_temperature, density, specific_heat, outside_temperature[0], 
                               radiator_location_1, 
                               radiator_location_2, 
                               radiator_location_3, 
                               radiator_location_4, 
                               radiators_power, h)
        
    def twelve_heat_maps_over_time(self, t_start, t_end, heat_maps_titles, file_title):

        print('-----------------------------')

        time = 0
        for _ in range(t_start):
            for window in self.apartment.windows:
                window.outside_temperature = self.outside_temperature[time]            
            self.apartment.update_house_temperature( self.alpha, self.time_delta)

            if time in self.reduse_heating[: , 0]:
                new_level = give_second_column_when_first_is_equal(self.reduse_heating, time)
                for radiator in self.apartment.radiators:
                    radiator.level = new_level

            time = time+1
        
        num_images = 12
        
        time_interval_between_images = int((t_end - t_start)/num_images)
        
        fig, axes = plt.subplots(4, 3, figsize=(10, 10))
        
        axes = axes.flatten()

        for i in range(num_images):
            for _ in range(time_interval_between_images):
                for window in self.apartment.windows:
                    window.outside_temperature = self.outside_temperature[time]
                self.apartment.update_house_temperature(self.alpha, self.time_delta)

                if time in self.reduse_heating[:, 0]:
                    new_level = give_second_column_when_first_is_equal(self.reduse_heating, time)
                    for radiator in self.apartment.radiators:
                        radiator.level = new_level

                time = time+1

            house_heat_area = Kelvin_to_Celsius(self.apartment.get_house())
            
            ax = axes[i]
            heatmap = ax.imshow(house_heat_area, cmap='rainbow', interpolation='nearest')
            
            cbar = fig.colorbar(heatmap, ax=ax)
            cbar.set_label('Temperatura (C)')

            heatmap.set_clim(vmin=Kelvin_to_Celsius(min(self.outside_temperature)), vmax=30)
            
            ax.set_title(heat_maps_titles[i])
            
            # Wyłączenie liczb na osiach
            ax.set_xticks([])  
            ax.set_yticks([])

            print(f"Obrazek {i+1} ukończony!")
        
        # Zapisanie obrazu
        plt.tight_layout()
        plt.savefig(file_title)
        #plt.show()
        plt.close()

        self.apartment = House(self.initial_temperature, self.density, self.specific_heat, self.outside_temperature[0], 
                               self.radiator_location_1, 
                               self.radiator_location_2, 
                               self.radiator_location_3, 
                               self.radiator_location_4, 
                               self.radiators_power, self.h)

        print("Plik został stworzony!!!")
        print('-----------------------------')

    def used_energy_plot(self, t_start, t_end, plot_title, file_title):

        print('-----------------------------')
        time = 0
        for _ in range(t_start):
            for window in self.apartment.windows:
                window.outside_temperature = self.outside_temperature[time]            
            self.apartment.update_house_temperature(self.alpha, self.time_delta)

            if time in self.reduse_heating[:, 0]:
                new_level = give_second_column_when_first_is_equal(self.reduse_heating, time)
                for radiator in self.apartment.radiators:
                    radiator.level = new_level

            time = time+1
            if (time+1)%converting_hours_into_iteration_steps(1, self.time_delta) == 0:
                print(f"Minęła {int((time+1)/converting_hours_into_iteration_steps(1, self.time_delta))} godzina!")

        used_energy_by_radiators = []
        period_time = np.arange(t_start, t_end)

        for _ in period_time:
            for window in self.apartment.windows:
                window.outside_temperature = self.outside_temperature[time]
            self.apartment.update_house_temperature(self.alpha, self.time_delta)

            if time in self.reduse_heating[:, 0]:
                new_level = give_second_column_when_first_is_equal(self.reduse_heating, time)
                for radiator in self.apartment.radiators:
                    radiator.level = new_level

            used_energy_by_radiators.append(self.apartment.used_energy())
            time = time+1

            if (time+1)%converting_hours_into_iteration_steps(1, self.time_delta) == 0:
                print(f"Minęła {int((time+1)/converting_hours_into_iteration_steps(1, self.time_delta))} godzina!")

        period_time = [converting_iteration_steps_into_hours(i, self.time_delta) for i in period_time]

        plt.plot(period_time, used_energy_by_radiators)
        plt.title(plot_title)
        plt.xlabel("Czas[h]")
        plt.ylabel("Energia[J]")

        plt.savefig(file_title)
        #plt.show()
        plt.close()

        self.apartment = House(self.initial_temperature, self.density, self.specific_heat, self.outside_temperature[0], 
                               self.radiator_location_1, 
                               self.radiator_location_2, 
                               self.radiator_location_3, 
                               self.radiator_location_4, 
                               self.radiators_power, self.h)

        print("Plik został stworzony!!!")
        print('-----------------------------')

    def mean_rooms_temperatures_plot(self, t_start, t_end, file_title):

        print('-----------------------------')
        time = 0
        for _ in range(t_start):
            for window in self.apartment.windows:
                window.outside_temperature = self.outside_temperature[time]            
            self.apartment.update_house_temperature(self.alpha, self.time_delta)

            if time in self.reduse_heating[:, 0]:
                new_level = give_second_column_when_first_is_equal(self.reduse_heating, time)
                for radiator in self.apartment.radiators:
                    radiator.level = new_level

            time = time+1
            if (time+1)%converting_hours_into_iteration_steps(1, self.time_delta) == 0:
                print(f"Minęła {int((time+1)/converting_hours_into_iteration_steps(1, self.time_delta))} godzina!")

        num_images = 12

        fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True, sharey=True)
        axes = axes.flatten()

        mean_room_1_temperatures = []
        mean_room_2_temperatures = []
        mean_room_3_temperatures = []
        mean_room_4_temperatures = []
        mean_room_5_temperatures = []
        mean_hause_temperatures = []
        period_time = np.arange(t_start, t_end)

        for _ in period_time:
            for window in self.apartment.windows:
                window.outside_temperature = self.outside_temperature[time]
            self.apartment.update_house_temperature(self.alpha, self.time_delta)

            if time in self.reduse_heating[:, 0]:
                new_level = give_second_column_when_first_is_equal(self.reduse_heating, time)
                for radiator in self.apartment.radiators:
                    radiator.level = new_level

            mean_room_1_temperatures.append(self.apartment.rooms[0].mean_temperature())
            mean_room_2_temperatures.append(self.apartment.rooms[1].mean_temperature())
            mean_room_3_temperatures.append(self.apartment.rooms[2].mean_temperature())
            mean_room_4_temperatures.append(self.apartment.rooms[3].mean_temperature())
            mean_room_5_temperatures.append(self.apartment.rooms[4].mean_temperature())
            mean_hause_temperatures.append((self.apartment.rooms[0].mean_temperature() + 
                                                self.apartment.rooms[1].mean_temperature() + 
                                                self.apartment.rooms[2].mean_temperature() + 
                                                self.apartment.rooms[3].mean_temperature() + 
                                                self.apartment.rooms[4].mean_temperature())/5)
            time = time+1

            if (time+1)%converting_hours_into_iteration_steps(1, self.time_delta) == 0:
                print(f"Minęła {int((time+1)/converting_hours_into_iteration_steps(1, self.time_delta))} godzina!")

        period_time = [converting_iteration_steps_into_hours(i, self.time_delta) for i in period_time]

        data = [Kelvin_to_Celsius(mean_room_1_temperatures),
                Kelvin_to_Celsius(mean_room_2_temperatures),
                Kelvin_to_Celsius(mean_room_3_temperatures),
                Kelvin_to_Celsius(mean_room_4_temperatures),
                Kelvin_to_Celsius(mean_room_5_temperatures),
                Kelvin_to_Celsius(mean_hause_temperatures)]

        for ax, y, title in zip(axes, data, ['Średnie temperatur w I pokoju', 
                                             'Średnie temperatur w II pokoju', 
                                             'Średnie temperatur w III pokoju', 
                                             'Średnie temperatur w IV pokoju', 
                                             'Średnie temperatur w V pokoju', 
                                             'Średnie temperatur w całym mieszkaniu']):
            ax.plot(period_time, y, label=title)
            ax.set_title(title)
            ax.set_xlim(min(period_time), max(period_time))
            ax.set_ylim(Kelvin_to_Celsius(min(self.outside_temperature)), 30)
            ax.set_xlabel('Czas[h]')
            ax.set_ylabel('Temperatura [C]')
            ax.grid(True)                      
        
        # Zapisanie obrazu
        plt.tight_layout()
        plt.savefig(file_title)
        #plt.show()
        plt.close()

        self.apartment = House(self.initial_temperature, self.density, self.specific_heat, self.outside_temperature[0], 
                               self.radiator_location_1, 
                               self.radiator_location_2, 
                               self.radiator_location_3, 
                               self.radiator_location_4, 
                               self.radiators_power, self.h)

        print("Plik został stworzony!!!")
        print('-----------------------------')



        
        


