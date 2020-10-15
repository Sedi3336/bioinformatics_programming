import csv
import sys

def calculate_avg_value(data, column_name):
    sum_data = 0
    for item in data:
        sum_data += item
    return sum_data/len(data)

def find_average_wines(wine_paths):
    dict1 = {}
    for wine_path in wine_paths:
        with open("./data/"+wine_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            dict2 = {}
            column_names = []
            for row in csv_reader:
                if line_count == 0:
                    for item1 in row:
                        dict2[item1] = []
                        column_names.append(item1)
                    line_count += 1
                else:
                    for num,item2 in enumerate(row):
                        dict2[column_names[num]].append(float(item2))

            dict3 = {}
            for k,v in dict2.items():
                dict3[k] = calculate_avg_value(v, k)
            dict1[wine_path.replace('.csv','')] = dict3
    return dict1
def main():
    print(find_average_wines(sys.argv[1:]))

if __name__ == "__main__":
    main()
