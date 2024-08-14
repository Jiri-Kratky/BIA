import random
import numpy as np
import defined_functions as functions
import matplotlib.pyplot as plt
from matplotlib import cm


def PSO_inertia_weight(population_size, c1, c2, M_max, function: functions.Function):
    """
    Pop size 15
    c1 = 2
    c2 = 2
    M_max = 50
    """
    # Initialize the swarm
    swarm = []
    for i in range(population_size):
        swarm.append(np.random.uniform(-5, 5, size=2))

    # Initialize the velocities
    velocities = []
    for i in range(population_size):
        velocities.append(np.random.uniform(0, 1, size=2))

    personal_best_positions = swarm.copy()
    # Initialize the personal best positions and values
    personal_best_values = []
    global_best_position = swarm[0]
    global_best_value = function.execute(swarm[0][0], swarm[0][1])

    # Initialize the global best position and value
    for i in range(population_size):
        personal_best_values.append(function.execute(swarm[i][0], swarm[i][1]))
        if personal_best_values[i] < function.execute(
            global_best_position[0], global_best_position[1]
        ):
            global_best_position = personal_best_positions[i]
            global_best_value = personal_best_values[i]

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

    bestx = global_best_position[0]
    besty = global_best_position[1]
    ax.scatter(  # Přidání bodů do heatmapy
        bestx,
        besty,
        c="red",
        marker="o",
        s=30,
        edgecolors="k",
    )
    colors = [
        "white",
        "yellow",
        "orange",
        "red",
        "black",
        "green",
        "blue",
        "purple",
        "pink",
        "brown",
        "gray",
        "cyan",
        "magenta",
        "olive",
        "navy",
    ]

    # Initialize the inertia weight
    w = 0.9

    M = 0
    # Main loop
    while M < M_max:
        for i in range(population_size - 1):
            r1, r2 = random.random(), random.random()
            # Update the velocity
            velocities[i][0] = (
                w * velocities[i][0]
                + c1 * r1 * (personal_best_positions[i][0] - swarm[i][0])
                + c2 * r2 * (global_best_position[0] - swarm[i][0])
            )

            velocities[i][1] = (
                w * velocities[i][1]
                + c1 * r1 * (personal_best_positions[i][1] - swarm[i][1])
                + c2 * r2 * (global_best_position[1] - swarm[i][1])
            )

            # check if velocity is within bounds, if no, change it to minimum or maximum
            for j in range(2):
                if velocities[i][j] < -1:
                    velocities[i][j] = -1  # set minimal velocity to -1
                elif velocities[i][j] > 1:
                    velocities[i][j] = 1  # set maximal velocity to 1

            # Update the position
            swarm[i] = swarm[i] + velocities[i]

            # check if the new position is within bounds, if no, change it to minimum or maximum
            for j in range(2):
                if swarm[i][j] < function.min:
                    swarm[i][j] = function.min
                elif swarm[i][j] > function.max:
                    swarm[i][j] = function.max

            # Check if the new position is better than the personal best
            new_value = function.execute(swarm[i][0], swarm[i][1])

            if new_value < personal_best_values[i]:
                personal_best_values[i] = new_value
                personal_best_positions[i] = swarm[i]

            # Check if the new position is better than the global best
            if new_value < global_best_value:
                global_best_value = new_value
                global_best_position = swarm[i]

                # show new best position on plot
                bestx = global_best_position[0]
                besty = global_best_position[1]
                ax.scatter(  # Přidání bodů do heatmapy
                    bestx,
                    besty,
                    c="red",
                    marker="o",
                    s=30,
                    edgecolors="k",
                )
            # common = (swarm[i][0], swarm[i][1])
            # ax.scatter(  # Přidání všech bodů do heatmapy
            #    common[0],
            #    common[1],
            #    c=colors[i],
            #    marker="o",
            #    s=30,
            #    edgecolors="k",
            # )
            
            # Update the inertia weight --- W-min = 0.4 | W-max = 0.9
            w = 0.9 - 0.4 * M / M_max
        # Update the iteration counter
        M += 1

        # show new best position on plot
    print(global_best_position, global_best_value)
    #append to csv file best result:
    f = open("PSO_"+str(function.__name__)+".csv", "a")
    f.write(str(function.__name__) + ";" + str(global_best_value) + "\n")
    plt.close()
    #plt.show()

for i in range(30):
    PSO_inertia_weight(30, 2, 2, 30, functions.Sphere)
    PSO_inertia_weight(30, 2, 2, 30, functions.Zakharov)
    PSO_inertia_weight(30, 2, 2, 30, functions.Rosenbrock)
    PSO_inertia_weight(30, 2, 2, 30, functions.Ackley)
    PSO_inertia_weight(30, 2, 2, 30, functions.Schwefel)
    PSO_inertia_weight(30, 2, 2, 30, functions.Rastrigin)
    PSO_inertia_weight(30, 2, 2, 30, functions.Griewank)
    PSO_inertia_weight(30, 2, 2, 30, functions.Levy)
    PSO_inertia_weight(30, 2, 2, 30, functions.Michalewicz)
