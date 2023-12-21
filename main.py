import csv
import pandas as pd

def rimuovi_duplicati(file_input, file_output):
    # Leggi il file CSV
    df = pd.read_csv(file_input)

    # Rimuovi i duplicati basandoti sulle righe complete
    df_senza_duplicati = df.drop_duplicates()

    # Salva il DataFrame senza duplicati in un nuovo file CSV
    df_senza_duplicati.to_csv(file_output, index=False)
    print("Duplicati rimossi con successo e salvati in", file_output)


def normalize_file_name(file_name):
    # Replace spaces with underscores
    file_name = file_name.replace(' ', '_')

    # Remove special characters using regular expression
    import re
    file_name = re.sub(r'[^\w.-]', '', file_name)

    # Ensure the file name is not empty
    file_name = file_name if file_name else 'unnamed_file'

    return file_name


input_csv_file = 'Review.csv'
output_directory = 'Output/'
rimuovi_duplicati(input_csv_file, 'Reviews.csv')
input_csv_file = 'Reviews.csv'

with open(input_csv_file, 'r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader, None)      # Skippa l'intestazione della tabella
    for i in range(0,500):     # Il for è solo per testing, per creare tutti i file sostiuire con un 'While True:'
        next(csv_reader, None)
        second_row = next(csv_reader, None)
        if second_row is None:
            continue
        print(second_row)
        output_txt_file = output_directory + f'{second_row[0]}_{second_row[1]}_{second_row[2]}_{normalize_file_name(second_row[3])}.txt'

        with open(output_txt_file, 'w', encoding='utf-8') as txt_file:
            for element in second_row:
                txt_file.write(element.strip() + '\n')
