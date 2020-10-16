import csv
import pickle
import sys

'''
calculate_avg_value function gets a dictionary of four columns as data and a string to match with the column’s name and calculate the average value for that column.
data is a dictionary of four columns with the key of a string and value of a list of floats.
'''
def calculate_avg_value(data, column_name):
    sum_data = 0
    for item in data:
        sum_data += item
    return ('%.2f' % (sum_data/len(data)))

'''
find_average_wines function takes some csv file paths in a list as input.
Then it reads each csv file individually and creates a dictionary(header_value) of that csv file.
In this dictionary, the key is csv's column names and the values are the corresponding values in each column of the csv file.
Then this function sends those dictionaries to the calculate_avg_value function and generates a new dictionary( header_avg ) out of the average values for each column.
At the end, another dictionary (result) is made with the key of wine_paths ( each csv file) and a value of the last dictionary (header_avg) and returns it.

'''
def find_average_wines(wine_paths):
    result = {}
    for wine_path in wine_paths:
        with open("./data/"+wine_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            header_value = {}
            column_names = []
            for row in csv_reader:
                if line_count == 0:
                    for header in row:
                        header_value[header] = []
                        column_names.append(header)
                    line_count += 1
                else:
                    for num,value in enumerate(row):
                        header_value[column_names[num]].append(float(value))

            header_avg = {}
            for k,v in header_value.items():
                header_avg[k] = calculate_avg_value(v, k)
            result[wine_path.replace('.csv','')] = header_avg
    return result
'''
sys.argv is a list in Python, which contains the command-line arguments passed to the script.
Pickle Python module is used to save the resulting dictionary to a file in a directory called results
'''
def main():
    results = find_average_wines(sys.argv[1:])
    print("Here are the avreages for different wine types and qualities:")
    for k,v in results.items():
        print(str(k) + ":" + (25-len(k))*' ' + str(v))
    print("saving the results in a pickle file in results directory...")
    with open('./results/results.pickle', 'wb') as handle:
        pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)

'''
This common piece of code is used to run the main function when my script is called from the command line (in this case bash script)
'''
if __name__ == "__main__":
    main()

