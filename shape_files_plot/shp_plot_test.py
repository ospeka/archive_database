# from pprint import pprint
import matplotlib.pyplot as plt
from random import uniform

subbasins_path = "./polygons.txt"
test_path = "./pol_test.txt"

def main():
    subbasin_polygons = open(subbasins_path, mode='r').readlines()
    subbasins = parse_subbasins(subbasin_polygons)
    fig, axes = plt.subplots(1,1)
    for sub in subbasins:
        sub.plot(axes)
    count = 0
    print('Subbasins count: ', len(subbasins))
    for sub in subbasins:
        if sub.one_pol:
            count += 1
            continue
        else:
            count += len(sub.pol)
    print('Polygons count: ', count)

    plt.show()

    
def parse_subbasins(lines):
    l = len(lines)
    start = 0
    subbasins = []
    for i in range(l):
        try:
            if lines[i + 1] == "\n" and lines[i + 2] == "\n":
                end = i + 1
                subbasin = parse_subbasin(lines, start, end)
                if subbasin is None:
                    break
                subbasins.append(subbasin)
                start = i + 2
        except IndexError:
            end = l - 1
            subbasin = parse_subbasin(lines, start, end)
            subbasins.append(subbasin)
            break
    return subbasins


def parse_subbasin(lines, start, end):
    to_parse = lines[start:end]
    if not to_parse:
        return None
    if '\n' in to_parse[1:]:
        subbasin = Subbasin(one_pol=False)
        pol = Polygon()

        for el in to_parse[1:]:
            if el == '\n':
                subbasin.pol.append(pol)
                pol = Polygon()
                continue
            splited = el.split()
            x, y = float(splited[0]), float(splited[1])
            pol.add_point(x, y)
        subbasin.pol.append(pol)
        return subbasin
    else:
        pol = Polygon()
        for el in to_parse[1:]:
            splited = el.split()
            x, y = float(splited[0]), float(splited[1])
            pol.add_point(x, y)
        subbasin = Subbasin()
        subbasin.pol = pol
        return subbasin



class Subbasin(object):
    """Subbasin represents actually subbasin.
        If subbasin contains only one polygon then
        attr pol is type of Polygon. If subbasins contains
        many polygons then attr poll is list of objects type of
        Polygon
    """
    def __init__(self, one_pol=True):
        super(Subbasin, self).__init__()
        self.pol = []
        self.one_pol = one_pol

    def _plot_one_pol(self, pol, rgb, ax):
        r, g, b = rgb
        x = []
        y = []
        for point in pol.points:
            x.append(point.x)
            y.append(point.y)
        ax.fill(x, y, color=(r, g, b))
        ax.plot(x, y, color='r', linewidth=0.75)

    def plot(self, ax):
        r, g, b = uniform(0, 1), uniform(0, 1), uniform(0, 1)
        rgb = r, g, b
        if  not self.one_pol:
            for pol in self.pol:
                self._plot_one_pol(pol, rgb, ax)
        else:
            x = []
            y = []
            for point in self.pol.points:
                x.append(point.x)
                y.append(point.y)
            ax.fill(x, y, color=(r, g, b))
            ax.plot(x, y, color='r', linewidth=0.75)

    def __str__(self):
        s = ''
        try:
            _ = (e for e in self.pol)
            s += "Polygons: " + str(len(self.pol)) + "\n"
            for pol in self.pol:
                s += pol.__str__() + '\n'
            return s
        except TypeError:
            s += "Polygons: 1\n"
            return s + self.pol.__str__()
        

class Polygon(object):
    """docstring for Polygon"""
    def __init__(self):
        super(Polygon, self).__init__()
        self.points = []

    def add_point(self, x, y):
        self.points.append(Point(x, y))

    def __str__(self):
        s = ''
        for el in self.points:
            s += "x:" + str(el.x) + " y:" + str(el.y) + "\n"
        return s

class Point(object):
    """docstring for Point"""
    def __init__(self, x, y):
        super(Point, self).__init__()
        self.x = x
        self.y = y
        
    

if __name__ == "__main__":
    main()
