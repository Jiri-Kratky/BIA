import matplotlib.pyplot as plt
import numpy as np
from numpy import *
import defined_functions as defined
from matplotlib import cm
from numpy import meshgrid
from mpl_toolkits.mplot3d import Axes3D
import program as pr
import defined_functions as functions
import algorithm as algorithm

# functions - Sphere, Schwefel, Ackley, Rastrigin, Rosenbrock, Griewank, Zakharov, Levy, Michalewicz
test = pr.Program(functions.Sphere, algorithm.BlindSearch())

test.execute(50)  # number of iterations (50)

test.executeAnimation(100)  # saves animation to animation.mp4
