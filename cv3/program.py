import defined_functions as functions
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter


class Program:
    def __init__(
        self, algorithm
    ):  # function - funkce (sphere atd) | algorithm (blind search)
        self.algorithm = algorithm

    def executeAnimation(self, counter):  # counter - počet projetí algoritmem
        self.algorithm.executeAnimation(counter)

    def execute(self, counter):  # counter - počet projetí algoritmem
        self.algorithm.execute(counter)
