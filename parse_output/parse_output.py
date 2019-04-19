from pprint import pprint

# path to outoput file
p = "./output.sub"

def main():
	file = open(p, mode='r')
	lines = file.readlines()
	pprint(lines[:10])

if __name__ == '__main__':
	main()
