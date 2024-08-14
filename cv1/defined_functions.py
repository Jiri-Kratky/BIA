import matplotlib.pyplot as plt
import numpy as np
from numpy import *
from numpy import meshgrid
from mpl_toolkits.mplot3d import Axes3D
import math


class Function:
    def __init__(self) -> None:
        pass

    def execute():
        pass


class Sphere(Function):
    min = -5.12
    max = 5.12

    def execute(x1, x2):
        return x1**2 + x2**2


class Schwefel(Function):
    min = -500
    max = 500

    def execute(x1, x2):
        return 418.9829 * 2 - x1 * sin(sqrt(abs(x1))) - x2 * sin(sqrt(abs(x2)))


class Ackley(Function):
    min = -32.768
    max = 32.768

    def execute(x1, x2):
        return (
            -20 * exp(-0.2 * sqrt(0.5 * (x1**2 + x2**2)))
            - exp(0.5 * (cos(2 * pi * x1) + cos(2 * pi * x2)))
            + exp(1)
            + 20
        )


class Rastrigin(Function):
    min = -5.12
    max = 5.12

    def execute(x1, x2):
        return 20 + x1**2 - 10 * cos(2 * pi * x1) + x2**2 - 10 * cos(2 * pi * x2)


class Rosenbrock(Function):
    min = -5
    max = 10

    def execute(x1, x2):
        return (1 - x1) ** 2 + 100 * (x2 - x1**2) ** 2


class Griewank(Function):
    min = -600
    max = 600

    def execute(x1, x2):
        return (x1**2 + x2**2) / 4000 - cos(x1) * cos(x2 / sqrt(2)) + 1


class Levy(Function):
    min = -10
    max = 10

    def execute(x1, x2):
        return (
            sin(3 * pi * x1) ** 2
            + (x1 - 1) ** 2 * (1 + sin(3 * pi * x2) ** 2)
            + (x2 - 1) ** 2 * (1 + sin(2 * pi * x2) ** 2)
        )


class Michalewicz(Function):
    min = 0
    max = math.pi

    def execute(x1, x2):
        return (
            -sin(x1) * sin(x1**2 / pi) ** 20 - sin(x2) * sin(2 * x2**2 / pi) ** 20
        )


class Zakharov(Function):
    min = -5
    max = 10

    def execute(x1, x2):
        return x1**2 + x2**2 + (x1 + x2) ** 2 + (x1 + x2) ** 4
