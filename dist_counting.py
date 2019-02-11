import geopy.distance as gp
import json

coors_path = "./station_coors.txt"


def main():
    content = open(coors_path, mode='r').readlines()
    stations = []
    for line in content:
        splited = line.split()
        st = {}
        st['name'] = splited[0]
        st['lon'] = splited[1]
        st['lat'] = splited[2]
        stations.append(st)
    st_data = {}
    for st1 in stations:
        st_data[st1['name']] = {}
        for st2 in stations:
            c1 = (float(st1['lon']), float(st1['lat']))
            c2 = (float(st2['lon']), float(st2['lat']))
            distance = round(gp.vincenty(c1, c2).km, 2)
            if distance != 0:
                st_data[st1['name']][st2['name']] = distance
    with open("./station_distances.json", 'w+') as fout:
        json.dump(st_data, fout)


if __name__ == '__main__':
    main()
