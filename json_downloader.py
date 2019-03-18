# Download and parse data from pgodklimat.ru
# save it into json files

import requests as r
from bs4 import BeautifulSoup as bs
from pprint import pprint
import datetime as dt
from dateutil.relativedelta import relativedelta
import calendar
import json

url = "http://www.pogodaiklimat.ru/weather.php"
charset = "windows-1251"
# tr - ryadku
# td - klitunka ryadka
# дата
# Облачность общая (первая цифра до черты)
# Т, Tmin, Tmax, R, S
# Ветер скорость
# И Td надо будет пересчитывать, чтобы вычислить относ. влажность
# S не понадобится для прогноза, но полезное значение
id = "26898"
# bryansk
start_data = dt.date(year=2011, month=1, day=1)
end_data = dt.date.today()


def main():
    city_ids = json.load(open("./city_ids.json", "r"))
    pprint(city_ids)
    get_params = {
        "id": "26898",
        "bday": "1",
        "fday": "10",
        "amonth": "10",
        "ayear": "2018",
        "bot": "2"
    }
    one_month = relativedelta(months=1)
    curr_data = start_data
    data_list = []
    i = 1
    j = 1
    for city in city_ids.keys():
        print(city, "number - ", j)
        data_list.append({'city': city, 'city_id': city_ids[city]})
        get_params['id'] = city_ids[city]
        while isNotMonthYearEqual(curr_data, end_data):
            print("request number - ", i)
            month_last = calendar.monthrange(curr_data.year, curr_data.month)[1]
            get_params['fday'] = str(month_last)
            get_params['amonth'] = str(curr_data.month)
            get_params['ayear'] = str(curr_data.year)
            table = get_table(get_params)
            data = parse_table(table)
            data['year'] = str(curr_data.year)
            data['date'].append({'year': get_params["ayear"]})
            data_list.append(data)
            curr_data += one_month
            i += 1
        i = 1
        j += 1
        curr_data = start_data
        with open("./downloaded_data/" + str(city) + ".json", 'w+') as fout:
            json.dump(data_list, fout)
        data_list = []


def isNotMonthYearEqual(date1, date2):
    # change this ugly function
    if date1.month != date2.month:
        return True
    if date1.year != date2.year:
        return True
    return False


def get_table(get_params):
    resp = r.get(url, get_params)
    soup = bs(resp.content, "html.parser")
    table = soup.find("div", {"id": "archive"}).table.table
    all_trs = table.find_all('tr')
    return all_trs


def parse_table(trs):
    data = {
        'date': [],
        'wind': [],
        'cloud': [],
        'T': [],
        'Tmin': [],
        'Tmax': [],
        'R': [],
        'S': [],
        'f': [],
        'Td': []
    }
    for tr in trs[1:]:
        tds = tr.find_all('td')
        data['date'].append(tds[0].text + " " + tds[1].text)
        data['wind'].append(tds[3].text)
        data['cloud'].append(tds[6].text)
        data['T'].append(tds[7].text)
        data['Tmin'].append(tds[15].text)
        data['Tmax'].append(tds[16].text)
        data['R'].append(tds[17].text)
        data['S'].append(tds[19].text)
        data['Td'].append(tds[8].text)
        data['f'].append(tds[9].text)
    return data


if __name__ == '__main__':
    main()
