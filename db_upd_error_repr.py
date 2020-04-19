import json_downloader
import json_parser
import json
from pprint import pprint

get_params = {
        "id": "33135", # chernigiv
        "bday": "1",
        "fday": "31",
        "amonth": "10",
        "ayear": "2015",
        "bot": "2"
    }
update_data_dir = "./update_data/"
st_name = "Unecha"

def main():
    # data_list = [{'city': st_name, 'city_id': "26985"}]
    # dates_table, data_table = json_downloader.get_table(get_params)
    # data = json_downloader.parse_table(dates_table, data_table)
    # data['date'].append({'year': get_params["ayear"]})
    # data['year'] = str(2015)
    # data_list.append(data)
    # path = update_data_dir + st_name + "_upd_data.json"
    # with open(path, 'w+') as fout:
    #     json.dump(data_list, fout)
    path = 'downloaded_data/Chernigiv.json'
    st_data, st_name_from_json = json_parser.get_city_data(get_params, path=path)
    print(st_data[1].pcp)

if __name__ == '__main__':
    main()