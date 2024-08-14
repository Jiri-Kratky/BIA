import random
import numpy as np
import defined_functions as functions
import matplotlib.pyplot as plt
from matplotlib import cm


def differential_evolution(NP, G, F, CR, function: functions.Function):
    """
    Parameters:
    NP (int): Number of individuals.      (30)
    G (int): Number of generation cycles. (30)
    F (float): Mutation constant.   (0.5)
    CR (float): Crossover range.    (0.5)
    """
    bounds = (function.min, function.max)
    # Initialize population
    pop = np.zeros((NP, len(bounds)))
    for i in range(NP):
        for j in range(len(bounds)):
            pop[i, j] = random.uniform(bounds[0], bounds[1])

    # Evaluate initial population
    fitness = np.zeros(NP)
    for i in range(NP):
        fitness[i] = function.execute(pop[i, :][0], pop[i, :][1])

    # Heatmap
    N = 100
    X = np.linspace(function.min, function.max, N)
    Y = np.linspace(function.min, function.max, N)
    X, Y = np.meshgrid(X, Y)
    Z = function.execute(X, Y)

    fig, ax = plt.subplots()
    cax = ax.imshow(
        Z,
        cmap="jet",
        extent=[
            function.min,
            function.max,
            function.min,
            function.max,
        ],
    )

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.colorbar(cax)

    # Main loop
    for gen in range(G):
        for i in range(NP):
            # Select three random individuals
            a, b, c = random.sample(range(NP), 3)

            # Mutate individual
            mutant = pop[a, :] + F * (pop[b, :] - pop[c, :])    #F - mutation constant (0.5)

            # Crossover with probability CR
            trial = np.zeros(len(bounds))
            j_rand = random.randint(0, len(bounds) - 1)
            for j in range(len(bounds)):
                if random.random() < CR or j == j_rand:         #CR - crossover range (0.5)
                    trial[j] = mutant[j]
                else:
                    trial[j] = pop[i, j]

            # Clip trial within bounds
            for j in range(len(bounds)):
                trial[j] = max(min(trial[j], bounds[1]), bounds[0])

            # Evaluate trial
            f_trial = function.execute(trial[0], trial[1])

            # Update population
            if f_trial < fitness[i]:
                pop[i, :] = trial
                fitness[i] = f_trial

        # Return best solution
        best_idx = np.argmin(fitness)
        bestx = pop[best_idx, :][0]
        besty = pop[best_idx, :][1]
        ax.scatter(  # Přidání bodů do heatmapy
            bestx,
            besty,
            c="r",
            marker="o",
            s=30,
            edgecolors="k",
        )

    print("Best solution: ", bestx, besty, "Fitness: ", fitness[best_idx])
    #append to csv file best result:
    f = open("DE_"+str(function.__name__)+".csv", "a")
    f.write(str(function.__name__) + ";" + str(fitness[best_idx]) + "\n")
    plt.close()
    #plt.show()

for i in range(30):
    differential_evolution(30, 30, 0.5, 0.5, functions.Sphere)
    differential_evolution(30, 30, 0.5, 0.5, functions.Zakharov)
    differential_evolution(30, 30, 0.5, 0.5, functions.Rosenbrock)
    differential_evolution(30, 30, 0.5, 0.5, functions.Ackley)
    differential_evolution(30, 30, 0.5, 0.5, functions.Schwefel)
    differential_evolution(30, 30, 0.5, 0.5, functions.Rastrigin)
    differential_evolution(30, 30, 0.5, 0.5, functions.Griewank)
    differential_evolution(30, 30, 0.5, 0.5, functions.Levy)
    differential_evolution(30, 30, 0.5, 0.5, functions.Michalewicz)