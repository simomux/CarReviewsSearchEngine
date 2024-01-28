# How to use:
# Tested with Python 3.11.5
# Run python3 -s concurrent_generator.py review.csv <output_directory>

import csv
import sys
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import time


def process_row(args):
    row, counters_dict, output_directory = args
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


def main():
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
        next(csv_reader, None)  # Skip header row
        rows = list(csv_reader)

    with ThreadPoolExecutor() as executor:

        # tqdm prende un iteratore e la lunghezza massima
        # ad ogni iterazione aggiorna la barra

        # executor è un aggreggato di tanti oggetti che
        # verranno eseguiti, viene applicato process_row
        # su ogni row di rows (ottenuta leggendo il csv)

        for _ in tqdm(
                executor.map(
                    process_row,
                    [(row, counters_dict, output_directory) for row in rows]),
                total=len(rows)):
            pass

    toc = time.perf_counter()
    elapsed_time = toc - tic
    print(f"Total time: {elapsed_time} seconds")


if __name__ == "__main__":
    main()
