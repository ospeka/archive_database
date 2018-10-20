import re

def main():
	""""
	dafsgvcx
	"""
	p = re.compile(r'[Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche]{1}')
	s = 'Mardi'
	print(p.search(s))
	print(p.findall(s))


if __name__ == '__main__':
	main()
