import defined_functions as functions
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter


class Program:
    def __init__(
        self, function, algorithm
    ):  # function - funkce (sphere atd) | algorithm (blind search)
        self.function = function
        self.algorithm = algorithm

        self.algorithm.min = self.function.min
        self.algorithm.max = self.function.max

    def executeAnimation(self, counter):  # counter - počet projetí algoritmem
        if counter > 0:
            x = self.algorithm.execute()
            y = self.algorithm.execute()
            counter -= 1
            self.minValueX = x
            self.minValueY = y
            self.minimalValue = self.function.execute(x, y)

            plt.rcParams[
                "animation.ffmpeg_path"
            ] = "C:\\Users\\jirka\\Desktop\\BIA\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe"

            metadata = dict(title="Functions", artist="KRA0601")
            self.writer = FFMpegWriter(fps=15, metadata=metadata)

            self.fig, self.axis = plt.subplots(subplot_kw=dict(projection="3d"))

            plt.xlim(self.function.min)
            plt.ylim(self.function.max)

            self.x1 = np.linspace(self.function.min, self.function.max)
            self.x2 = np.linspace(self.function.min, self.function.max)

            self.x1, self.x2 = np.meshgrid(self.x1, self.x2)

            self.results = self.function.execute(self.x1, self.x2)

            with self.writer.saving(self.fig, "animation.mp4", 100):
                while counter > 0:
                    x = self.algorithm.execute()
                    y = self.algorithm.execute()
                    newmin = self.function.execute(x, y)
                    # print(newmin)
                    if newmin < self.minimalValue:
                        self.minimalValue = newmin
                        self.minValueX = x
                        self.minValueY = y

                    self.axis.plot_surface(
                        self.x1, self.x2, self.results, cmap=cm.coolwarm
                    )
                    self.axis.scatter(
                        self.minValueX,
                        self.minValueY,
                        self.minimalValue,
                        color="red",
                        marker="o",
                        s=50,
                    )
                    self.axis.set_xlabel("X")
                    self.axis.set_ylabel("Y")
                    self.axis.set_zlabel("Z")
                    self.writer.grab_frame()
                    plt.cla()
                    counter -= 1
                    print("Current minimum: " + str(self.minimalValue))
                    print("Iterations left: " + str(counter))
                print("konec")

    def draw(self, x, y, z):
        self.axis.scatter(
            x,
            y,
            z,
            color="red",
            marker="o",
            s=100,
        )

    def execute(self, counter):  # counter - počet projetí algoritmem
        self.x1 = np.linspace(self.function.min, self.function.max)
        self.x2 = np.linspace(self.function.min, self.function.max)

        self.x1, self.x2 = np.meshgrid(self.x1, self.x2)

        results = self.function.execute(self.x1, self.x2)

        figure = plt.figure()
        self.axis = figure.add_subplot(projection="3d")
        self.axis.plot_surface(self.x1, self.x2, results, cmap=cm.coolwarm)
        self.axis.set_xlabel("X")
        self.axis.set_ylabel("Y")
        self.axis.set_zlabel("Z")

        if counter > 0:
            x = self.algorithm.execute()
            y = self.algorithm.execute()
            counter -= 1

            self.minimalValue = self.function.execute(x, y)
            self.minValueX = x
            self.minValueY = y

            while counter > 0:
                x = self.algorithm.execute()
                y = self.algorithm.execute()
                newmin = self.function.execute(x, y)

                if newmin < self.minimalValue:
                    self.minimalValue = newmin
                    self.minValueX = x
                    self.minValueY = y

                counter -= 1

            self.draw(self.minValueX, self.minValueY, self.minimalValue)
            plt.show()
