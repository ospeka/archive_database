from pprint import pprint

subbasins_path = "./polygons.txt"

def main():
	subbasin_polygons = open(subbasins_path, mode='r').readlines()
	# pprint(subbasin_polygons[:10])
	subbasins = parse_subbasins(subbasin_polygons)
	print(len(subbasins))
	


def parse_subbasins(lines):
	l = len(lines)
	start = 0
	subbasins = []
	for i in range(l):
		try:
			if lines[i + 1] == "" and lines[i + 2] == "":
				end = i + 1
				subbasin = parse_subbasin(lines, start, end)
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
	subbasin = Subbasin()
	pol = Polygon()
	is_one_pol = True
	for line in to_parse:
		if line != "":
			splited = line.split()
			x, y = splited[0], splited[1]
			pol.add_point(x, y)
		else:
			is_one_pol = False
			subbasin.one_pol = False
			subbasin.pol.append(pol)
			pol = Polygon()
	if is_one_pol:
		subbasin.pol = pol
	return subbasin



class Subbasin(object):
	"""Subbasin represents actually subbasin.
		If subbasin contains only one polygon then
		attr pol is type of Polygon. If subbasins contains
		many polygons then attr poll is list of objects type of
		Polygon
	"""
	def __init__(self):
		super(Subbasin, self).__init__()
		self.pol = []
		self.one_pol = True

	def plot(self, ax):
		pass

class Polygon(object):
	"""docstring for Polygon"""
	def __init__(self):
		super(Polygon, self).__init__()
		self.points = []

	def add_point(self, x, y):
		self.points.append(Point(x, y))

class Point(object):
	"""docstring for Point"""
	def __init__(self, x, y):
		super(Point, self).__init__()
		self.x = x
		self.y = y
		
	

if __name__ == "__main__":
	main()
