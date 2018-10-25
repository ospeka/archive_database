import json
from pprint import pprint

def main():
    data = json.load(open("./downloaded_data/Bryansk.json", 'r+'))

    print(data[2].keys())
    for i in range(1, 15):
        line = data[i]
        print(line['date'])

if __name__ == '__main__':
    main()