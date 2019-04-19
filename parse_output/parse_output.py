from pprint import pprint

# path to output file
p = "./output.sub"

def main():
	file = open(p, mode='r')
	lines = file.readlines()
	data_lines = lines[9:]
	col_names = lines[8].split()

	subbasins = [set_up_dict(col_names) for _ in range(116)]
	days = data_lines[::116]
	days_num = len(days)
	
	for day in days:
		for subbasin in subbasins:
			print(day)
			print(subbasin)
			exit()






def set_up_dict(col_names):
	subbasin = {}
	for col_name in col_names:
		subbasin[col_name] = []
	return subbasin


if __name__ == '__main__':
	main()
