import math
import random
import defined_functions as functions
import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter


class Individual:
    Fitness = 0
    Position = []
    function = None

    def __init__(self, Position, function: functions.Function):
        self.Position = Position
        self.function = function
        self.calculate_Fitnes()

    def calculate_Fitnes(self):
        self.Fitness = self.function.execute(self.Position[0], self.Position[1])


def soma_all_to_one(
    function: functions.Function,
    pop_size=10,
    PRT=0.3,
    PathLength=3.0,
    Step=0.11,
    N_MAX=10,
):
    
    """
    SOMA AllToOne algorithm implementation.

    pop_size (int): Number of individuals.
    PRT (float): Probability of random mutation.
    PathLength (float): Maximum path length.    (1 jsem u leadra, 2 přeskočím lídra 1x, 3 - přeskočím leadra 2x)
    Step (float): Step size.
    N_MAX (int): Maximum number of iterations.
    """
    bounds = (function.min, function.max)

    Population = []
    # Initialize population with random starting points in the bounds
    for i in range(pop_size):
        for j in range(2):
            x = random.uniform(bounds[0], bounds[1])
            y = random.uniform(bounds[0], bounds[1])
            Population.append(Individual([x, y], function))


    bestIndividual = Population[0]
    for i in range(pop_size):
        if Population[i].Fitness < bestIndividual.Fitness:
            bestIndividual = Population[i]
        
    new_population = []
    for gen in range(N_MAX):
            if(new_population != []):
                Population = new_population
                new_population = []

            for individual in Population:

                prt_vector = np.zeros((2))  #vector for random mutation
                for i in range(2):
                    if random.random() > PRT:
                        prt_vector[i] = 1


                #create path on which will be generated new position  
                t = np.arange(0, PathLength, Step)          #array starting from 0 to PathLength with step (0, 0.11, 0.22,....)

                new_positions = []
                index=0
                for i in range(len(t)):
                    new_positionx = individual.Position[0] + (bestIndividual.Position[0] - individual.Position[0]) * t[index] * prt_vector[0]
                    new_positiony = individual.Position[1] + (bestIndividual.Position[1] -individual.Position[1]) * t[index] * prt_vector[1]
                    new_position = np.array([new_positionx,new_positiony])

                    #clip directions within bounds
                    for k in range(len(bounds)):
                        new_position[k] = max(min(new_position[k], bounds[1]), bounds[0])
                    new_positions.append(new_position)


                # Find new position for selected individual
                best_new_pos = new_positions[0]
                for new_position in new_positions:
                    if(function.execute(new_position[0], new_position[1]) < function.execute(best_new_pos[0], best_new_pos[1])):
                        best_new_pos = new_position         #find best position from new positions

                new_population.append(Individual(best_new_pos, function))       #add best new position to new population

            # Save best individual in each generation
            for i in new_population:
                if i.Fitness < bestIndividual.Fitness:
                    bestIndividual = i


    print("Best solution: ", bestIndividual.Position[0], bestIndividual.Position[1], "Fitness: ", bestIndividual.Fitness)
    f = open("SOMA_"+str(function.__name__)+".csv", "a")
    f.write(str(function.__name__) + ";" + str(bestIndividual.Fitness) + "\n")
    plt.close()


for i in range(30):
    soma_all_to_one(functions.Sphere, pop_size=30, N_MAX=30)
    soma_all_to_one(functions.Zakharov, pop_size=30, N_MAX=30)
    soma_all_to_one(functions.Rosenbrock, pop_size=30, N_MAX=30)
    soma_all_to_one(functions.Ackley, pop_size=30, N_MAX=30)
    soma_all_to_one(functions.Schwefel, pop_size=30, N_MAX=30)
    soma_all_to_one(functions.Rastrigin, pop_size=30, N_MAX=30)
    soma_all_to_one(functions.Griewank, pop_size=30, N_MAX=30)
    soma_all_to_one(functions.Levy, pop_size=30, N_MAX=30)
    soma_all_to_one(functions.Michalewicz, pop_size=30, N_MAX=30)
