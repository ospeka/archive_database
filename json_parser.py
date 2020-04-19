import json
import datetime as dt
from collections import OrderedDict
from DayRecord import DayRecord
from pprint import pprint
import json_downloader

city_ids = json.load(open("./city_ids.json", "r"))

def get_city_data(get_params, path="./downloaded_data/SpasDemensk.json"):
    data = json.load(open(path, 'r'))
    city_name = data[0]['city']
    city_data = []
    for month in data[1:]:
        month_data = parse_month(month)
        city_data.extend(month_data)
    pcp_data = []
    for month in data[1:]:
        month_len = len(month['date'])
        year = month['year']
        for i in range(month_len - 1):
            date = month['date'][i] + ' ' + year
            pcp = month['R'][i]
            pcp_data.append([date, pcp])
    get_params['id'] = data[0]['city_id']
    pcp_data = recount_pcp2(pcp_data, get_params)
    # last day pcp is not countable coz its needed
    # next day pcp to recount it
    for dr, pcp, in zip(city_data, pcp_data):
        dr.pcp = pcp[1]

    return city_data, city_name


def recount_pcp(pcp_data):
    dates = OrderedDict()
    for el in pcp_data:
        try:
            date = dt.datetime.strptime(el[0], '%H %d.%m %Y').date()
        except ValueError:
            pcp_data.remove(el)
            continue
        if date not in dates:
            dates[date] = [el[1]]
        else:
            dates[date].append(el[1])
    records = [[key, value] for key, value in dates.items()]
    records_len = len(records)
    pcp = None
    for i in range(records_len - 1):
        today_pcp = records[i][1]
        tomorrow_pcp = records[i + 1][1]
        try:
            if today_pcp[5] != '':
                if tomorrow_pcp[1] != '':
                    pcp = float(today_pcp[5]) + float(tomorrow_pcp[1])
                else:
                    pcp = float(today_pcp[5])
            elif today_pcp[6] != '':
                if tomorrow_pcp[2] != '':
                    pcp = float(today_pcp[6]) + float(tomorrow_pcp[2])
                else:
                    pcp = float(today_pcp[6])
            elif tomorrow_pcp[1] != '':
                pcp = float(tomorrow_pcp[1])
            elif tomorrow_pcp[2] != '':
                pcp = float(tomorrow_pcp[2])
        except IndexError:
            pcp = None
        if pcp is not None and pcp > 200:
            pcp = pcp / 50
        if pcp is not None and pcp > 100:
            pass
            # avarage with nearest station!
        records[i][1] = pcp
        pcp = None
    return records


def recount_pcp2(pcp_data, get_params):
    hours_list = []
    for el in pcp_data:
        date_string = el[0].strip(' ')
        try:
            date_time = dt.datetime.strptime(date_string, '%H %d.%m %Y')
        except ValueError:
            continue
        if el[1] == '':
            val = None
        else:
            val = float(el[1])
        hours_list.append([date_time, val])
    days_list = []
    try:
        curr_hour_record = hours_list[0]
    except:
        print(hours_list)
        print(pcp_data)
        print(get_params)
        return [['', None]]
    day_list = []
    for el in hours_list:
        if el[0].day == curr_hour_record[0].day:
            day_list.append(el)
        else:
            days_list.append(day_list)
            day_list = [el]
            curr_hour_record = el
    else:
        days_list.append(day_list)
    res = []
    for i in range(len(days_list[:-1])):
        val = count_value(days_list[i], days_list[i + 1])
        if val is not None and val > 200:
            val = val / 50
        if val is not None:
            val = round(val, 3)
        res.append([days_list[i][0][0].date(), val])

    last_day_hours_list = days_list[-1]
    last_day = days_list[-1][0][0]

    one_day = dt.timedelta(days=1)
    next_day = last_day + one_day
    new_get_params = get_params
    new_get_params['bday'] = next_day.day
    new_get_params['fday'] = next_day.day
    new_get_params['amonth'] = next_day.month
    new_get_params['ayear'] = next_day.year

    citys_names_by_id = {v: k for k, v in city_ids.items()}
    data_list = [{'city': citys_names_by_id[new_get_params["id"]], 'city_id': new_get_params["id"]}]
    dates_table, data_table = json_downloader.get_table(get_params)
    data = json_downloader.parse_table(dates_table, data_table)
    data['date'].append({'year': get_params["ayear"]})
    data['year'] = str(2015)
    data_list.append(data)
    next_day_pcp = data_list[1]['R']
    next_day_dates = data_list[1]['date'][:-1]

    hours_list = []
    for pcp, date in zip(next_day_pcp, next_day_dates):
        date_string = (date + " " + str(new_get_params['ayear'])).strip()
        try:
            date_time = dt.datetime.strptime(date_string, '%H %d.%m %Y')
        except ValueError:
            last_day_error = True
            break
        if pcp == '':
            val = 0
        else:
            val = float(pcp)
        hours_list.append([date_time, val])
    else:
        last_day_error = False
    last_day_value = count_value(last_day_hours_list, hours_list, last_day_error=last_day_error)
    res.append([last_day.date(), round(last_day_value, 3)])

    return res


def count_value(today_el, tommorow_el, last_day_error=False):
    val1 = None
    hour = 15
    for el in today_el:
        if el[0].hour == hour:
            val1 = el[1]
    if val1 is None:
        hour = 18
    for el in today_el:
        if el[0].hour == hour:
            val1 = el[1]
    if val1 is None:
        val1 = None
    if last_day_error:
        return val1
    val2 = None
    hour = 3 if hour == 15 else 6
    for el in tommorow_el:
        if el[0].hour == hour:
            val2 = el[1]
    if val2 is None:
        val2 = None
    if val1 is None and val2 is not None:
        return val2
    elif val1 is not None and val2 is None:
        return val1
    elif val1 is None and val2 is None:
        return None
    return val1 + val2



def parse_month(month):
    year = month['year']
    num_of_recs_by_day = num_of_records_by_day(month)
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


if __name__ == '__main__':
    get_city_data()
