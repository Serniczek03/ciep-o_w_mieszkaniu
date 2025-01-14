import numpy as np
from experiment import Experiment
from functions import sketch_of_the_apartment, Celsius_to_Kelvin, converting_hours_into_iteration_steps, converting_iteration_steps_into_hours, outside_temperature_in_time_iteration
import csv

print('--------------------------------------------------------------------------------------------------------------------------------')

sketch_of_the_apartment(list(set([(1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9), (1,10), (1,11), (1,12),
                                 (1,20), (1,21), (1,22), (1,23),
                                 (28,12), (28,13), (28,14), (28,15), (28,16), (28,17), (28,18),
                                 (28,23), (28,24)])), 'Schemat mieszkania z kaloryferami obok okien.png')

sketch_of_the_apartment(list(set([(17,1), (17,2), (17,3), (17,4), (17,5), (17,6), (17,7), (17,8), (17,9), (17,10),
                                 (8,25), (9,25), (10,25), (11,25),
                                 (20,10), (20,11), (20,12), (20,13), (20,14), (20,15), (20,16),
                                 (20,23), (21,23)])), 'Schemat mieszkania z kaloryferami daleko od okien.png')

print("Schematy mieszkania stworzone!")

file_path_1 = "C:/Users/Lenovo/Documents/GitHub/ciep-o_w_mieszkaniu/data/Physical constants.csv"
file_path_2 = "C:/Users/Lenovo/Documents/GitHub/ciep-o_w_mieszkaniu/data/Outside temperatures in Wroclaw (3 types of days).csv"

density = 0

specific_heat = 0

radiators_power = 0

alpha = 0

with open(file_path_1, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Pominięcie nagłówka
    for row in reader:
        if row[0] == "Gęstość Powietrza w Mieszkaniu":
            density = float(row[1])
        elif row[0] == "Ciepło Właściwe Powietrza w Mieszkaniu":
            specific_heat = float(row[1])
        elif row[0] == "Moc Kaloryferów w Mieszkaniu":
            radiators_power = float(row[1])
        elif row[0] == "Współczynnik Przewodnictwa Cieplnego":
            alpha = float(row[1])

outside_temperature_very_cold_day = []
outside_temperature_cold_day = []
outside_temperature_cool_day = []

with open(file_path_2, mode='r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        outside_temperature_very_cold_day.append(float(row[1]))
        outside_temperature_cold_day.append(float(row[2]))
        outside_temperature_cool_day.append(float(row[3]))

#------------------------------------------------------------------------------------------------------------------

time_delta=0.5
h=0.5

initial_temperature = Celsius_to_Kelvin(5)

outside_temperature_very_cold_day = outside_temperature_in_time_iteration(Celsius_to_Kelvin(outside_temperature_very_cold_day), time_delta)
outside_temperature_cold_day = outside_temperature_in_time_iteration(Celsius_to_Kelvin(outside_temperature_cold_day), time_delta)
outside_temperature_cool_day = outside_temperature_in_time_iteration(Celsius_to_Kelvin(outside_temperature_cool_day), time_delta)

# Problem 1
# Rozmieszczenie Kaloryferów

reduse_heating = np.matrix([[converting_hours_into_iteration_steps(6, time_delta), 3], 
                            [converting_hours_into_iteration_steps(22, time_delta), 2]])

# 1) Kaloryfery pod oknami

radiator_location_1 = [(1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9), (1,10), (1,11), (1,12)]
radiator_location_2 = [(1,3), (1,4), (1,5), (1,6)]
radiator_location_3 = [(9,3), (9,4), (9,5), (9,6), (9,7), (9,8), (9,9)] 
radiator_location_4 = [(9,1), (9,2)]

Experiment_radiators_next_to_windows = Experiment(initial_temperature, density, specific_heat, outside_temperature_cold_day, 
                                                    radiator_location_1, 
                                                    radiator_location_2, 
                                                    radiator_location_3, 
                                                    radiator_location_4, 
                                                    radiators_power, alpha, reduse_heating, 
                                                    time_delta, h)

# Mapy ciepła
Experiment_radiators_next_to_windows.twelve_heat_maps_over_time(converting_hours_into_iteration_steps(6, time_delta), 
                                                                converting_hours_into_iteration_steps(7, time_delta), 
                                                                ['6:05', '6:10', '6:15', 
                                                                '6:20', '6:25', '6:30',
                                                                '6:35', '6:40', '6:45', 
                                                                '6:50', '6:55', '7:00'], 
                                                                'Zmiana temperatury przez pierwszą godzinę grzania (kaloryfery obok okien).png')

# Wykres energii
Experiment_radiators_next_to_windows.used_energy_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                                      converting_hours_into_iteration_steps(24, time_delta), 
                                                      'Wykres wzrostu pobieranej energi przez cały dzień (od północy do północy)', 
                                                      'Wykres wzrostu energi (kaloryfery obok okien).png')

# Wykresy zmiany średnich temperatur w pokojach i mieszakniu
Experiment_radiators_next_to_windows.mean_rooms_temperatures_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                                                  converting_hours_into_iteration_steps(24, time_delta), 
                                                                  'Wykresy zmiany średnich temperatur w pokojach i mieszakniu (kaloryfery obok okien).png')

# 2) Kaloryfery daleko od okien

radiator_location_1 = [(17,1), (17,2), (17,3), (17,4), (17,5), (17,6), (17,7), (17,8), (17,9), (17,10)]
radiator_location_2 = [(8,8), (9,8), (10,8), (11,8)]
radiator_location_3 = [(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7)] 
radiator_location_4 = [(1,1), (2,1)]

Experiment_radiators_far_from_windows = Experiment(initial_temperature, density, specific_heat, outside_temperature_cold_day, 
                                                    radiator_location_1, 
                                                    radiator_location_2, 
                                                    radiator_location_3, 
                                                    radiator_location_4, 
                                                    radiators_power, alpha, reduse_heating, 
                                                    time_delta, h)

# Mapy ciepła
Experiment_radiators_far_from_windows.twelve_heat_maps_over_time(converting_hours_into_iteration_steps(6, time_delta), 
                                                                 converting_hours_into_iteration_steps(7, time_delta), 
                                                                 ['6:05', '6:10', '6:15', 
                                                                  '6:20', '6:25', '6:30',
                                                                  '6:35', '6:40', '6:45', 
                                                                  '6:50', '6:55', '7:00'], 
                                                                  'Zmiana temperatury przez pierwszą godzinę grzania (kaloryfery daleko od okien).png')

# Wykres energii
Experiment_radiators_far_from_windows.used_energy_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                                       converting_hours_into_iteration_steps(24, time_delta), 
                                                       'Wykres wzrostu pobieranej energi przez cały dzień (od północy do północy)', 
                                                       'Wykres wzrostu energi (kaloryfery daleko od okien).png')

# Wykresy zmiany średnich temperatur w pokojach i mieszakniu
Experiment_radiators_far_from_windows.mean_rooms_temperatures_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                                                   converting_hours_into_iteration_steps(24, time_delta), 
                                                                   'Wykresy zmiany średnich temperatur w pokojach i mieszakniu (kaloryfery daleko od okien).png')


# Problem 2
# Zmienianie mocy Kaloryferów

reduse_heating_1 = np.matrix([[converting_hours_into_iteration_steps(6, time_delta), 3],  
                              [converting_hours_into_iteration_steps(8, time_delta), 2], 
                              [converting_hours_into_iteration_steps(15, time_delta), 3],
                              [converting_hours_into_iteration_steps(22, time_delta), 2]])

reduse_heating_2 = np.matrix([[converting_hours_into_iteration_steps(6, time_delta), 3], 
                              [converting_hours_into_iteration_steps(8, time_delta), 1], 
                              [converting_hours_into_iteration_steps(15, time_delta), 3], 
                              [converting_hours_into_iteration_steps(22, time_delta), 2]])

reduse_heating_3 = np.matrix([[converting_hours_into_iteration_steps(6, time_delta), 3], 
                              [converting_hours_into_iteration_steps(8, time_delta), 0], 
                              [converting_hours_into_iteration_steps(15, time_delta), 3],
                              [converting_hours_into_iteration_steps(22, time_delta), 2]])

radiator_location_1 = [(1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9), (1,10), (1,11), (1,12)]
radiator_location_2 = [(1,3), (1,4), (1,5), (1,6)]
radiator_location_3 = [(9,3), (9,4), (9,5), (9,6), (9,7), (9,8), (9,9)] 
radiator_location_4 = [(9,1), (9,2)]

# 1) Bardzo zimny dzień

# 1.1) Zmiana ogrzewania na 2 przed wyjściem z mieszkania
Experiment_with_a_knob = Experiment(initial_temperature, density, specific_heat, outside_temperature_very_cold_day, 
                                    radiator_location_1, 
                                    radiator_location_2, 
                                    radiator_location_3, 
                                    radiator_location_4, 
                                    radiators_power, alpha, reduse_heating_1, 
                                    time_delta, h)

# Mapy ciepła
Experiment_with_a_knob.twelve_heat_maps_over_time(converting_hours_into_iteration_steps(15, time_delta), 
                                                  converting_hours_into_iteration_steps(16, time_delta), 
                                                  ['15:05', '15:10', '15:15', 
                                                   '15:20', '15:25', '15:30',
                                                   '15:35', '15:40', '15:45', 
                                                   '15:50', '15:55', '16:00'], 
                                                   'Zmiana temperatury po powrocie i zmianie mocy grzania (bardzo zimny dzień i zmiana ogrzewania na 2).png')

# Wykres energii
Experiment_with_a_knob.used_energy_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                        converting_hours_into_iteration_steps(24, time_delta), 
                                        'Wykres wzrostu pobieranej energi przez cały bardzo zimny dzień', 
                                        'Wykres wzrostu energi (bardzo zimny dzień i zmiana ogrzewania na 2).png')

# Wykresy zmiany średnich temperatur w pokojach i mieszakniu
Experiment_with_a_knob.mean_rooms_temperatures_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                                    converting_hours_into_iteration_steps(24, time_delta), 
                                                    'Wykresy zmiany średnich temperatur w pokojach i mieszakniu (bardzo zimny dzień i zmiana ogrzewania na 2).png')

# 1.2) Zmiana ogrzewania na 1 przed wyjściem z mieszkania
Experiment_with_a_knob = Experiment(initial_temperature, density, specific_heat, outside_temperature_very_cold_day, 
                                    radiator_location_1, 
                                    radiator_location_2, 
                                    radiator_location_3, 
                                    radiator_location_4, 
                                    radiators_power, alpha, reduse_heating_2, 
                                    time_delta, h)

# Mapy ciepła
Experiment_with_a_knob.twelve_heat_maps_over_time(converting_hours_into_iteration_steps(15, time_delta), 
                                                  converting_hours_into_iteration_steps(16, time_delta), 
                                                  ['15:05', '15:10', '15:15', 
                                                   '15:20', '15:25', '15:30',
                                                   '15:35', '15:40', '15:45', 
                                                   '15:50', '15:55', '16:00'], 
                                                   'Zmiana temperatury po powrocie i zmianie mocy grzania (bardzo zimny dzień i zmiana ogrzewania na 1).png')

# Wykres energii
Experiment_with_a_knob.used_energy_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                        converting_hours_into_iteration_steps(24, time_delta), 
                                        'Wykres wzrostu pobieranej energi przez cały bardzo zimny dzień', 
                                        'Wykres wzrostu energi (bardzo zimny dzień i zmiana ogrzewania na 1).png')

# Wykresy zmiany średnich temperatur w pokojach i mieszakniu
Experiment_with_a_knob.mean_rooms_temperatures_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                                    converting_hours_into_iteration_steps(24, time_delta), 
                                                    'Wykresy zmiany średnich temperatur w pokojach i mieszakniu (bardzo zimny dzień i zmiana ogrzewania na 1).png')

# 1.3) Brak ogrzewania po wyjściem z mieszkania
Experiment_with_a_knob = Experiment(initial_temperature, density, specific_heat, outside_temperature_very_cold_day, 
                                    radiator_location_1, 
                                    radiator_location_2, 
                                    radiator_location_3, 
                                    radiator_location_4, 
                                    radiators_power, alpha, reduse_heating_3, 
                                    time_delta, h)

# Mapy ciepła
Experiment_with_a_knob.twelve_heat_maps_over_time(converting_hours_into_iteration_steps(15, time_delta), 
                                                  converting_hours_into_iteration_steps(16, time_delta), 
                                                  ['15:05', '15:10', '15:15', 
                                                   '15:20', '15:25', '15:30',
                                                   '15:35', '15:40', '15:45', 
                                                   '15:50', '15:55', '16:00'], 
                                                   'Zmiana temperatury po powrocie i zmianie mocy grzania (bardzo zimny dzień i brak ogrzewania).png')

# Wykres energii
Experiment_with_a_knob.used_energy_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                        converting_hours_into_iteration_steps(24, time_delta), 
                                        'Wykres wzrostu pobieranej energi przez cały bardzo zimny dzień', 
                                        'Wykres wzrostu energi (bardzo zimny dzień i brak ogrzewania).png')

# Wykresy zmiany średnich temperatur w pokojach i mieszakniu
Experiment_with_a_knob.mean_rooms_temperatures_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                                    converting_hours_into_iteration_steps(24, time_delta), 
                                                    'Wykresy zmiany średnich temperatur w pokojach i mieszakniu (bardzo zimny dzień i brak ogrzewania).png')

# 2) Zimny dzień

# 2.1) Zmiana ogrzewania na 2 przed wyjściem z mieszkania
Experiment_with_a_knob = Experiment(initial_temperature, density, specific_heat, outside_temperature_cold_day, 
                                    radiator_location_1, 
                                    radiator_location_2, 
                                    radiator_location_3, 
                                    radiator_location_4, 
                                    radiators_power, alpha, reduse_heating_1, 
                                    time_delta, h)

# Mapy ciepła
Experiment_with_a_knob.twelve_heat_maps_over_time(converting_hours_into_iteration_steps(15, time_delta), 
                                                  converting_hours_into_iteration_steps(16, time_delta), 
                                                  ['15:05', '15:10', '15:15', 
                                                   '15:20', '15:25', '15:30',
                                                   '15:35', '15:40', '15:45', 
                                                   '15:50', '15:55', '16:00'], 
                                                   'Zmiana temperatury po powrocie i zmianie mocy grzania (zimny dzień i zmiana ogrzewania na 2).png')

# Wykres energii
Experiment_with_a_knob.used_energy_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                        converting_hours_into_iteration_steps(24, time_delta), 
                                        'Wykres wzrostu pobieranej energi przez cały zimny dzień', 
                                        'Wykres wzrostu energi (zimny dzień i zmiana ogrzewania na 2).png')

# Wykresy zmiany średnich temperatur w pokojach i mieszakniu
Experiment_with_a_knob.mean_rooms_temperatures_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                                    converting_hours_into_iteration_steps(24, time_delta), 
                                                    'Wykresy zmiany średnich temperatur w pokojach i mieszakniu (zimny dzień i zmiana ogrzewania na 2).png')

# 2.2) Zmiana ogrzewania na 1 przed wyjściem z mieszkania
Experiment_with_a_knob = Experiment(initial_temperature, density, specific_heat, outside_temperature_cold_day, 
                                    radiator_location_1, 
                                    radiator_location_2, 
                                    radiator_location_3, 
                                    radiator_location_4, 
                                    radiators_power, alpha, reduse_heating_2, 
                                    time_delta, h)

# Mapy ciepła
Experiment_with_a_knob.twelve_heat_maps_over_time(converting_hours_into_iteration_steps(15, time_delta), 
                                                  converting_hours_into_iteration_steps(16, time_delta), 
                                                  ['15:05', '15:10', '15:15', 
                                                   '15:20', '15:25', '15:30',
                                                   '15:35', '15:40', '15:45', 
                                                   '15:50', '15:55', '16:00'], 
                                                   'Zmiana temperatury po powrocie i zmianie mocy grzania (zimny dzień i zmiana ogrzewania na 1).png')

# Wykres energii
Experiment_with_a_knob.used_energy_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                        converting_hours_into_iteration_steps(24, time_delta), 
                                        'Wykres wzrostu pobieranej energi przez cały zimny dzień', 
                                        'Wykres wzrostu energi (zimny dzień i zmiana ogrzewania na 1).png')

# Wykresy zmiany średnich temperatur w pokojach i mieszakniu
Experiment_with_a_knob.mean_rooms_temperatures_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                                    converting_hours_into_iteration_steps(24, time_delta), 
                                                    'Wykresy zmiany średnich temperatur w pokojach i mieszakniu (zimny dzień i zmiana ogrzewania na 1).png')

# 2.3) Brak ogrzewania po wyjściem z mieszkania
Experiment_with_a_knob = Experiment(initial_temperature, density, specific_heat, outside_temperature_cold_day, 
                                    radiator_location_1, 
                                    radiator_location_2, 
                                    radiator_location_3, 
                                    radiator_location_4, 
                                    radiators_power, alpha, reduse_heating_3, 
                                    time_delta, h)

# Mapy ciepła
Experiment_with_a_knob.twelve_heat_maps_over_time(converting_hours_into_iteration_steps(15, time_delta), 
                                                  converting_hours_into_iteration_steps(16, time_delta), 
                                                  ['15:05', '15:10', '15:15', 
                                                   '15:20', '15:25', '15:30',
                                                   '15:35', '15:40', '15:45', 
                                                   '15:50', '15:55', '16:00'], 
                                                   'Zmiana temperatury po powrocie i zmianie mocy grzania (zimny dzień i brak ogrzewania).png')

# Wykres energii
Experiment_with_a_knob.used_energy_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                        converting_hours_into_iteration_steps(24, time_delta), 
                                        'Wykres wzrostu pobieranej energi przez cały zimny dzień', 
                                        'Wykres wzrostu energi (zimny dzień i brak ogrzewania).png')

# Wykresy zmiany średnich temperatur w pokojach i mieszakniu
Experiment_with_a_knob.mean_rooms_temperatures_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                                    converting_hours_into_iteration_steps(24, time_delta), 
                                                    'Wykresy zmiany średnich temperatur w pokojach i mieszakniu (zimny dzień i brak ogrzewania).png')

# 3) Chłodny dzień

# 3.1) Zmiana ogrzewania na 2 przed wyjściem z mieszkania
Experiment_with_a_knob = Experiment(initial_temperature, density, specific_heat, outside_temperature_cool_day, 
                                    radiator_location_1, 
                                    radiator_location_2, 
                                    radiator_location_3, 
                                    radiator_location_4, 
                                    radiators_power, alpha, reduse_heating_1, 
                                    time_delta, h)

# Mapy ciepła
Experiment_with_a_knob.twelve_heat_maps_over_time(converting_hours_into_iteration_steps(15, time_delta), 
                                                  converting_hours_into_iteration_steps(16, time_delta), 
                                                  ['15:05', '15:10', '15:15', 
                                                   '15:20', '15:25', '15:30',
                                                   '15:35', '15:40', '15:45', 
                                                   '15:50', '15:55', '16:00'], 
                                                   'Zmiana temperatury po powrocie i zmianie mocy grzania (chłodny dzień i zmiana ogrzewania na 2).png')

# Wykres energii
Experiment_with_a_knob.used_energy_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                        converting_hours_into_iteration_steps(24, time_delta), 
                                        'Wykres wzrostu pobieranej energi przez cały chłodny dzień', 
                                        'Wykres wzrostu energi (chłodny dzień i zmiana ogrzewania na 2).png')

# Wykresy zmiany średnich temperatur w pokojach i mieszakniu
Experiment_with_a_knob.mean_rooms_temperatures_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                                    converting_hours_into_iteration_steps(24, time_delta), 
                                                    'Wykresy zmiany średnich temperatur w pokojach i mieszakniu (chłodny dzień i zmiana ogrzewania na 2).png')

# 3.2) Zmiana ogrzewania na 1 przed wyjściem z mieszkania
Experiment_with_a_knob = Experiment(initial_temperature, density, specific_heat, outside_temperature_cool_day, 
                                    radiator_location_1, 
                                    radiator_location_2, 
                                    radiator_location_3, 
                                    radiator_location_4, 
                                    radiators_power, alpha, reduse_heating_2, 
                                    time_delta, h)

# Mapy ciepła
Experiment_with_a_knob.twelve_heat_maps_over_time(converting_hours_into_iteration_steps(15, time_delta), 
                                                  converting_hours_into_iteration_steps(16, time_delta), 
                                                  ['15:05', '15:10', '15:15', 
                                                   '15:20', '15:25', '15:30',
                                                   '15:35', '15:40', '15:45', 
                                                   '15:50', '15:55', '16:00'], 
                                                   'Zmiana temperatury po powrocie i zmianie mocy grzania (chłodny dzień i zmiana ogrzewania na 1).png')

# Wykres energii
Experiment_with_a_knob.used_energy_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                        converting_hours_into_iteration_steps(24, time_delta), 
                                        'Wykres wzrostu pobieranej energi przez cały chłodny dzień', 
                                        'Wykres wzrostu energi (chłodny dzień i zmiana ogrzewania na 1).png')

# Wykresy zmiany średnich temperatur w pokojach i mieszakniu
Experiment_with_a_knob.mean_rooms_temperatures_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                                    converting_hours_into_iteration_steps(24, time_delta), 
                                                    'Wykresy zmiany średnich temperatur w pokojach i mieszakniu (chłodny dzień i zmiana ogrzewania na 1).png')

# 3.3) Brak ogrzewania po wyjściem z mieszkania
Experiment_with_a_knob = Experiment(initial_temperature, density, specific_heat, outside_temperature_cool_day, 
                                    radiator_location_1, 
                                    radiator_location_2, 
                                    radiator_location_3, 
                                    radiator_location_4, 
                                    radiators_power, alpha, reduse_heating_3, 
                                    time_delta, h)

# Mapy ciepła
Experiment_with_a_knob.twelve_heat_maps_over_time(converting_hours_into_iteration_steps(15, time_delta), 
                                                  converting_hours_into_iteration_steps(16, time_delta), 
                                                  ['15:05', '15:10', '15:15', 
                                                   '15:20', '15:25', '15:30',
                                                   '15:35', '15:40', '15:45', 
                                                   '15:50', '15:55', '16:00'], 
                                                   'Zmiana temperatury po powrocie i zmianie mocy grzania (chłodny dzień i brak ogrzewania).png')

# Wykres energii
Experiment_with_a_knob.used_energy_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                        converting_hours_into_iteration_steps(24, time_delta), 
                                        'Wykres wzrostu pobieranej energi przez cały chłodny dzień', 
                                        'Wykres wzrostu energi (chłodny dzień i brak ogrzewania).png')

# Wykresy zmiany średnich temperatur w pokojach i mieszakniu
Experiment_with_a_knob.mean_rooms_temperatures_plot(converting_hours_into_iteration_steps(0, time_delta), 
                                                    converting_hours_into_iteration_steps(24, time_delta), 
                                                    'Wykresy zmiany średnich temperatur w pokojach i mieszakniu (chłodny dzień i brak ogrzewania).png')