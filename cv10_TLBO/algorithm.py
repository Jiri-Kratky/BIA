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


def teacher_phase(population,individual:Individual, function: functions.Function ):
    total_fitness = sum(person.Fitness for person in population)
    mean = total_fitness / len(population)

    #find best individual based on fitness
    teacher = min(population, key=lambda x: x.Fitness)
    DifferenceX = random.uniform(0,1) * (teacher.Position[0] - (random.randint(1,3) * mean))
    DifferenceY = random.uniform(0,1) * (teacher.Position[1] - (random.randint(1,3) * mean))

    #calculate new position
    new_position = [individual.Position[0] + DifferenceX,individual.Position[1] + DifferenceY]

    #clip new position within bounds
    for i in range(2):
        new_position[i] = max(min(new_position[i], function.max), function.min)

    if function.execute(new_position[0], new_position[1]) < individual.Fitness: #ovlivněný student je lepší než stávající
        individual.Position = new_position
        individual.calculate_Fitnes()

    if(individual.Fitness < teacher.Fitness):
        return individual
    else:
        return teacher


def learner_phase(individual:Individual, random_individual:Individual, function: functions.Function):
    if  individual.Fitness < random_individual.Fitness:
        new_position = [individual.Position[i] + random.uniform(0, 1) * (individual.Position[i] - random_individual.Position[i]) for i in range(2)]
    else:
        new_position = [individual.Position[i] + random.uniform(0, 1) * (random_individual.Position[i] - individual.Position[i]) for i in range(2)]

    #clip new position within bounds
    for i in range(2):
        new_position[i] = max(min(new_position[i], function.max), function.min)

    if (function.execute(new_position[0], new_position[1]) < individual.Fitness):
        individual.Position = new_position
        individual.calculate_Fitnes()


def TLBO(
    function: functions.Function,
    pop_size=30,
    N_MAX=30,
):
    bounds = [function.min, function.max]
    
    Population = []
    # Initialize population with random starting points in the bounds
    for i in range(pop_size):
        for j in range(2):
            x = random.uniform(bounds[0], bounds[1])
            y = random.uniform(bounds[0], bounds[1])
            Population.append(Individual([x, y], function))

    # Initialize best individual 
    bestIndividual = Population[0]

    for gen in range(N_MAX):
            for individual in Population:

                #Teacher phase
                bestIndividual = teacher_phase(Population, individual, function)      

                #Learner phase
                #find random individual (cant be the same as selected individual)
                tmp = Population.copy()
                tmp.remove(individual)
                random_individual = tmp[random.randint(0,len(tmp)-1)]
                learner_phase(individual,random_individual, function)     

    print("Best solution: ", bestIndividual.Position[0], bestIndividual.Position[1], "Fitness: ", bestIndividual.Fitness)
    #append to csv file best result:
    f = open("TLBO_"+str(function.__name__)+".csv", "a")
    f.write(str(function.__name__) + ";" + str(bestIndividual.Fitness) + "\n")

for i in range(30):
    TLBO(functions.Sphere,N_MAX=30,pop_size=30)
    TLBO(functions.Zakharov,N_MAX=30,pop_size=30)
    TLBO(functions.Rosenbrock,N_MAX=30,pop_size=30)
    TLBO(functions.Ackley,N_MAX=30,pop_size=30)
    TLBO(functions.Schwefel,N_MAX=30,pop_size=30)
    TLBO(functions.Rastrigin,N_MAX=30,pop_size=30)
    TLBO(functions.Griewank,N_MAX=30,pop_size=30)
    TLBO(functions.Levy,N_MAX=30,pop_size=30)
    TLBO(functions.Michalewicz,N_MAX=30,pop_size=30)
    

#TLBO(functions.Sphere, pop_size=30, N_MAX=5)

#TLBO(functions.Zakharov)

#TLBO(functions.Schwefel)
