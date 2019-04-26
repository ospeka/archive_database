import shapefile as shp
from pprint import pprint
# import matplotlib.pyplot as plt
from random import uniform

p = "./Subbasins116.shp"

def main():
	sf = shp.Reader(p)
	# pprint(dir(sf))
	# pprint(sf.fields)
	shapes = sf.shapes()
	recs = sf.shapeRecords()
	for rec in recs:
		print(rec.record[22])
	
	
	
	
if __name__ == '__main__':
	main()