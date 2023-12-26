import csv
import sys
import os
from concurrent.futures import ThreadPoolExecutor

import time

def process_row(row, counters_dict, output_directory):
    key = tuple(row[0:3])
    counter = counters_dict.get(key, 0) + 1
    counters_dict[key] = counter

    output_txt_file = os.path.join(
        output_directory,
        f'{row[0]}_{row[1]}_{row[2]}_{counter}.txt'
    )

    with open(output_txt_file, 'w', encoding='utf-8') as txt_file:
        for element in row:
            txt_file.write(element.strip() + '\n')

if __name__ == "__main__":
    tic = time.perf_counter()
    
    if len(sys.argv) < 2:
        raise Exception('Please provide an input file!')

    input_csv_file = sys.argv[1]
    output_directory = sys.argv[2]

    counters_dict = {}
    
    # Create directory if not exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    with open(input_csv_file, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = list(csv_reader)[1:]
        
    with ThreadPoolExecutor() as executor:
        [executor.submit(process_row, row, counters_dict, output_directory) for row in rows]
    
    toc = time.perf_counter()
    elapsed_time = toc - tic
    print(elapsed_time)