from random import random

from bokeh.io import show
from bokeh.plotting import figure

# create a figure with no toolbar and axis ranges from 0 to 1
p = figure(toolbar_location=None, x_range=(0, 1), y_range=(0, 1))

# generate 150 random circles with random x and y coordinates,
# random radii between 0.1 and 0.3, and random colors
for i in range(150):
    x, y = random(), random()
    p.circle(x, y, radius=random() * 0.2 + 0.1, color=(random(), random(), random()))

# show the figure
show(p)