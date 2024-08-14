import math
import random
import defined_functions as functions
import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter

class AntColonyOptimization():
    def __init__(self, cities, n_ants, n_best, n_iterations, decay=0.1, alpha=1, beta=1):
        self.cities = cities        # city coordinates
        self.distances = self.create_matrix_distances() # distance matrix between cities
        self.pheromone = np.ones(self.distances.shape) / len(self.distances) # pheromone matrix
        self.all_inds = range(len(self.distances)) # city indexes
        self.n_ants = n_ants # ant count
        self.n_best = n_best # number of best paths
        self.n_iterations = n_iterations # number of iterations
        self.decay = decay # decay of pheromone
        self.alpha = alpha # influence of pheromone
        self.beta = beta # influence of distance
        self.fig, self.ax = plt.subplots() 
        self.lines = []

    def create_matrix_distances(self): # compute distance between cities
        matrix = np.zeros((len(self.cities), len(self.cities))) 
        for i in range(len(self.cities)):
            for j in range(len(self.cities)):
                if i != j:
                    matrix[i][j] = ((self.cities[i][0] - self.cities[j][0]) ** 2 +
                                    (self.cities[i][1] - self.cities[j][1]) ** 2) ** 0.5
                else:
                    matrix[i][j] = np.inf

        return matrix

    def run(self):
        shortest_path = None
        all_time_shortest_path = (None, np.inf) 
        for i in range(self.n_iterations): 
            all_paths = self.gen_all_paths() # generate all paths
            shortest_path = min(all_paths, key=lambda x: x[1]) # shortest path
            if shortest_path[1] < all_time_shortest_path[1]: # if shortest path is better than all time shortest path
                all_time_shortest_path = shortest_path
                self.ax.clear()
                self.display_paths(all_time_shortest_path[0])
                print("Iteration: {}, shortest path: {}".format(i, all_time_shortest_path[1]))
                plt.pause(1)

            self.pheromone *= (1 - self.decay)  # decay of pheromone
            self.spread_pheromone(all_paths, self.n_best, shortest_path=shortest_path) # spread pheromone

        plt.show()

    def spread_pheromone(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1]) # sort paths by distance
        for path, dist in sorted_paths[:n_best]: # for n best paths spread pheromone
            for move in path: # for all moves in path
                self.pheromone[move] += 1.0 / self.distances[move] # add pheromone

    def gen_path_dist(self, path):
        total_dist = 0 # total distance
        for ele in path:  
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = [] # all paths
        for i in range(self.n_ants): 
            path = self.gen_path(i) # ants path
            all_paths.append((path, self.gen_path_dist(path))) # add path and distance to all paths touple (path, distance)
        return all_paths

    def gen_path(self, ant_index):
        path = []
        visited = set()                         # visited cities
        start = np.random.choice(self.all_inds) # select random city as start location
        visited.add(start)                      # add start location to visited
        prev = start 
        for i in range(len(self.distances) - 1):        # for all cities
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited) # selection of next city
            path.append((prev, move))                   # add selected city to path
            prev = move                                 
            visited.add(move)                           # add selected city to visited
        path.append((prev, start))                      # at last add start location to path to close the loop
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone) 
        pheromone[list(visited)] = 0                              # set pheromon of visited cities to 0
        row = pheromone ** self.alpha * (1.0 / dist) ** self.beta # compute probability of next city
        norm_row = row / row.sum()                                # normalize probability
        move = np.random.choice(self.all_inds, 1, p=norm_row)[0]  # select next city from cities
        return move

    def display_paths(self, path):
        path_coords = np.array([self.cities[i] for i, _ in path]) 
        path_line, = self.ax.plot(path_coords[:, 0], path_coords[:, 1], marker='o', linestyle='-', linewidth=1, markersize=3, color='blue') 

        # Connect the last point to the starting point to close the loop
        start_point = path_coords[0]
        path_line, = self.ax.plot([path_coords[-1, 0], start_point[0]], [path_coords[-1, 1], start_point[1]],
                                marker='o', linestyle='-', linewidth=1, markersize=3, color='blue')
        
        self.lines.append(path_line)


cities = [(np.random.uniform(0, 10), np.random.uniform(0, 10)) for i in range(25)]
ant_colony = AntColonyOptimization(cities, n_ants=15, n_best=2, n_iterations=120, decay=0.1, alpha=1, beta=1)
ant_colony.run()