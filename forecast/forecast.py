import requests as r
from datetime import datetime, timedelta
from .station import Station

from .pcp import count_pcp, write_pcp
from .clouds import calc_clouds, write_clouds
from .humidity import calc_hmd, write_hmd
from .temp import calc_temp, write_temp
from .wind import calc_wind, write_wind

api_adress = "http://api.openweathermap.org/data/2.5/forecast?APPID=3137ee4c7c2ca995b5ad22cbc2d67bd9&id="
ids = [489868,467753,462914,462822,571476,552920,523186,479028,572295,565908,709584,563300,694603,694273,506596,538560,704915,482986,538908,695019,707758,516400,538560,705135,699942,692194,698247,688726]
elev = [248,224,200,167,189,197,157,210,164,176,181,155,154,116,224,231,210,260,147,176,127,250,105,133,107,150,109,50]

def perform_all(dirpath):
	stations = create_stations()
	stations = perfom_calcs(stations)
	write_pcp(stations, dirpath)
	write_temp(stations, dirpath)
	write_wind(stations, dirpath)
	write_hmd(stations, dirpath)
	write_clouds(stations, dirpath)


def perfom_calcs(stations):
	for st in stations:
		st.pcp = count_pcp(st)
		st.clouds = calc_clouds(st)
		st.hmd = calc_hmd(st)
		st.temp = calc_temp(st)
		st.wind = calc_wind(st)
	return stations

def create_stations():
	stations = []
	for id, ele in zip(ids, elev):
		url = api_adress + str(id)
		data = r.get(url).json()
		station = Station(data["city"]["name"])
		if station.name == "Ponyri Vtoryye":
			station.name = "Ponyri_Vtorye"
		if station.name == "Vyshegrad":
			station.name = "Vyshhorod"
		station.lat = round(data["city"]["coord"]["lat"], 1)
		station.lon = round(data["city"]["coord"]["lon"], 1)
		station.data = data["list"]
		station.id = data["city"]["id"]
		station.elev = ele
		stations.append(station)
	return stations

if __name__ == '__main__':
	stations = create_stations()
	print(stations[0])
