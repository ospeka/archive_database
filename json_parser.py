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
    pcp_data = recount_pcp(pcp_data, get_params)
    # last day pcp is not countable coz its needed
    # next day pcp to recount it
    for dr, pcp, in zip(city_data, pcp_data):
        dr.pcp = pcp[1]

    return city_data, city_name


def recount_pcp(pcp_data, get_params):
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
    if last_day_value is not None:
        last_day_value = round(last_day_value, 3)
    res.append([last_day.date(), last_day_value])
    return res



def count_value(today_el, tomorrow_el, last_day_error=False):
    today_15 = None
    today_18 = None
    tomorrow_03 = None
    tomorrow_06 = None
    tomorrow_15 = None
    datetime_15 = "exist"
    datetime_18 = "exist"
    datetime_03 = "exist"
    datetime_06 = "exist"
    for el in today_el:
        if el[0].hour == 15:
            today_15 = el[1]
            datetime_15 = "exist"
            break
        else:
            datetime_15 = "absent"
    for el in today_el:
        if el[0].hour == 18:
            today_18 = el[1]
            datetime_18 = "exist"
            break
        else:
            datetime_18 = "absent"

    if not last_day_error:
        for el in tomorrow_el:
            if el[0].hour == 3:
                tomorrow_03 = el[1]
                datetime_03 = "exist"
                break
            else:
                datetime_03 = "absent"
        for el in tomorrow_el:
            if el[0].hour == 6:
                tomorrow_06 = el[1]
                datetime_06 = "exist"
                break
            else:
                datetime_06 = "absent"
        for el in tomorrow_el:
            if el[0].hour == 15:
                tomorrow_15 = el[1]
    if datetime_15 == "absent" and datetime_18 == "absent" and datetime_03 == "absent" and datetime_06 == "absent":
        return None  # что-нибудь, что сигнализирует о том, что надо взять данные с соседней станции

    pcp_total = 0.0
    if today_15 is not None:
        pcp_total += today_15
    if tomorrow_03 is not None:
        pcp_total += tomorrow_03
    else:
        if today_18 is not None:
            pcp_total += today_18
        if tomorrow_06 is not None:
            if tomorrow_15 is None:
                pcp_total += tomorrow_06
            elif datetime_03 == "absent":
                pcp_total += 0.75 * tomorrow_06
            elif today_18 is None and tomorrow_06 is None:
                pcp_total = None
    return pcp_total


def parse_month(month):
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
    pass

