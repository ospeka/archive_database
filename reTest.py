import re

def main():
	""""
	dafsgvcx
	"""
	p = re.compile(r'\s{0,}\d{1,}\.\d{1,}\s{0,}')
	s = '2.0'
	print(p.match(s))



if __name__ == '__main__':
	main()
