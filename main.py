import csv
import sys
from tqdm import tqdm


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        raise Exception('Please provide an input file!')

    input_csv_file = sys.argv[1]
    output_directory = sys.argv[2]

    counter = 1
    bckp = []

    with open(input_csv_file, 'r', encoding='utf-8') as file:
        num_lines = 300000 # sum(1 for line in file if line.strip())

    with open(input_csv_file, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        print(num_lines)
        next(csv_reader, None)  # Skippa l'intestazione della tabella
        for _ in tqdm(range(num_lines), desc="Creating Files", unit="file"):
            next(csv_reader, None)
            second_row = next(csv_reader, None)
            if second_row is None:
                continue
            if bckp != second_row[0:3]:
                counter = 1
            bckp = second_row[0:3]
            output_txt_file = output_directory + f'{second_row[0]}_{second_row[1]}_{second_row[2]}_{counter}.txt'
            counter += 1

            with open(output_txt_file, 'w', encoding='utf-8') as txt_file:
                for element in second_row:
                    txt_file.write(element.strip() + '\n')
