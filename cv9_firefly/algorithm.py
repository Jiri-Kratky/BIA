import defined_functions as functions
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter

def draw_fireflies(function,writer,axis,x1,x2,results,fireflies,light_intensity):
    axis.plot_surface(
    x1, x2, results, cmap='gray',alpha=0.5
            )

    for i in range(len(fireflies)):
        axis.scatter(
        fireflies[i][0],
        fireflies[i][1],
        light_intensity[i],
        color="yellow",
        marker="o",
        s=30,
        )

    axis.set_xlabel("Best individual: ")
    axis.set_ylabel(str(min(light_intensity)))
    axis.set_zlabel("")
    axis.set_title(function.__name__)



def firefly_algorithm(function: functions.Function, num_fireflies=40, max_generations=100, alpha=0.5, beta0=1.0):
    """
    Implements the Firefly Algorithm for optimization problems.

    Parameters:
    objective_function (function): The objective function to be minimized.
    num_fireflies (int): The number of fireflies in the swarm.
    max_generations (int): The maximum number of generations to run the algorithm.
    alpha (float): The attractiveness parameter.
    beta0 (float): The initial value of the light absorption coefficient.

    """

    # Initialize the fireflies randomly within the search space
    fireflies = np.random.uniform(low=function.min, high=function.max, size=(num_fireflies, 2))
    light_intensity = np.zeros(num_fireflies)

    # Evaluate the initial light intensity of each firefly
    for i in range(num_fireflies):
        light_intensity[i] = function.execute(fireflies[i][0], fireflies[i][1])     # evaluate new position (her light intensity)
#animation:
    plt.rcParams[
        "animation.ffmpeg_path"
    ] = "C:\\Users\\jirka\\Desktop\\BIA\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe"

    metadata = dict(title="Functions", artist="KRA0601")
    writer = FFMpegWriter(fps=15, metadata=metadata)

    fig, axis = plt.subplots(subplot_kw=dict(projection="3d"))

    plt.xlim(function.min)
    plt.ylim(function.max)

    x1 = np.linspace(function.min, function.max)
    x2 = np.linspace(function.min, function.max)

    x1,x2 = np.meshgrid(x1, x2)

    results = function.execute(x1, x2)

    with writer.saving(fig, "animation_Michalewicz_Firefly.mp4", 100):

        #draw_fireflies(function,writer,axis,x1,x2,results,fireflies,light_intensity)
        #writer.grab_frame()
        #plt.cla()
        for generation in range(max_generations):
            for i in range(num_fireflies):        # Update the light intensity of each firefly
                for j in range(num_fireflies):
                    if light_intensity[j] < light_intensity[i]:  
                        r = np.linalg.norm(fireflies[i] - fireflies[j])                     # distance between fireflies (euclidean distance)
                        beta = beta0 / (1+r)
                        fireflies[i] += alpha * beta * (fireflies[j] - fireflies[i])        # move towards brighter fireflies
                        fireflies[i] = np.clip(fireflies[i], function.min, function.max)    # clip to search space
                        light_intensity[i] = function.execute(fireflies[i][0], fireflies[i][1]) # evaluate new position

                #draw_fireflies(function,writer,axis,x1,x2,results,fireflies,light_intensity)
                #writer.grab_frame()
                #plt.cla()

    # Find the best solution
    best_idx = np.argmin(light_intensity)   # index of the best solution (lowest light intensity)
    best_solution = fireflies[best_idx]
    best_fitness = light_intensity[best_idx]

    print("Firefly algorithm: {0}".format(best_fitness))
    f = open("Firefly_"+str(function.__name__)+".csv", "a")
    f.write(str(function.__name__) + ";" + str(light_intensity[best_idx]) + "\n")
    plt.close()


for i in range(30):
    firefly_algorithm(functions.Sphere, 30, 30, 0.5, 1.0)
    firefly_algorithm(functions.Zakharov, 30, 30, 0.5, 1.0)
    firefly_algorithm(functions.Rosenbrock, 30, 30, 0.5, 1.0)
    firefly_algorithm(functions.Ackley, 30, 30, 0.5, 1.0)
    firefly_algorithm(functions.Schwefel, 30, 30, 0.5, 1.0)
    firefly_algorithm(functions.Rastrigin, 30, 30, 0.5, 1.0)
    firefly_algorithm(functions.Griewank, 30, 30, 0.5, 1.0)
    firefly_algorithm(functions.Levy, 30, 30, 0.5, 1.0)
    firefly_algorithm(functions.Michalewicz, 30, 30, 0.5, 1.0)
