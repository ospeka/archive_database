import shapefile as shp
from pprint import pprint
import matplotlib.pyplot as plt
from random import uniform
from matplotlib.path import Path
import matplotlib.colors as mcolors
import matplotlib.cm as cm

p = "./Subbasins116.shp"

def main():
	sf = shp.Reader(p)
	shapes = sf.shapes()
	sub_names = names = [el.record[22][:-4] for el in sf.shapeRecords()]
	print("Num of shapes: ", len(shapes))
	
	fig, ax = plt.subplots(1,1)
	colors_rgb = []
	for _ in range(116):
		rgb = uniform(0, 1), uniform(0, 1), uniform(0, 1)
		colors_rgb.append(rgb)
	
	pols = []
	vals = [round(uniform(0, 1), 3) for _ in range(len(sub_names))]
	colors_cm = []

	for shape, color, val in zip(shapes, colors_rgb, vals):
		points = shape.points
		x = [el[0] for el in points]
		y = [el[1] for el in points]
		color_val = 1 - val 
		rgb = color_val, color_val, 0.9
		colors_cm.append(rgb)
		ax.fill(x, y, color=rgb)
		# ax.plot(x, y, color='r', linewidth=0.75)
		path_inp = [[xi, yi] for xi, yi in zip(x,y)]
		pols.append(path_inp)
	pathes = [Path(el) for el in pols]
	sub_names = names = [el.record[22][:-4] for el in sf.shapeRecords()]

	colors_cm = sort_colors(colors_cm)
	mycmp = mcolors.LinearSegmentedColormap.from_list(name='custom',
		colors=colors_cm, N=10)


	normalize = mcolors.Normalize(vmin=min(vals), vmax=max(vals))
	scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=mycmp)
	scalarmappaple.set_array(vals)
	plt.colorbar(scalarmappaple)
	
	annot = ax.annotate("111", xy=(350000, 5800000), 
		bbox=dict(boxstyle="round", fc="w"))
	annot.set_visible(False)

	fig.canvas.mpl_connect("motion_notify_event",
		lambda event: hover(event, annot, fig, ax, pathes, sub_names, vals))

	plt.show()

def hover(event, annot, fig, ax, pathes, sub_names, vals):
	if event.inaxes == ax:
		x, y = round(event.xdata, 1), round(event.ydata, 1)
		# text = str(x) + " " + str(y)
		text = ''
		annot.set_position((x + 5000, y + 5000))
		annot.set_visible(True)
		index = 0
		for path, name, i in zip(pathes, sub_names, range(116)):
			if path.contains_point([x, y]):
				text += " " + str(name) + " " + str(i)
				index = pathes.index(path)
		annot.set_text(text + ": " + str(vals[index]))
		fig.canvas.draw_idle()

def sort_colors(colors):
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

# add colorbar legend
# 62, 77, 22, 50 , 113
# Лучше просто номер суббасейна. Не надо название станции



























