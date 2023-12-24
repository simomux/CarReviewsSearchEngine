import csv
import sys
import os
# from tqdm import tqdm


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        raise Exception('Please provide an input file!')

    input_csv_file = sys.argv[1]
    output_directory = sys.argv[2]

    counter = 1
    bckp = []

    with open(input_csv_file, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)  # Skippa l'intestazione della tabella
        for row in csv_reader: # _ in tqdm(range(num_lines), desc="Creating Files", unit="file"):
            if bckp != row[0:3]:
                counter = 1
            bckp = row[0:3]
            output_txt_file = os.path.join(output_directory, f'{row[0]}_{row[1]}_{row[2]}_{counter}.txt')
            counter += 1

            with open(output_txt_file, 'w', encoding='utf-8') as txt_file:
                for element in row:
                    txt_file.write(element.strip() + '\n')
                        
