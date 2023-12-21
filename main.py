import csv
import pandas as pd
import re


def rimuovi_duplicati(file_input, file_output):
    # Leggi il file CSV
    df = pd.read_csv(file_input)
    # Rimuovi i duplicati basandoti sulle righe complete
    df_senza_duplicati = df.drop_duplicates()
    # Salva il DataFrame senza duplicati in un nuovo file CSV
    df_senza_duplicati.to_csv(file_output, index=False)


def normalize_file_name(file_name):
    # Sostituisci spazi con underscore
    file_name = file_name.replace(' ', '_')
    # Rimozione dei caratteri speciali usando le espressioni regolari
    file_name = re.sub(r'[^\w.-]', '', file_name)
    return file_name


input_csv_file = 'Review.csv'
output_directory = 'Output/'
rimuovi_duplicati(input_csv_file, 'Reviews.csv')
input_csv_file = 'Reviews.csv'

with open(input_csv_file, 'r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader, None)  # Salta l'intestazione della tabella
    i = 0   # Contatore per il nome del file che garantisce l'unicità del nome
    for row in csv_reader:
        # Crea un file txt per ogni riga del file CSV
        output_txt_file = output_directory + f'{i}_{row[0]}_{row[1]}_{row[2]}_{normalize_file_name(row[3])}.txt'
        with open(output_txt_file, 'w', encoding='utf-8') as txt_file:
            # Scrivi ogni elemento della riga del file CSV nel file txt
            for element in row:
                txt_file.write(element.strip() + '\n')
        i += 1
