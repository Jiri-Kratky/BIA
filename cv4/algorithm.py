import math
import random
import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
from matplotlib import cm

distance = int(input("size of the map: "))
generations = int(input("Number of generations: "))
destination_count = int(input("Number of destinations (cities): "))
individuals = int(input("Number of individuals (SalesMen): "))

mutation_rate = destination_count / individuals  # cities/individuals

cities = np.random.uniform(low=0, high=distance, size=(destination_count, 2))


class SalesMan:
    destinations = []  # order of visiting cities
    fitness = 0
    distances = 0

    def __init__(self):  # generate random path to go through all destinations
        self.destinations = [i for i in range(destination_count)]
        random.shuffle(self.destinations)
        self.destinations.append(
            self.destinations[0]
        )  # add first city to the end of the path

    def calculate_fitness(self):
        tmp_distance = 0
        current_position = cities[self.destinations[0]]
        for i in range(1, destination_count):
            tmp_distance += (
                (current_position[0] - cities[self.destinations[i]][0]) ** 2
                + (current_position[1] - cities[self.destinations[i]][1]) ** 2
            ) ** 0.5  # compute distance between two cities (euclidean method) could also use manhattan method
            current_position = cities[self.destinations[i]]

        self.distances = tmp_distance  # distance of the path
        self.fitness = (
            tmp_distance / distance
        )  # we want fitness to be grater than 1 and also we want to have different fitness values for different distances


plt.scatter
plt.xlabel("Distance X")
plt.ylabel("Distance Y")
plt.xlim(0, distance)
plt.ylim(0, distance)
plt.title("Genetic Algorithm")


population = []
for i in range(individuals):  # generate initial population
    population.append(SalesMan())

Best_salesman = SalesMan()
generation_count = 0

while generation_count < generations:  # loop until number of generations is reached
    generation_count += 1

    # Calculating the fitness
    for i in population:
        i.calculate_fitness()

        if Best_salesman.distances == 0:
            Best_salesman = population[0]

        elif (
            Best_salesman.distances >= i.distances
        ):  # find the best individual overall (fastest SalesMan)
            print(f"Generation ({generation_count}) Best SalesMan: " + str(i.distances))
            Best_salesman = i

    # Generating a mating pool
    mating_pool = []
    for i in population:
        for j in range(
            int(i.fitness) ** 3
        ):  # those who have higher fitness have more chance to be selected
            mating_pool.append(i)

    population = []  # clear population

    # Generating the next generation
    for i in range(individuals):
        # randomly select two parents
        parent_A = random.choice(mating_pool)
        parent_B = random.choice(mating_pool)

        # Crossover
        break_point_0 = random.randrange(0, destination_count)
        break_point_1 = random.randrange(break_point_0, destination_count)
        child = SalesMan()
        child.destinations = [-1 for i in range(destination_count)]
        child.destinations[break_point_0:break_point_1] = parent_A.destinations[
            break_point_0:break_point_1
        ]
        for (
            i
        ) in (
            parent_B.destinations
        ):  # fill the rest of the child with the cities from the second parent
            if i not in child.destinations:
                for j in range(destination_count):
                    if child.destinations[j] == -1:
                        child.destinations[j] = i
                        break

        # Mutation
        record = random.random()  # number from [0 to 1) => randomly mutate child
        if record < mutation_rate:
            break_point = random.randrange(
                0, destination_count
            )  # randomly select two cities and swap them
            (
                child.destinations[break_point],
                child.destinations[(break_point + 1) % destination_count],
            ) = (
                child.destinations[(break_point + 1) % destination_count],
                child.destinations[break_point],
            )

        child.destinations.append(
            child.destinations[0]
        )  # add first city to the end of the path

        population.append(child)  # Add child into the new population

for i in range(destination_count):  # Show cities on the map and their numbers
    plt.scatter(cities[i][0], cities[i][1], color="red", s=25, marker="+")
    plt.text(cities[i][0] + 2, cities[i][1] + 2, str(i), fontsize=12)

print(f"\nSalesMan path: {Best_salesman.destinations}")
print(f"\nShortest distance: {Best_salesman.distances}")

path = Best_salesman.destinations[0:]

x = []
y = []

for i in path:
    x.append(cities[i][0])
    y.append(cities[i][1])

plt.plot(x, y, color="m", linewidth=1, linestyle="-")

plt.show()
