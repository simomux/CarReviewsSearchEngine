# How to use:
# Tested with Python 3.11.5
# Run python3 -s index_generator.py <dataset_directory>

import sys
import time
import os
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import Schema, TEXT, NUMERIC, DATETIME, ID, KEYWORD, STORED
from whoosh.index import create_in
from datetime import datetime

from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax

MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

max_length = 512  # Max amount of tokens


def index_files_in_directory(directory):
    # Schema definition
    schema = Schema(
        file=STORED,
        maker=ID(stored=True),
        model=ID(stored=True),
        year=NUMERIC,
        author=STORED,
        date=DATETIME(stored=True),
        title=STORED,
        rating=NUMERIC(stored=True),
        content=TEXT(analyzer=StemmingAnalyzer(), stored=True),
        sentiment_value=NUMERIC(stored=True),
        sentiment_type=KEYWORD(stored=True)
    )

    # Index directory creation
    if not os.path.exists("tmp_indexdir"):
        os.mkdir("tmp_indexdir")
    ix = create_in("tmp_indexdir", schema)

    # Open index writer
    writer = ix.writer()

    i = 0

    # Read all files in the input directory
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            content = file.read()

            #  Separate fields by newline
            fields = content.split('\n')
            print(f'\nN: {i}')
            print(f'File: {filename}')

            text = '\n'.join(fields[7:])
            print(text)

            encoded_input = tokenizer(text, max_length=max_length, return_tensors='pt', truncation=True)

            output = model(**encoded_input)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)

            tmp_dict = {
                'negative': scores[0],
                'neutral': scores[1],
                'positive': scores[2]
            }

            print(tmp_dict)

            max_score = max(tmp_dict.values())
            max_type = list(tmp_dict.keys())[list(tmp_dict.values()).index(max_score)]

            print(f'Sentiment: {max_type}, {max_score}')

            #  Convert date to datetime
            try:
                tmp_date = datetime.strptime(fields[4], "%m/%d/%Y")
            except ValueError:
                tmp_date = datetime(1970, 1, 1, 0, 0, 0)
            #  Add document to index
            writer.add_document(file=filename, maker=fields[0], model=fields[1], year=fields[2], author=fields[3],
                                date=tmp_date, title=fields[5], rating=fields[6], content=text,
                                sentiment_value=max_score, sentiment=max_type)
            i += 1
            if i == 20000:
                break
    # Close index writer
    writer.commit()


if __name__ == "__main__":
    # Check arguments
    if len(sys.argv) == 2:
        print("Generating inverted index for Full-Text Search")
    else:
        print("Wrong number of arguments!")
        exit(1)

    tic = time.perf_counter()

    output_directory = sys.argv[1]
    index_files_in_directory(output_directory)

    toc = time.perf_counter()
    elapsed_time = toc - tic
    print(f"\n\nElapsed time: " + str(round(elapsed_time, 2)))
