import requests as r
from bs4 import BeautifulSoup as bs
from pprint import pprint
import datetime as dt
from dateutil.relativedelta import relativedelta
import calendar


url = "http://www.pogodaiklimat.ru/weather.php"
charset = "windows-1251"
#tr - ryadku
#td - klitunka ryadka

# дата
# Облачность общая (первая цифра до черты)
# Т, Tmin, Tmax, R, S
# Ветер скорость
# И Td надо будет пересчитывать, чтобы вычислить относ. влажность
# S не понадобится для прогноза, но полезное значение
id = "26898"#bryansk
start_data = dt.date(year=2011, month=1, day=1)
end_data = dt.date.today()

def main():
    # get_params = {
    #     "id": "26898",
    #     "bday": "1",
    #     "fday": "10",
    #     "amonth": "10",
    #     "ayear": "2018",
    #     "bot": "0"
    # }
    # table = get_table(get_params["id"], get_params["bday"], get_params["amonth"], get_params["ayear"])
    # # for item in table:
    # #     print(item.prettify())
    # data = parse_table(table)
    # pprint(data)
    print("start data ", start_data)
    print("end data ", end_data)
    one_month = relativedelta(months=1)
    curr_data = start_data
    dates = []
    while (isNotMonthYearEqual(curr_data, end_data)):
        print("curr data", curr_data)
        month_last = calendar.monthrange(curr_data.year, curr_data.month)[1]
        print(month_last)
        curr_data += one_month
        dates.append(curr_data)
    print(len(dates))


def isNotMonthYearEqual(date1, date2):#change this ugly function
    if date1.month != date2.month:
        return True
    if date1.year != date2.year:
        return True
    return False


def get_table(id, start_day, finish_day, month, year):
    get_params = {
        "id": id,
        "bday": start_day,
        "fday": finish_day,
        "amonth": month,
        "ayear": year,
        "bot": "0"
    }
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
        'S': []
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
    return data

def create_col_names_dict(first_tr):
    all_tds = first_tr.find_all('td')
    col_names = {td.text: [] for td in all_tds}
    return col_names





if __name__ == '__main__':
    main()
