import numpy as np
import matplotlib.pyplot as plt

def Celsius_to_Kelvin(tempertures):
    if type(tempertures) == list:
        new_temperatures = []
        for temp in tempertures:
            new_temperatures.append(temp + 273.15)
        return(new_temperatures)
    return(tempertures + 273.15)

def Kelvin_to_Celsius(tempertures):
    if type(tempertures) == list:
        new_temperatures = []
        for temp in tempertures:
            new_temperatures.append(temp - 273.15)
        return(new_temperatures)
    return(tempertures - 273.15)

def converting_hours_into_iteration_steps(hours, time_delta):
    iteration = int(hours * 60 * 60 * 1/time_delta)
    return(iteration)

def converting_iteration_steps_into_hours(iteration_steps, time_delta):
    hours = iteration_steps / 60 / 60 * time_delta
    return(hours)

def outside_temperature_in_time_iteration(outside_temperature, time_delta):
    new_outside_temperatures = []
    number_of_iterations_with_given_temperature = converting_hours_into_iteration_steps(1/6, time_delta)
    for temp in outside_temperature:
        new_outside_temperatures = [*new_outside_temperatures, *np.repeat(temp,number_of_iterations_with_given_temperature)]
    return(new_outside_temperatures)

def give_second_column_when_first_is_equal(matrix, number):
    row_matrix = np.where(matrix[:, 0] == number)[0][0]
    return(matrix[row_matrix, 1])

def surroundings(m, n, location):
    y = location[0]
    x = location[1]
    neighbors = []
    if x-1 > 0:
        neighbors.append((y, x-1))
    if x+1 < n-1:
        neighbors.append((y, x+1))
    if y-1 > 0:
        neighbors.append((y-1, x))
    if y+1 < m-1:
        neighbors.append((y+1, x))
    if x-1 > 0 and y-1 > 0:
        neighbors.append((y-1, x-1))
    if x+1 < n-1 and y-1 > 0:
        neighbors.append((y-1, x+1))
    if x+1 < n-1 and y+1 < m-1:
        neighbors.append((y+1, x+1))
    if x-1 > 0 and y+1 < m-1:
        neighbors.append((y+1, x-1))
    return(neighbors)

def sketch_of_the_apartment(radiators_location, file_title):
    apartment = np.full((30, 27), 0)

    walls_location = list(set([*[(0, i) for i in range(0, 27)],
                               *[(12, i) for i in range(16, 27)],
                               *[(13, i) for i in range(16, 27)],
                               *[(18, i) for i in range(0, 27)],
                               *[(19, i) for i in range(9, 27)],
                               *[(29, i) for i in range(9, 27)],
                               *[(i, 0) for i in range(0, 19)],
                               *[(i, 9) for i in range(19, 30)],
                               *[(i, 16) for i in range(0, 19)],
                               *[(i, 17) for i in range(0, 19)],
                               *[(i, 21) for i in range(18, 30)],
                               *[(i, 22) for i in range(18, 30)],
                               *[(i, 26) for i in range(0, 30)]]))
    
    for part in walls_location:
        apartment[part] = 1
    
    windows_location = list(set([(0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,9), (0,10), (0,11), (0,12), (0,13),
                                 (0,20), (0,21), (0,22), (0,23), (0,24),
                                 (29,12), (29,13), (29,14), (29,15), (29,16), (29,17), (29,18),
                                 (29,23), (29,24), (29,25)]))
    
    for part in windows_location:
        apartment[part] = 2
    
    doors_location = list(set([(12,19), (12,20), (13,19), (13,20),
                               (15,16), (16,16), (15,17), (16,17),
                               (18,19), (18,20), (19,19), (19,20),
                               (18,24), (18,25), (19,24), (19,25)]))
    
    for part in doors_location:
        apartment[part] = 0

    for part in radiators_location:
        apartment[part] = 3
    
    colors = {0: 'white', 1: 'black', 2: 'blue', 3: 'yellow'}

    fig, ax = plt.subplots()
    for (i, j), val in np.ndenumerate(apartment):
        ax.add_patch(plt.Rectangle((j, -i), 1, 1, color=colors[val]))

    ax.set_xlim(0, apartment.shape[1])
    ax.set_ylim(1-apartment.shape[0], 1)
    ax.set_title('Analizowane Mieszkanie')
    ax.set_aspect('equal')

    # Dodanie siatki w tle
    ax.set_xticks(np.arange(0, apartment.shape[1], 1), minor=False)
    ax.set_yticks(np.arange(1-apartment.shape[0], 1, 1), minor=False)
    ax.grid(visible=True, which='both', color='lightgrey', linestyle='--', linewidth=0.5)

    # Ukrywanie osi, ale pozostawienie siatki
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

    handles = [plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=color, markersize=10, label=label)
               for label, color in zip(['Ściany', 'Okna', 'Kaloryfery'], ['black', 'blue', 'yellow'])]
    ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(1, 1))

    room_labels = {
        '1': (9, 8),
        '2': (6, 22),
        '3': (23.5, 16),
        '4': (23, 24.5),
        '5': (15, 22),
    }

    for room_name, (y, x) in room_labels.items():
        ax.text(x, -y, room_name, fontsize=10, ha='center', va='center', color='black', fontweight='bold')

    plt.savefig(file_title)
    #plt.show() f
    plt.close()
    




