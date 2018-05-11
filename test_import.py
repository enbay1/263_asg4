import random
import sys
import csv
from operator import itemgetter
import matplotlib.pyplot as plt

from BME163_Custom_Plots_McCreath_Benjamin import swarm_plot, subsample, construct_data, load_data

# This code imports and runs the swarm_plot function.
# swarm_plot takes the following parameters:
#swarm_plot(panel=panel,
#                       y_values=list_of_y_values,  a 1 dim list of the desired Y values
#                       x_position=x_position,      the 'bin' being plotted. It better be in your xrange
#                       panel_width=panel_width,    the panel width of the panel being passed in
#                       panel_height=panel_height,  the panel height of the panel being passed in
#                       xmin=xmin,                  the minimum x value of the panel
#                       xmax=xmax,                  the maximum x value of the panel
#                       ymin=ymin,                  the mimimum y value of the panel
#                       ymax=ymax,                  the maximum y value of the panel
#                       plot_width=.4,              how wide each bin is.
#                       minimum_distance=1 / 125,   how much buffer space there is between points.
#                       shift=0.005,                how far to move each iteration
#                       size=0.5,                   the size of the points to be plotted
#                       color='black')              color or colors of points to be plotted


def main():
    """Drive the import, construction, subsample, median generation, panel configuration, and swarm generation."""
    data = list(map(list, [construct_data(datum) for datum in load_data()]))
    data.sort(key=itemgetter(1))
    data.sort(key=itemgetter(0))
    # Subsample requires the data to be sorted to get 1K from each bin easily, but returns an unsorted version.
    # So it's easiest just to sort the data again after subsampling.
    data = subsample(data)
    list_of_y_values = [datum[1] for datum in data if datum[0] == 1]
    # Set the stylesheet
    plt.style.use('BME163.mplstyle')
    # Set the figure size, make the axes, and set axes properties
    plt.figure(figsize=(7, 3))
    panel = plt.axes([0.7 / 7, 0.6 / 3, 5 / 7, 2 / 3])
    panel.set(xlim=(0.5, 11.5), xticks=list(range(1, 12)), xticklabels=list(range(1, 11)) + ['>10'],
              xlabel="Subread coverage", ylabel="Identity (%)", ylim=(75, 100), yticklabels=list(range(75, 105, 5)))
    x_position = 1
    panel_width = 5
    panel_height = 2
    xmin = 0.5
    xmax = 11.5
    ymin = 75
    ymax = 100
    panel = swarm_plot(panel=panel,
                       y_values=list_of_y_values,
                       x_position=x_position,
                       panel_width=panel_width,
                       panel_height=panel_height,
                       xmin=xmin,
                       xmax=xmax,
                       ymin=ymin,
                       ymax=ymax,
                       plot_width=.4,
                       minimum_distance=1 / 125,
                       shift=0.005,
                       size=0.5,
                       color='black')
    # save the figure.
    plt.savefig('McCreath_Benjamin_BME263_Week4.5.png', dpi=600)


if __name__ == "__main__":
    main()
