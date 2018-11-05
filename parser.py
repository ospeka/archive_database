import json
from pprint import pprint
import datetime as dt
from collections import OrderedDict
from DayRecord import DayRecord

def get_city_data(path="./downloaded_data/Druzhba.json"):
    data = json.load(open(path, 'r'))
    # print("year = ", data[1]['date'][-1]['year'])
    # print("monthes - ", len(data) - 1)
    # print("city - ", data[0]['city'])
    city_name = data[0]['city']
    # month_data = parse_month(data[1])
    city_data = []
    month_number = 1
    for month in data[1:]:
        month_data = parse_month(month)
        city_data.extend(month_data)
        month_number += 1
    # for rec in city_data:
    #     print(rec)
    return city_data, city_name

def parse_month(month):
    year = month['year']
    num_of_recs_by_day = num_of_records_by_day(month)
    # pprint(num_of_recs_by_day)
    i = 0
    month_records = []
    for key in num_of_recs_by_day.keys():
        j = i + num_of_recs_by_day[key]
        month_records.append(DayRecord(start=i, end=j, month_data=month, date=key))
        i += num_of_recs_by_day[key]
    return month_records


def num_of_records_by_day(month):
    year = month['year']
    month['date'] = month['date'][0:-1]
    num_of_recs_by_day = {}
    for date_str in month['date']:
        try:
            date = dt.datetime.strptime(date_str + " " + year, '%H %d.%m %Y')
        except ValueError:
            continue
        num_of_recs_by_day[date] = 0
    res = OrderedDict()
    for key in num_of_recs_by_day.keys():
        day = key.replace(hour=0)
        res[day] = 0
        for key2 in num_of_recs_by_day:
            if key.day == key2.day:
                res[day] += 1
    return res


def print_month(month_data):

    keys = month_data.keys()
    number_of_recs = len(month_data['date']) - 1
    for key in keys:
        print("{:30s}".format(key), end=" ")
    print()
    for i in range(number_of_recs):
        for key in keys:
            if key == 'cloud':
                try:
                    slash_index = month_data[key][i].index('/')
                    print("{:30s}".format(month_data[key][i])[:slash_index], end=" ")
                except ValueError:
                    print("{:30s}".format(month_data[key][i]), end=" ")
                continue
            if key != 'year' and month_data[key][i] == "":
                print("{:30s}".format("_"), end=" ")
                continue
            if key != 'year':
                print("{:30s}".format(month_data[key][i]), end=" ")
        print()





if __name__ == '__main__':
    get_city_data()
