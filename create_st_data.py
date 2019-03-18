import requests as r
from pprint import pprint
import json


ids = [489868,467753,462914,462822,571476,552920,523186,479028,572295,565908,709584,563300,694603,694273,506596,538560,704915,482986,538908,695019,707758,516400,538560,705135,699942,692194,698247,688726]
elev = [248,224,200,167,189,197,157,210,164,176,181,155,154,116,224,231,210,260,147,176,127,250,105,133,107,150,109,50]
api_adress = "http://api.openweathermap.org/data/2.5/forecast?APPID=3137ee4c7c2ca995b5ad22cbc2d67bd9&id="

def main():
    stations = []
    for id, ele in zip(ids, elev):
        url = api_adress + str(id)
        data = r.get(url).json()
        st_data = {}
        st_data["alter_names"] = []
        st_data["name"] = data["city"]["name"]
        if st_data["name"] == "Vyshegrad":
            st_data["name"] = "Vyshhorod"
            st_data["alter_names"].append("Vyshegrad")
        if st_data["name"] == "Ponyri Vtoryye":
            st_data["name"] = "Ponyri_Vtorye"
            st_data["alter_names"].append("Ponyri Vtoryye")
        st_data["lat"] = round(data["city"]["coord"]["lat"], 1)
        st_data["lon"] = round(data["city"]["coord"]["lon"], 1)
        st_data["elev"] = ele
        st_data["id_open_weather_map"] = id
        stations.append(st_data)
    pprint(stations)
    file = open("./st_data.json", mode='w+')
    json.dump(stations, file)




if __name__ == "__main__":
    main()