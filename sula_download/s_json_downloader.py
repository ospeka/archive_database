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
# tr - рядки
# td - клітинка рядка
# дата
# Облачность общая (первая цифра до черты)
# Т, Tmin, Tmax, R, S
# Ветер скорость
# И Td надо будет пересчитывать, чтобы вычислить относ. влажность
# S не понадобится для прогноза, но полезное значение
id = "26898"
# bryansk
start_data = dt.date(year=2015, month=1, day=1)
end_data = dt.date.today()


def main():
    city_ids = json.load(open("./sula_ids.json", "r"))
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
            dates_table, data_table = get_table(get_params)
            data = parse_table(dates_table, data_table)
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
    # print(url, get_params)
    soup = bs(resp.content, "html.parser")
    table = soup.find("div", {"class": "archive-table"})
    dates_table = table.find("div", {"class": "archive-table-left-column"}).find_all("tr")
    data_table = table.find("div", {"class": "archive-table-wrap"}).find_all("tr")
    return dates_table, data_table


def parse_table(dates_table, data_table):
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
    for date, weather_data in zip(dates_table[1:], data_table[1:]):
        # print(date)
        # print(weather_data)
        date_tds = date.find_all('td')
        data['date'].append(date_tds[0].text + ' ' + date_tds[1].text)
        wd_tds = weather_data.find_all('td')  # wd_tds - weather data td's
        data['wind'].append(wd_tds[1].text)
        data['cloud'].append(wd_tds[4].text)
        data['T'].append(wd_tds[5].text)
        data['Tmin'].append(wd_tds[-5].nobr.text)
        data['Tmax'].append(wd_tds[-4].nobr.text)
        data['R'].append(wd_tds[-3].text)
        data['S'].append(wd_tds[-1].text)
        data['Td'].append(wd_tds[6].nobr.text)
        data['f'].append(wd_tds[7].text)
    return data


if __name__ == '__main__':
    main()
