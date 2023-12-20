import csv

input_csv_file = 'Directory/CSV/FILE.csv'
output_directory = f'Directory/Output/Directory/'

with open(input_csv_file, 'r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader, None)      # Skippa l'intestazione della tabella
    for i in range(0,500):     # Il for è solo per testing, per create tutti i file sostiuire con un 'While True:'
        next(csv_reader, None)
        second_row = next(csv_reader, None)
        if second_row is None:
            continue
        print(second_row)
        output_txt_file = output_directory + f'{second_row[0]}_{second_row[1]}_{second_row[2]}_{second_row[3]}.txt'

        with open(output_txt_file, 'w', encoding='utf-8') as txt_file:
            for element in second_row:
                txt_file.write(element.strip() + '\n')