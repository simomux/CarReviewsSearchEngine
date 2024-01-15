import sys
import time
import nltk
import os
import string
from nltk.corpus import stopwords
from whoosh import index
from whoosh.analysis import StandardAnalyzer
from whoosh.fields import Schema, TEXT, NUMERIC, DATETIME
from whoosh.index import create_in
from datetime import datetime

nltk.download('punkt')
nltk.download('stopwords')

# Funzione per il pre-processing del testo
def preprocess_text(text):
    tokens = nltk.word_tokenize(text)
    wnl = nltk.WordNetLemmatizer()
    clean_tokens = [wnl.lemmatize(word) for word in tokens if word not in stopwords.words('english') and word not in string.punctuation]
    print(clean_tokens)
    return clean_tokens


# Funzione per leggere i file da una cartella, applicare il pre-processing e creare l'indice Woosh
def index_files_in_directory(directory):
    # Definire lo schema per l'indice
    schema = Schema(
        file = TEXT(stored=True),
        auto = TEXT(stored=True),
        model = TEXT(stored=True),
        year = NUMERIC(stored=True),
        #author=TEXT(stored=True),
        date = DATETIME(stored=True),
        title = TEXT(stored=True),
        rating = NUMERIC(stored=True),
        content = TEXT(analyzer=StandardAnalyzer(), stored=True)
    )

    # Creare un nuovo indice nella directory specificata
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    ix = create_in("indexdir", schema)

    # Aprire l'indice per l'aggiunta di documenti
    writer = ix.writer()

    # Elaborare i file nella cartella
    '''
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):  # Modifica il filtro per il tipo di file desiderato
                file_path = os.path.join(root, filename)
                print(file_path)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    preprocessed_text = preprocess_text(content)
                    print(preprocessed_text)
                    writer.add_document(path=file_path, content=preprocessed_text)
    '''

    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            content = file.read()
            # Perform any necessary text preprocessing here
            fields = content.split('\n')
            # Add document to the index
            print(filename)
            try:
                tmpdate=datetime.strptime(fields[4], "%m/%d/%Y")
            except ValueError:
                tmpdate=datetime.now()


            writer.add_document(file=filename, auto=fields[0], model=fields[1], year=fields[2], date=tmpdate, title=fields[5], rating=fields[6], content=''.join(fields[7:]))

    # Committare le modifiche e chiudere il writer
    writer.commit()


if __name__ == "__main__":
    if len(sys.argv) < 1:
        raise Exception('Please provide the output directory!')
    if len(sys.argv) > 2:
        raise Exception('Too many arguments!')
    
    tic = time.perf_counter()

    output_directory = sys.argv[1]

    # Esempio di utilizzo della funzione per indicizzare i file nella cartella 'documents_folder'
    index_files_in_directory(output_directory)

    toc = time.perf_counter()
    elapsed_time = toc - tic
    print("\n\nElapsed time: " + round(elapsed_time, 2))