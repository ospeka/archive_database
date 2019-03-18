import csv
from pprint import pprint
import re
from Record import Record
import datetime as dt

needCols = ['Local time in Dmitrovsk', 'T', 'Po', 'P', 'U', 'Ff', 'N', 'Td', 'RRR', 'tR', 'sss']
colsDesc = ['T - температура воздуха 2м над землей',
            "Po - Атмосферное давление на уровне станции "
            'Р - атмосферное давление, приведенное к среднему уровню моря',
            'U - относительная влажность',
            'Ff - скорость ветра на высоте 10-12м над земной поверхностью, осредненная за 10-мин период непосредственно предшествующий сроку наблюдения',
            'N - общая облачность',
            'Td - температура точки росы на 2м',
            'RRR - количество выпавших осадков',
            'tR - период времени, за который накоплено указанное количество осадков',
            'sss - высота снежного покрова'
            ]

def main():
    file = csv.reader(open("./data.csv", "r+", encoding="utf-8"), delimiter=';')
    content = [line for line in file]
    colNames = content[6]
    colIndexes = {colName: colNames.index(colName) for colName in needCols}
    data = content[7:]
    for line in data:
        print(line[0], "   ", line[colIndexes["RRR"]])
    recordsList = linesToObjs(data, colIndexes)[::-1]
    dataByDay = recsListByDay(recordsList)
    # print("\nsepareted by days\n")
    # for l in dataByDay:
    #     for el in l:
    #         print(el)
    #     print()
    recountedRecs = recountPCP(dataByDay)
    print("\nRecounted pcp(tR)")
    # for el in recountedRecs:
    #     print(el)
    recountedRecs = fillGapDays(recountedRecs)
    for el in recountedRecs:
        print(el)


def fillGapDays(recountedRecs):
    firstDay = recountedRecs[0].date.day
    lastDay= recountedRecs[-1].date.day
    recsLen = len(recountedRecs)
    if (lastDay - firstDay) == recsLen:
        return recountedRecs
    i = 0
    oneDay = dt.timedelta(days=1)
    while i < (recsLen - 1):
        currDate = recountedRecs[i].date
        nextDate = recountedRecs[i + 1].date
        if nextDate.day != (nextDate.day - 1):
            fillGapDay = currDate + oneDay
            newRecord = Record(fillGapDay, "no data", "no data")
            recountedRecs.insert(i + 1, newRecord)
        i += 1
    return (recountedRecs)


def recountPCP(dataByDay):
    res = []
    for day in dataByDay:
        recountedDay = recountDay(day)
        res.append(recountedDay)
    return res

def recountDay(day):
    lastRecord = day[0]
    for record in day:
        if record.RRR == "no data":
            continue
        else:
            lastRecord = record
    # print("last record", lastRecord)
    tR_template = re.compile(r'\s{0,}\d{1,}\.\d{1,}\s{0,}')
    summPCP = countPCPSum(lastRecord, day, tR_template)
    # print("sum pcp", summPCP)
    # if lastRecord.RRR == no data  ---->>> means to mark it as NO DATA or smth else
    newRecord = Record(dt.date(year=lastRecord.date.year, month=lastRecord.date.month, day=lastRecord.date.day),
                       summPCP, "24")
    return newRecord

def countPCPSum(lastRecord, day, tR_template):
    summPCP = 0

    if lastRecord.date.hour == 21:
        if tR_template.match(lastRecord.RRR):
            summPCP += float(lastRecord.RRR)
        for record in day:
            if record.date.hour == 9 and record.RRR.isdigit():
                summPCP += float(record.RRR)
        return summPCP
    elif lastRecord.date.hour == 18:
        if tR_template.match(lastRecord.RRR):
            summPCP += float(lastRecord.RRR)
        for record in day:
            if record.date.hour == 6 and record.RRR.isdigit():
                summPCP += float(record.RRR)
        return summPCP
    else:
        return "no data"


def recsListByDay(recsList):
    """
    :param recsList: list of Record objects
    :return: list of lists by day
    """
    dateByDay = []
    i = 0
    recsLen = len(recsList)
    res = []
    while i < (recsLen - 1):
        j = i
        currDate = recsList[i].date
        while i < (recsLen-1) and isDayEqual(currDate, recsList[i].date):
            i += 1
        res.append(recsList[j: i])
    return res


def isDayEqual(date1, date2):
    """
    :param date1: datetime object to compare
    :param date2: datetime object to compare
    :return: true if year , month and day are equal
    """
    if (date1.year != date2.year):
        return False
    if (date1.month != date2.month):
        return False
    if (date1.day != date2.day):
        return False
    return True


def linesToObjs(data, colInds):
    """
    :param data: list of data from rp5 database (google it)
    :param colInds: dict where key - name of column ,value - index of column name
    :return: list of objects type of Record
    """
    dateInd = colInds['Local time in Dmitrovsk']
    rrrInd = colInds['RRR']
    tRInd = colInds['tR']
    listObs = []
    for rec in data:
        date = dt.datetime.strptime(rec[dateInd], "%d.%m.%Y %H:%M")
        rrr = rec[rrrInd]
        tR = rec[tRInd]
        listObs.append(Record(date, rrr, tR))
    return listObs


def printDictAsTable(dataDict):
    """
    Print dict in table format. Names of columns is dict keys, values in values with this keys.
    """
    keys = dataDict.keys()
    maxLen = 0
    for key in keys:
        recordLen = len(dataDict[key])
        if recordLen > maxLen:
            maxLen = recordLen
    for key in keys:
        print("{:25s}".format(key), end="")
    print()
    for i in range(0, maxLen):
        for key in keys:
            print("{:25s}".format(str(dataDict[key][i])), end="")
    print()


if __name__ == '__main__':
    main()
