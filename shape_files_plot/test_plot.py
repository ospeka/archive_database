import shapefile as shp
from pprint import pprint
import matplotlib.pyplot as plt
from random import uniform
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np

path = "./Subbasins116.shp"

def main():
    sf = shp.Reader(path)
    shapes = sf.shapes()

    fig, ax = plt.subplots(1,1)
    colors_rgb = []
    for _ in range(116):
        rgb = uniform(0, 1), uniform(0, 1), uniform(0, 1)
        colors_rgb.append(rgb)


    patches = []
    for ind, color in zip([62, 77, 22, 50 , 113], colors_rgb):
        points = shapes[ind].points
        x = [el[0] for el in points]
        y = [el[1] for el in points]
        ax.fill(x, y, color=color)
        ax.plot(x, y, color='r')
    plt.show()
    
    

if __name__ == '__main__':
    main()