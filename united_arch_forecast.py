import forecast.forecast as fc
from pprint import pprint
import sys

def main():
    sys.path.append('.')
    sys.path.append('./forecast')
    stations = fc.create_stations()
    stations = fc.perfom_calcs(stations)
    for st in stations:
        print(st)

if __name__ == '__main__':
    main()
