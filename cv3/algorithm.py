import math
import random
import defined_functions as functions
import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter

class Algorithm:
    def __init__(self,function):
        self.function = function
        pass

    def execute(count):
        pass

    def executeAnimation(count):
        pass

    def draw(self, x, y, z,color):
        self.axis.scatter(
            x,
            y,
            z,
            color=color,
            marker="o",
            s=30,
        )

    def generateSublot(self):
        plt.rcParams[
            "animation.ffmpeg_path"
        ] = "C:\\Users\\jirka\\Desktop\\BIA\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe"

        metadata = dict(title="Functions", artist="KRA0601")
        self.writer = FFMpegWriter(fps=15, metadata=metadata)

        self.fig, self.axis = plt.subplots(subplot_kw=dict(projection="3d"))

        plt.xlim(self.function.min)
        plt.ylim(self.function.max)

#############################################################################################################        
#############################################################################################################   
#############################################################################################################

class BlindSearch(Algorithm):
    def __init__(self,function):
        self.function = function
        self.min = function.min
        self.max = function.max

    def executeAnimation(self, counter):  # counter - počet projetí algoritmem
        if counter > 0:
            x = random.uniform(self.min, self.max)
            y = random.uniform(self.min, self.max)
            counter -= 1
            self.minValueX = x
            self.minValueY = y
            self.minimalValue = self.function.execute(x, y)

            self.generateSublot()
            self.draw(self.minValueX, self.minValueY, self.minimalValue,"red")

            self.x1 = np.linspace(self.function.min, self.function.max)
            self.x2 = np.linspace(self.function.min, self.function.max)

            self.x1, self.x2 = np.meshgrid(self.x1, self.x2)

            self.results = self.function.execute(self.x1, self.x2)

            with self.writer.saving(self.fig, "animation.mp4", 100):
                while counter > 0:
                    x = random.uniform(self.min, self.max)
                    y = random.uniform(self.min, self.max)
                    newmin = self.function.execute(x, y)
                    if newmin < self.minimalValue:
                        self.minimalValue = newmin
                        self.minValueX = x
                        self.minValueY = y

                    #whole function
                    self.axis.plot_surface(
                        self.x1, self.x2, self.results, cmap=cm.coolwarm,alpha=0.5
                    )
                    self.draw(self.minValueX, self.minValueY, self.minimalValue,"red")

                    self.axis.set_xlabel("X")
                    self.axis.set_ylabel("Y")
                    self.axis.set_zlabel("Z")
                    self.axis.set_title(self.function.__name__)
                    self.writer.grab_frame()
                    plt.cla()
                    counter -= 1
                    print("Current minimum: " + str(self.minimalValue))
                    print("Iterations left: " + str(counter))
                print("konec")

    def execute(self, counter):  # counter - počet projetí algoritmem
        self.x1 = np.linspace(self.function.min, self.function.max)
        self.x2 = np.linspace(self.function.min, self.function.max)

        self.x1, self.x2 = np.meshgrid(self.x1, self.x2)

        results = self.function.execute(self.x1, self.x2)

        figure = plt.figure()
        self.axis = figure.add_subplot(projection="3d")
        self.axis.plot_surface(self.x1, self.x2, results, cmap=cm.coolwarm,alpha=0.5)
        self.axis.set_xlabel("X")
        self.axis.set_ylabel("Y")
        self.axis.set_zlabel("Z")
        self.axis.set_title(self.function.__name__)

        if counter > 0:
            x = random.uniform(self.min, self.max)
            y = random.uniform(self.min, self.max)
            counter -= 1

            self.minimalValue = self.function.execute(x, y)
            self.minValueX = x
            self.minValueY = y

            while counter > 0:
                x = random.uniform(self.min, self.max)
                y = random.uniform(self.min, self.max)
                newmin = self.function.execute(x, y)

                if newmin < self.minimalValue:
                    self.minimalValue = newmin
                    self.minValueX = x
                    self.minValueY = y

                counter -= 1

            self.draw(self.minValueX, self.minValueY, self.minimalValue,"red")
            plt.show()

#############################################################################################################        
#############################################################################################################   
#############################################################################################################

class HillClimbing(Algorithm):
    def __init__(self,function, neighbourSize): #stepSize - velikost kroku, neighbourSize - number of neighbours
        self.function = function
        self.stepSize = function.max/10     #stepSize = 10% of max value
        self.neighbourSize = neighbourSize
        self.min = function.min
        self.max = function.max
        self.minValueX = random.uniform(self.min, self.max)
        self.minValueY = random.uniform(self.min, self.max)
        self.localmin = function.execute(self.minValueX,self.minValueY)  #generate random point which is also the starting one


    def execute(self,counter):
        self.x1 = np.linspace(self.function.min, self.function.max)
        self.x2 = np.linspace(self.function.min, self.function.max)

        self.x1, self.x2 = np.meshgrid(self.x1, self.x2)

        results = self.function.execute(self.x1, self.x2)

        figure = plt.figure()
        self.axis = figure.add_subplot(projection="3d")
        self.axis.plot_surface(self.x1, self.x2, results, cmap=cm.coolwarm,alpha=0.5)

        self.axis.set_xlabel("X")
        self.axis.set_ylabel("Y")
        self.axis.set_zlabel("Z")
        self.axis.set_title(self.function.__name__)

        self.bestNeighbourX=self.minValueX
        self.bestNeighbourY=self.minValueY
        self.bestValueNeighbour=self.localmin

        if counter > 0:
            while counter > 0:
                for _ in range(self.neighbourSize):
                    self.x = self.minValueX + random.uniform(-self.stepSize, self.stepSize)
                    self.y = self.minValueY + random.uniform(-self.stepSize, self.stepSize)
                    newmin = self.function.execute(self.x, self.y)

                    if newmin < self.bestValueNeighbour:
                        self.bestNeighbourX = self.x
                        self.bestNeighbourY = self.y
                        self.bestValueNeighbour = newmin
                        print("New best neighbour with current counter("+str(counter)+")"+" and main Neighbour "+ str(self.localmin) +" is " + str(self.bestValueNeighbour))

                self.minValueX = self.bestNeighbourX
                self.minValueY = self.bestNeighbourY
                self.localmin = self.bestValueNeighbour
                counter -= 1
            
            self.draw(self.minValueX, self.minValueY, self.localmin,"red")
            plt.show()


    def executeAnimation(self, counter):  # counter - počet projetí algoritmem
        if counter > 0:
            self.x1 = np.linspace(self.function.min, self.function.max)
            self.x2 = np.linspace(self.function.min, self.function.max)

            self.x1, self.x2 = np.meshgrid(self.x1, self.x2)

            self.results = self.function.execute(self.x1, self.x2)

            self.x = self.minValueX + random.uniform(-self.stepSize, self.stepSize)
            self.y = self.minValueY + random.uniform(-self.stepSize, self.stepSize)
            newmin = self.function.execute(self.x, self.y)

            counter -= 1
            self.minValueX = self.x
            self.minValueY = self.y
            self.localmin = self.function.execute(self.x, self.y)

            self.bestNeighbourX=self.minValueX
            self.bestNeighbourY=self.minValueY
            self.bestValueNeighbour=self.localmin

            self.generateSublot()
            self.draw(self.minValueX, self.minValueY, self.localmin,"red")

            with self.writer.saving(self.fig, "animation.mp4", 100):
                while counter > 0:
                    #whole function
                    self.axis.plot_surface(
                        self.x1, self.x2, self.results, cmap=cm.coolwarm,alpha=0.5
                    )
                    self.draw(self.minValueX, self.minValueY, self.localmin,"red")  #draw current minimum

                    self.axis.set_xlabel("X")
                    self.axis.set_ylabel("Y")
                    self.axis.set_zlabel("Z")
                    self.axis.set_title(self.function.__name__)

                    for _ in range(self.neighbourSize):
                        self.x = self.minValueX + random.uniform(-self.stepSize, self.stepSize)
                        self.y = self.minValueY + random.uniform(-self.stepSize, self.stepSize)
                        newmin = self.function.execute(self.x, self.y)

                        self.draw(self.x, self.y, newmin,"gray")  #draw neighbour

                        if newmin < self.bestValueNeighbour:
                            self.bestNeighbourX = self.x
                            self.bestNeighbourY = self.y
                            self.bestValueNeighbour = newmin
                            print("New best neighbour with current counter("+str(counter)+")"+" and main Neighbour "+ str(self.localmin) +" is " + str(self.bestValueNeighbour))
                        self.writer.grab_frame()

                    self.minValueX = self.bestNeighbourX
                    self.minValueY = self.bestNeighbourY
                    self.localmin = self.bestValueNeighbour

                    plt.cla()
                    counter -= 1

                self.axis.plot_surface(
                        self.x1, self.x2, self.results, cmap=cm.coolwarm,alpha=0.5
                    )
                self.draw(self.minValueX, self.minValueY, self.localmin,"red")  #draw current minimum
                print(self.minValueX, self.minValueY, self.localmin)
                print("konec")


#############################################################################################################        
#############################################################################################################   
#############################################################################################################
   
class Annealing(Algorithm):
    def __init__(self,function: functions.Function, temp: int):
        self.function = function
        self.stepSize = function.max/8     #stepSize = 12,5% of max value
        self.min = function.min
        self.max = function.max
        self.temp = temp

    def execute(self,counter: int):
        if counter > 0:
            #generate initial point
            x = random.uniform(self.min, self.max)
            y = random.uniform(self.min, self.max)
            counter -= 1
            self.minValueX = x
            self.minValueY = y
            self.minimalValue = self.function.execute(x, y)

            self.x1 = np.linspace(self.function.min, self.function.max)
            self.x2 = np.linspace(self.function.min, self.function.max)

            self.x1, self.x2 = np.meshgrid(self.x1, self.x2)

            results = self.function.execute(self.x1, self.x2)

            figure = plt.figure()
            self.axis = figure.add_subplot(projection="3d")
            self.axis.plot_surface(self.x1, self.x2, results, cmap=cm.coolwarm,alpha=0.5)

            self.bestX = self.minValueX
            self.bestY = self.minValueY
            self.bestValue = self.minimalValue

            for i in range(counter-1):
                self.x = self.minValueX + random.uniform(-self.stepSize, self.stepSize)
                self.y = self.minValueY + random.uniform(-self.stepSize, self.stepSize)
                candidate_eval = self.function.execute(self.x, self.y)

                if candidate_eval < self.bestValue:
                    self.bestX=self.x
                    self.bestY=self.y
                    self.bestValue = candidate_eval

                # working with temperature
                difference = candidate_eval - self.minimalValue
                t = self.temp / float(i + 1)
                metropolis = math.exp(-difference / t)

                # check if we should keep the new point

                if difference < 0 or rand() < metropolis:
                    self.minValueX=self.x
                    self.minValueY=self.y
                    self.minimalValue=candidate_eval
                    #print('temperature changed')

            print('Done!')
            print('f(%0.5f %0.5f) = %f' % (self.bestX,self.bestY, self.bestValue))
            self.draw(self.bestX, self.bestY, self.bestValue,"red")
            plt.show()
    

    def executeAnimation(self, counter: int):  # counter - počet projetí algoritmem
        if counter > 0:
            self.generateSublot()
            self.x1 = np.linspace(self.function.min, self.function.max)
            self.x2 = np.linspace(self.function.min, self.function.max)

            self.x1, self.x2 = np.meshgrid(self.x1, self.x2)

            self.results = self.function.execute(self.x1, self.x2)

            #generate initial point
            x = random.uniform(self.min, self.max)
            y = random.uniform(self.min, self.max)
            counter -= 1
            self.minValueX = x
            self.minValueY = y
            self.minimalValue = self.function.execute(x, y)

            #set initial point as best
            self.bestX = self.minValueX
            self.bestY = self.minValueY
            self.bestValue = self.minimalValue

            self.draw(self.bestX, self.bestY, self.bestValue,"red")  #draw initial point

            print('1/'+str(counter+1))
            with self.writer.saving(self.fig, "animation.mp4", 100):
                for i in range(counter):
                    #whole function
                    self.axis.plot_surface(
                        self.x1, self.x2, self.results, cmap=cm.coolwarm,alpha=0.5
                    )
                    self.draw(self.bestX, self.bestY, self.bestValue,"red")  #draw current minimum

                    self.axis.set_xlabel("X")
                    self.axis.set_ylabel("Y")
                    self.axis.set_zlabel("Z")
                    self.axis.set_title(self.function.__name__)

                    self.x = self.minValueX + random.uniform(-self.stepSize, self.stepSize)
                    self.y = self.minValueY + random.uniform(-self.stepSize, self.stepSize)
                    candidate_eval = self.function.execute(self.x, self.y)

                    if candidate_eval < self.bestValue:
                        self.bestX=self.x
                        self.bestY=self.y
                        self.bestValue = candidate_eval
                        self.draw(self.bestX, self.bestY, self.bestValue,"grey")  #draw where i will be moving next

                    # working with temperature
                    difference = candidate_eval - self.minimalValue
                    t = self.temp / float(i + 1)
                    metropolis = math.exp(-difference / t)

                    # check if we should keep the new point
                    if difference < 0 or rand() < metropolis:
                        self.minValueX=self.x
                        self.minValueY=self.y
                        self.minimalValue=candidate_eval
                        #print('temperature changed')

                    self.writer.grab_frame()
                    print(str(i+2)+'/'+str(counter+1))
                    plt.cla()

                self.axis.plot_surface(
                        self.x1, self.x2, self.results, cmap=cm.coolwarm,alpha=0.5
                    )
                self.draw(self.bestX, self.bestY, self.bestValue,"red")  #draw current minimum
                print('Done!')
                print('f(%0.5f %0.5f) = %f' % (self.bestX,self.bestY, self.bestValue))