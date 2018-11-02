import re

t1 = '5{12}'
t2 = '5-11{13}'


def main():
	p = re.compile(r'\d{1,3}\-\d{1,3}\{\d{1,5}\}')
	print(p.match(t2))
	print(p.findall(r'\d{1,3}'))





if __name__ == '__main__':
	main()
