import numpy as np

def heat_matrix(k):
    diff_matrix = np.zeros((k,k))
    for i in range(k):
        if i == 0:
            diff_matrix[(i, i)] = -2
            diff_matrix[(i, i+1)] = 1
        if i == k-1:
            diff_matrix[(i, i-1)] = 1
            diff_matrix[(i, i)] = -2
        if i != 0 and i != k-1:
            diff_matrix[(i, i-1)] = 1
            diff_matrix[(i, i)] = -2
            diff_matrix[(i, i+1)] = 1

    return(diff_matrix)

def heat_matrix_2D(dimensions):
    D_x = heat_matrix(dimensions[1])
    D_y = heat_matrix(dimensions[0])
    return(np.kron(np.identity(dimensions[0]), D_x) + np.kron(D_y, np.identity(dimensions[1])))

class Room:
    def __init__(self, dimensions, initial_temperature, density, specific_heat):
        self.m = dimensions[0]
        self.n = dimensions[1]

        self.L = heat_matrix_2D(dimensions)

        self.initial_temperature = initial_temperature
        heat_area = np.full(dimensions, initial_temperature)
        self.heat_area = heat_area

        self.density = density
        self.specific_heat = specific_heat
    
    def update_temperature(self, alpha, time_delta, h):
        self.heat_area = self.heat_area.flatten()
        self.heat_area = self.heat_area + alpha * (time_delta/(h**2)) * np.matmul(self.L, self.heat_area)
        self.heat_area = self.heat_area.reshape(self.m, self.n)

    def mean_temperature(self):
        sum = 0
        for i in np.arange(1, self.n - 1):
            sum = sum + np.sum(self.heat_area[np.arange(1, self.m - 1), i])
        return(sum/((self.m-2)*(self.n-2)))
    
    def local_mean_temperature(self, location):
        sum = 0
        for part in location:
            sum = sum + self.heat_area[part]
        return(sum/len(location))


