import ftplib
from pprint import pprint 
from datetime import datetime

port = 21
url = "ftp://osipov_weather:jH9lf26Z@uhmi.org.ua"
login = "osipov_weather"
paswd = "jH9lf26Z"


def main():
	f = ftplib.FTP()
	f.connect("uhmi.org.ua", port)
	f.login(login, paswd)
	f.cwd("osipov_weather")
	files = f.nlst()
	# pprint(files)
	# lines = []
	# resp = f.retrlines('RETR ./cgms_01_01_2019.txt', callback=lines.append)
	for file_name in files:
		file_lines = []
		f.retrlines('RETR ./' + file_name, callback=file_lines.append)
		compare_file_date(file_name, file_lines)


def compare_file_date(file_name, file_lines):
	day = int(file_name[5:7])
	month = int(file_name[8:10])
	year = int(file_name[11:15])
	file_name_date = datetime(year=year, month=month, day=day).date()
	for file_line in file_lines:
		cols = file_line.split(';')
		file_line_date = datetime.strptime(cols[1], "%d.%m.%Y").date()
		if file_line_date != file_name_date:
			print(file_name)
			print(file_line)
			print()


if __name__ == '__main__':
	main()