import shapefile as shp
from pprint import pprint
import matplotlib.pyplot as plt
from random import uniform

p = "./Subbasins116.shp"

def main():
	sf = shp.Reader(p)
	shapes = sf.shapes()
	print("Num of shapes: ", len(shapes))
	
	fig, ax = plt.subplots(1,1)
	colors_rgb = []
	for _ in range(116):
		rgb = uniform(0, 1), uniform(0, 1), uniform(0, 1)
		colors_rgb.append(rgb)
	
	for shape, color in zip(shapes, colors_rgb):
		points = shape.points
		x = [el[0] for el in points]
		y = [el[1] for el in points]
		ax.fill(x, y, color=color)
	
	annot = ax.annotate("111", xy=(350000, 5800000), 
		bbox=dict(boxstyle="round", fc="w"))
	annot.set_visible(False)

	fig.canvas.mpl_connect("motion_notify_event",
		lambda event: hover(event, annot, fig, ax))

	plt.show()

def hover(event, annot, fig, ax):
	if event.inaxes == ax:
		x, y = round(event.xdata, 1), round(event.ydata, 1)
		annot.set_text(str(x) + " " + str(y))
		annot.set_position((x + 5000, y + 5000))
		annot.set_visible(True)
		fig.canvas.draw_idle()

if __name__ == '__main__':
	main()