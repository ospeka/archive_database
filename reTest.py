import re

t1 = '5{11}'
t2 = '5-11{11}'

def main():
	p = re.compile(r'\d{1,}\{\d{1,}\}')
	print(p.match(t1))
	print(type(p))
	print(p.search(r'\d{1,}'))



if __name__ == '__main__':
	main()
