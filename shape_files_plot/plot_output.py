import shapefile as shp
from pprint import pprint
from matplotlib.figure import Figure
# from random import uniform
from matplotlib.path import Path
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import sys
sys.path.append('../')
from parse_output.parse_output import get_vals, parse_output

p = "./Subbasins116.shp"
output_sub = "../parse_output/output.sub"


def main():
    col_name = 'PETmm'
    subbasins = parse_output(output_sub)
    vals = get_vals(col_name, subbasins, day=5)
    # pprint(vals)
    plot_output(vals, col_name)


def plot_output(values, col_name):
    # read shape file
    sf = shp.Reader(p)
    shapes = sf.shapes()
    # get subbasins names
    # sub_names = names = [el.record[22][:-4] for el in sf.shapeRecords()]
    # print("Num of shapes: ", len(shapes))
    # create fig and axes
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.set_title(col_name)
    fig.canvas.set_window_title('Visualization')
    # random colors list. leave it just for tests
    # colors_rgb = []
    # for _ in range(116):
    #   rgb = uniform(0, 1), uniform(0, 1), uniform(0, 1)
    #   colors_rgb.append(rgb)
    # ploting and addit to pols and colors return of plotting
    pols = []
    colors_cm = []
    diff = max(values) - min(values)
    norm_values = [(val - min(values)) / diff for val in values]
    for shape, val in zip(shapes, norm_values):
        points = shape.points
        x = [el[0] for el in points]
        y = [el[1] for el in points]
        color_val = 1 - val
        rgb = color_val, color_val, 0.9
        colors_cm.append(rgb)
        # just fill with color polygin
        ax.fill(x, y, color=rgb)
        # plot a line thet defines polygin
        ax.plot(x, y, color='r', linewidth=0.75)
        path_inp = [[xi, yi] for xi, yi in zip(x, y)]
        pols.append(path_inp)
    # create pathes objects to recognize subbasins
    pathes = [Path(el) for el in pols]
    # sub_names = names = [el.record[22][:-4] for el in sf.shapeRecords()]

    # creating my own colobar
    colors_cm = sort_colors(colors_cm)
    mycmp = mcolors.LinearSegmentedColormap.from_list(name='custom',
        colors=colors_cm, N=10)

    # setting my own colorbar
    normalize = mcolors.Normalize(vmin=min(values), vmax=max(values))
    scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=mycmp)
    scalarmappaple.set_array(values)
    plt.colorbar(scalarmappaple)    
    # set up annotation around the curosr
    annot = ax.annotate("", xy=(350000, 5800000),
        bbox=dict(boxstyle="round", fc="w"))
    annot.set_visible(False)

    # add on mouse move callback function to the figure
    fig.canvas.mpl_connect("motion_notify_event",
        lambda event: hover(event, annot, fig, ax, pathes, values))

    # plt.show()


def hover(event, annot, fig, ax, pathes, values):
    if event.inaxes == ax:
        # take position of cursor
        x, y = round(event.xdata, 1), round(event.ydata, 1)
        # text = str(x) + " " + str(y)
        text = ''
        # set position of annot
        annot.set_position((x + 5000, y + 5000))
        annot.set_visible(True)
        # index of coorect subbasin number under the curosr
        index = 0
        for path, i in zip(pathes, range(1, 117)):
            # find the number ofsubbasin under the mouse
            if path.contains_point([x, y]):
                text += str(i)
                index = pathes.index(path)
        annot.set_text(text + ": " + str(values[index]))
        # redraw graf to change annotation positiion. :(
        fig.canvas.draw_idle()


def sort_colors(colors):
    # super hard to understand function that sort sort colors
    # for my own colorbar
    d = {k: v for k, v in zip(colors, range(len(colors)))}
    d_sums = {sum(k): v for k, v in d.items()}
    sorted_sums = list(d_sums.keys())
    sorted_sums = sorted(sorted_sums)
    good_order = [d_sums[el] for el in sorted_sums]
    ret = []
    d_reversed = {v: k for k, v in d.items()}
    for ind in good_order:
        ret.append(d_reversed[ind])
    return ret[::-1]


if __name__ == '__main__':
    main()

# 62, 77, 22, 50 , 113 - numbers subbasins with incorrect
# order of points  in polygons - ????
