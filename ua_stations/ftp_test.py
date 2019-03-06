import ftplib
from pprint import pprint 

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
	pprint(files)
	# lines = []
	# resp = f.retrlines('RETR ./cgms_01_01_2019.txt', callback=lines.append)
	# pprint(lines)
	needed_year = [el for el in files if '2018' in el]
	# pprint(needed_year)
	# print(len(needed_year))	




if __name__ == '__main__':
	main()