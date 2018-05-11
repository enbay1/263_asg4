import csv
import math
import os
import random
import statistics
import sys
from operator import itemgetter

import matplotlib.patches as mplpatches
import matplotlib.pyplot as plt


# done
def load_data() -> list:
    """Load data from supplied sequence file."""
    # Try to open the file, if it opens read it into 'data' delimited by tabs
    try:
        with open(sys.argv[1], 'r') as file_in:
            data = list(csv.reader(file_in, delimiter='\t'))
        return data
    # When someone misspells the filename or is in the wrong working directory, give a pleasant error message.
    except (FileNotFoundError, IndexError) as e:
        if type(e) is FileNotFoundError:
            trans_table = str.maketrans("'\"", "  ", "'\"")
            sys.stderr.write("File '{}' not found.".format(sys.argv[1].translate(trans_table).strip()))
        elif type(e) is IndexError:
            sys.stderr.write("Usage: {} input_file\n\tinput_file: The file of special format defined by the "
                             "assignment.".format(os.path.basename(__file__)))
        else:
            sys.stderr.write("Unexpected error.")
        sys.exit(1)


# done
def construct_data(datum: list) -> (int, float):
    """Manipulate loaded data into correct order and format."""
    # The bin and quality value are stuck in datum[0] as a string
    datum[0] = datum[0].split('_')
    # All the desired indices are known, so grab them. Also, if the number is greater than 10 assign it bin 11.
    return int(datum[0][3]) if int(datum[0][3]) <= 10 else 11, float(datum[1]), float(datum[0][1])


# done
def fill_color_scale(scale: plt.axes) -> None:
    """Generate and populate color scale for quality on right of figure."""
    # Scale range for normalizing data.
    scale_range = scale.get_ylim()[1] - scale.get_ylim()[0]
    # 255 steps because I like 8 bit RBG values.
    for i in range(255):
        # get the RBG vaules from blue to yellow
        R, G, B = 255 - i, 255 - i, 0 + i
        # Plot the patch in the scale
        scale.add_patch(
            mplpatches.Rectangle((0, (7 + ((i / 255) * scale_range))), 1, scale_range / 255,
                                 facecolor=(R / 255, G / 255, B / 255)))
    return


# done
def subsample(data: list) -> list:
    """Sample 1000 points from each of the x axis bins."""
    current_bin = 1
    i = 0
    data_to_return = []
    # loop over bins 1 to 11, as that are the possible X values.
    while current_bin <= 11:
        j = i + 1
        # While in a bin, search for the end of the bin
        while data[j][0] == current_bin and j < len(data) - 1:
            j += 1
        # Sample K random points in the bin
        data_to_return += random.sample(data[i:j], k=1000)
        # Update index to ahead of the most recently subsampled bin
        i = j
        # Update to the next bin
        current_bin += 1
    return data_to_return


# done
def get_medians(data: list) -> list:
    """Calculate median for each x axis bin in the data."""
    # This function loops over the bins like the subsample function does.
    medians = []
    current_bin = 1
    i = 0
    # while all the bins have not been visited
    while current_bin <= 11:
        j = i + 1
        # find the end of the bin
        while data[j][0] == current_bin and j < len(data) - 1:
            j += 1
            # Get the mean from the start of the bin to the end of the bin
        medians.append([current_bin, statistics.median([value[1] for value in data[i:j]])])
        # update the running indices
        i = j
        current_bin += 1
    return medians


# done
def euclidean_distance(point_1: list, point_2: list, panel_width: float, panel_height: float, xrange: float,
                       yrange: float) -> float:
    """Calculate the euclidean distance between two points in a specifified panel size."""
    delta_x = (math.fabs(point_1[0] - point_2[0]) / xrange) * panel_width
    delta_y = (math.fabs(point_1[1] - point_2[1]) / yrange) * panel_height
    return math.sqrt(delta_x ** 2 + delta_y ** 2)


def swarm_helper(data: list, shift, min_dist, point_size, xmin, xmax, ymin, ymax, panel_width, panel_height) -> list:
    """For each bin generate x offsets such that data points do not touch."""
    # his dots are 6px
    # 1 data point = .072"
    # dot diameter = .14
    # One pixel = .002
    # Mine are 7px * .002"/px = .014/2 = .007 = radius
    point_radius = (((point_size + .1) * .002) + (min_dist))
    #point_radius = .009
    # negative is a bool that determines which way to move the point so the resulting swarm is balanced.
    negative = True
    for i, datum in enumerate(data):
        # Bear with me. This only compares the point with the 75 points closest to it. If the data is super dense
        # this won't work. However, the data bins are only .8 wide. Each point is .014. So, 75 points occupies 1.05
        # of space, which is wider than the allowed .8 bin width. So really, the 75 point comparison is not the
        # limiting factor here. This isn't perfect, but it is fast!
        compare = data[i - 75:i]
        # generates distances to all close points to determine if moving the point is required.
        distances = []
        for point in compare:
            distances.append(euclidean_distance([datum[0], datum[1]], [point[0], point[1]], panel_width,
                                                panel_height, (xmax - xmin), (ymax - ymin)))
        # if moving the point is required, this moves it a tiny bit -/+ and recalculates until it satisfies the
        # distance requirement.
        while any(distance <= point_radius for distance in distances):
            datum[0] += shift * (-1) ** negative
            distances = []
            for point in compare:
                distances.append(euclidean_distance([datum[0], datum[1]], [point[0], point[1]], panel_width,
                                                    panel_height, xmax - xmin, ymax - ymin))
        # if the point moved negatively make negative false, if point move positively make negative true.
        negative = not round(datum[0]) > datum[0]
    return data


def generate_swarm_data(data: list,shift, min_dist, point_size, xmin, xmax, ymin, ymax, panel_width, panel_height) -> list:
    """Split data into bins and pass along to the swarm_helper function."""
    swarm_data = []
    current_bin = 1
    i = 0
    # loops over the data by bin, then ships it off in chunks to the function that moves poitns left/right.
    while current_bin <= 11:
        j = i + 1
        while data[j][0] == current_bin and j < len(data) - 1:
            j += 1
        # Safe zone
        swarm_data += swarm_helper(data[i:j], shift, min_dist, point_size, xmin,xmax,ymin,ymax,panel_width,panel_height)
        # End safe zone
        i = j
        current_bin += 1
    return swarm_data


def generate_colors(data: list, color_scale: plt.axes) -> list:
    """Generate a colors array from the quality scores to match the color scale."""
    # Grab the colors from the color plot
    colors = [patch.get_facecolor() for patch in color_scale.patches]
    # Define the data range
    data_range = color_scale.get_ylim()[1] - color_scale.get_ylim()[0]
    # Loop over the data
    for i, datum in enumerate(data):
        # if under the minimum score, set to minimum color
        if datum[2] <= 7:
            datum[2] = colors[0]
        # if data above maximum color, set to maximum color
        elif datum[2] >= 15:
            datum[2] = colors[-1]
        # if a color in range link it to the proper color from the color list.
        else:
            color_proportion = (datum[2] - 7) / data_range
            color_proportion_in_255_space = int(round(color_proportion * 255)) - 1
            datum[2] = colors[color_proportion_in_255_space]
    return data


# swarm_plot(panel,list_of_y_values,x_position,panel_width,panel_height,xmin,xmax,ymin,ymax,0.5,1/125,0.005,0.5,'black')
def swarm_plot(panel: plt.axes,
               y_values: list,
               x_position: int or float,
               panel_width: int or float = None,
               panel_height: int or float = None,
               xmin: int or float = None,
               xmax: int or float = None,
               ymin: int or float = None,
               ymax: int or float = None,
               plot_width: int or float = None,
               minimum_distance: float = None,
               shift: float = None,
               size: float = None,
               color: list or str or tuple = None) -> plt.axes:
    if type(color) is list:
        if len(color) is 1:
            if type(color[0]) is list:
                color = [tuple(color[0])] * len(y_values)
            elif type(color[0]) is str:
                color = [color[0]] * len(y_values)
            elif type(color[0]) is tuple:
                color = [color[0]] * len(y_values)
        if len(color) is 3:
            color = [tuple(color)] * len(y_values)
        elif len(color) is len(y_values):
            pass
        else:
            sys.stderr.write("Colors are not of correct format. Printing points in black. Param 'color' should be of "
                             "type list<str>, list<list>, or list<tuple> and match length of y_values. Else, "
                             "one value should be passed as the color for all points.")
            sys.exit(1)
    elif type(color) is str:
        color = [color] * len(y_values)
    elif type(color) is tuple:
        color = [color] * len(y_values)
    else:
        sys.stderr.write(
            "{} type for paramater 'color' is not valid. Please use a list<str> or list<rgb tuple> of colors, "
            "one for each Y value, or a single "
            "color in string or tuple format('black', '(1,1,1)').".format(str(type(color))))
        sys.exit(1)
    y_values.sort()
    data = [[x_position, y_value] for y_value in y_values]
    for i, datum in enumerate(data):
        datum.append(color[i])
    median = statistics.median([y[1] for y in data])
    swarm_data = swarm_helper(data, shift, minimum_distance, size, xmin, xmax, ymin, ymax, panel_width, panel_height)
    panel.scatter([x[0] for x in swarm_data], [y[1] for y in swarm_data],
                  c=[z[2] for z in swarm_data], s=float(math.sqrt(size)), linewidths=0)
    panel.plot([x_position - plot_width, x_position + plot_width], [median, median], linewidth=.7, color='red')
    return panel


def main():
    """Drive the import, construction, subsample, median generation, panel configuration, and swarm generation."""
    # load data and construct shit
    data = list(map(list, [construct_data(datum) for datum in load_data()]))
    data.sort(key=itemgetter(1))
    data.sort(key=itemgetter(0))
    # Subsample requires the data to be sorted to get 1K from each bin easily, but returns an unsorted version.
    # So it's easiest just to sort the data again after subsampling.
    data = subsample(data)
    data.sort(key=itemgetter(1))
    data.sort(key=itemgetter(0))
    # Grab all the medians from the data.
    medians = get_medians(data)
    # Set the stylesheet
    plt.style.use('BME163.mplstyle')
    # Set the figure size, make the axes, and set axes properties
    plt.figure(figsize=(7, 3))
    panel = plt.axes([0.7 / 7, 0.6 / 3, 5 / 7, 2 / 3])
    panel.set(xlim=(0.5, 11.5), xticks=list(range(1, 12)), xticklabels=list(range(1, 11)) + ['>10'],
              xlabel="Subread coverage", ylabel="Identity (%)", ylim=(75, 100), yticklabels=list(range(75, 105, 5)))
    scale = plt.axes([6.3 / 7, 0.6 / 3, 0.2 / 7, 2 / 3])
    # Generate the side panel with color gradient.
    scale.set(xlim=(0, 1), ylim=(7, 15), xticks=[], ylabel="Read quality (Q)")
    scale.set_yticklabels(['<7'] + list(range(8, 15)) + ['>15'])
    fill_color_scale(scale)
    panel.plot([0.055, 11.5], [95, 95], dashes=[4, 8, 8, 8], linewidth=.5, color='black')
    # Plot medians.
    for median in medians:
        panel.plot([median[0] - 0.4, median[0] + 0.4], [median[1], median[1]], linewidth=.7, color='red')
    # Generate the swarm data
    plottable_swarm_data = generate_swarm_data(data=data, shift=.005,min_dist=.001,point_size=.4,xmin=.05,xmax=11.5,
                                               ymin=75,ymax=100,panel_width=5,panel_height=2)
    # Generate the colors for the data
    colored_and_plottable_data = generate_colors(plottable_swarm_data, scale)
    # plot the data
    panel.scatter([x[0] for x in colored_and_plottable_data], [y[1] for y in colored_and_plottable_data],
                  c=[z[2] for z in colored_and_plottable_data], s=0.4, linewidths=0)
    # save the figure.
    plt.savefig('McCreath_Benjamin_BME263_Week4.png', dpi=600)


if __name__ == "__main__":
    main()
