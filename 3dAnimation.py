import numpy as np
import matplotlib
import defined_functions as defined
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter, PillowWriter

plt.rcParams[
    "animation.ffmpeg_path"
] = "C:\\Users\\jirka\\Desktop\\BIA\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe"


metadata = dict(title="Movie", artist="codinglikemad")
# writer = PillowWriter(fps=15, metadata=metadata)
writer = FFMpegWriter(fps=15, metadata=metadata)

fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
plt.xlim(-5, 5)
plt.ylim(-5, 5)


def func(x, y, r, t):
    return np.cos(r / 2 + t) * np.exp(-np.square(r) / 50)


xvec = np.linspace(-10, 10, 1000)
yvec = np.linspace(-10, 10, 1000)

xlist, ylist = np.meshgrid(xvec, yvec)

rlist = np.sqrt(np.square(xlist) + np.square(ylist))

with writer.saving(fig, "exp3d.mp4", 100):
    for tval in np.linspace(0, 20, 160):
        zval = func(xlist, ylist, rlist, tval)
        ax.set_zlim(-1, 1)
        ax.plot_surface(xlist, ylist, zval, cmap=cm.viridis)

        writer.grab_frame()
        plt.cla()
