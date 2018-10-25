import json
from pprint import pprint

def main():
    content = json.load(open("./downloaded_data/Bryansk.json", 'r+'))
    data = content[1:]

    data_len = len(data)
    for i in range(15):

        for key in data[i].keys():
            print("{:>10s}".format(key), end=" ")
        print()
        for j in range(15):
            for key in data[i].keys():
                if (data[i][key][j] == ""):
                    print("{:>10s}".format("_"), end=" ")
                    continue
                print("{:>10s}".format(data[i][key][j]), end=" ")
            print()




if __name__ == '__main__':
    main()