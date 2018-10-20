import csv
from pprint import pprint
import re
from Record import Record

needCols = ['Local time in Dmitrovsk', 'T', 'Po' ,'P' , 'U', 'Ff', 'N', 'Td', 'RRR', 'tR', 'sss']
colsDesc = ['T - температура воздуха 2м над землей',
"Po - Атмосферное давление на уровне станции "
'Р - атмосферное давление, приведенное к среднему уровню моря',
'U - относительная влажность' ,
'Ff - скорость ветра на высоте 10-12м над земной поверхностью, осредненная за 10-мин период непосредственно предшествующий сроку наблюдения',
'N - общая облачность',
'Td - температура точки росы на 2м',
'RRR - количество выпавших осадков',
 'tR - период времени, за который накоплено указанное количество осадков',
 'sss - высота снежного покрова'
 ]

def test_main():
	file = csv.reader(open("./data.csv", "r+", encoding = "utf-8"), delimiter=';')
	data = [line for line in file]

	i = 0
	colNames = data[6]
	colIndexes = {colName: colNames.index(colName) for colName in needCols}
	# print(colIndexes)
	# for key in colIndexes.keys():
	# 	print("{:<25s}".format(key), end='')
	# print()
	records = data[7:]
	# for rec in records:
	# 	for ind in colIndexes.values():
	# 		print("{:<25s}".format(rec[ind]), end='')
	# 	print()
	dataDict = {}
	for key in colIndexes.keys():
		dataDict[key] = []
		index = colIndexes[key]
		for rec in records:
			dataDict[key].append(rec[index])
	dataDict['N'] = fixN(dataDict['N'])
	dataDict = convertToDigits(dataDict)
	# printDictAsTable(dataDict)
	testData = {}
	testData["date"] = dataDict["Local time in Dmitrovsk"]
	testData["RRR"] = dataDict["RRR"]
	testData["tR"] = dataDict["tR"]
	printDictAsTable(testData)
	dataByDays = sumPCP(dataDict)

def sumPCP(dataDict):
	records = []
	maxLen = len(dataDict["Local time in Dmitrovsk"])
	for i in range(maxLen):
		date = dataDict["Local time in Dmitrovsk"][i]
		RRR = dataDict["RRR"][i]
		tR = dataDict["tR"][i]
		record = Record(date, RRR, tR)
		records.append(record)

	records = records[::-1]
	recsLen = len(records)
	i = 0;
	test = []
	while (i < (recsLen - 1)):
		currDate = records[i].date
		j = i
		while (i < recsLen and currDate.year == records[i].date.year and currDate.month == records[i].date.month and currDate.day == records[i].date.day):
			i += 1
		if (i == recsLen):
			test.append(records[j:i-1])
		test.append(records[j:i])

	# test2 = []
	# i = 0
	# for rec in records:
	# 	currDate = rec.date
	# 	j = i
	# 	while (i < recsLen and currDate.year == rec.date.year and currDate.month == rec.date.month and currDate.day == rec.date.day):
	# 		i += 1
	# 		#make an iterator from recors and call next in this line . under the while
	# 	test2.append(records[j:i-1])
	print("separeted by days")
	for t in test:
		for d in t:
			print(d)
		print()


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


def convertToDigits(dataDict):
	for key in dataDict.keys():
		if (key == 'Local time in Dmitrovsk' or key == 'RRR'):
			continue
		recordsLen = len(dataDict[key])
		for el in range(0, recordsLen):
			if (dataDict[key][el] != ""):
				dataDict[key][el] = float(dataDict[key][el])
			elif key == 'U':
				dataDict[key][el] = float(dataDict[key][el]) / 100
			elif dataDict[key][el] == "":
				dataDict[key][el] = "no data"
			else:
				dataDict[key][el] = 0
	return (dataDict)
	

def fixN(records):
	res = []
	p = re.compile(r'\s{0,}\d{1,2}\s{0,}[\-, –]\s{0,}\d{1,2}\s{0,}%\.')
	p2 = re.compile(r'\d{1,2}')
	p3 = re.compile(r'\s{0,}\d{1,3}\s{0,}%\.')
	p4 = re.compile(r'\d{1,3}')
	for rec in records:
		if (rec == "90  or more, but not 100%"):
			res.append(0.95)
			continue
		if p.search(rec) != None:
			nums = p2.findall(rec)
			middle = (float(nums[0]) + float(nums[1]))/2
			res.append(middle/100)
			continue
		if (rec ==  'no clouds'):
			res.append(0)
			continue
		if (rec == ""):
			rec.append("no data")
			continue
		if p3.search(rec) != None:
			num = p4.findall(rec)
			res.append(float(num[0]) / 100)
			continue
		res.append(rec)
	return(res)


if __name__ == '__main__':
	test_main()