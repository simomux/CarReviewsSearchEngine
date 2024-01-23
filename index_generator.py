import sys
import time
import os
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import Schema, TEXT, NUMERIC, DATETIME, STORED, ID
from whoosh.index import create_in
from datetime import datetime
from decimal import Decimal
import sentiment

accuracy = 5


def normalize_sentiment(scores):
    negative = scores[0]
    neutral = scores[1]
    positive = scores[2]

    sentiment_sum = negative + neutral + positive

    # Normalize the value from 3 different variables to a single one with domain [0:10]
    normalized_value = ((positive - negative) / sentiment_sum + 1) * 5 if sentiment_sum != 0 else 0
    return normalized_value


def index_files_in_directory(directory, type_of_index):
    # Schema definition
    schema = Schema(
        file=STORED,
        maker=ID(stored=True),
        model=ID(stored=True),
        year=NUMERIC,
        author=STORED,
        date=DATETIME(stored=True, sortable=True),
        title=STORED,
        rating=NUMERIC,
        content=TEXT(analyzer=StemmingAnalyzer(), stored=True)
    )

    # sentiment_value needs to be treated as an Integer with decimals in order to sort by this field
    if type_of_index == 'sentiment':
        schema.add('sentiment_value', NUMERIC(int, sortable=True, stored=True, decimal_places=accuracy))

    # Index directory creation
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    ix = create_in("indexdir", schema)

    # Open index writer
    writer = ix.writer()

    i = 0

    # Read all files in the input directory
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            content = file.read()

            #  Separate fields by newline
            fields = content.split('\n')
            # print(filename)
            i += 1
            print(f'\nFile: {i}')

            text = ''.join(fields[7:])

            if type_of_index == 'sentiment':
                normalized_value = normalize_sentiment(sentiment.index_sentiment(text))

            print(normalized_value)

            #  Convert date to datetime
            try:
                tmp_date = datetime.strptime(fields[4], "%m/%d/%Y")
            except ValueError:
                tmp_date = datetime(1970, 1, 1, 0, 0, 0)
            #  Add document to index
            writer.add_document(file=filename, maker=fields[0], model=fields[1], year=fields[2], author=fields[3],
                                date=tmp_date, title=fields[5], rating=fields[6], content=text,
                                sentiment_value=Decimal(round(normalized_value, accuracy)))

    # Close index writer
    writer.commit()


if __name__ == "__main__":

    # Sentiment analysis index generation
    type_of_index = ""

    # Check arguments
    if len(sys.argv) > 3:
        raise Exception('Too many arguments!')
    if len(sys.argv) < 2:
        raise Exception('Too few arguments!')
    if len(sys.argv) == 3:
        if sys.argv[2].lower().strip() == 'sentiment':
            type_of_index = "sentiment"
            print("Generating inverted index for sentiment analysis")

    if input("Are you sure of your choice? The index generation might take a while (y/n) ").lower() != 'y':
        exit(1)

    tic = time.perf_counter()

    output_directory = sys.argv[1]

    index_files_in_directory(output_directory, type_of_index)

    toc = time.perf_counter()
    elapsed_time = toc - tic
    print(f"\n\nElapsed time: " + str(round(elapsed_time, 2)))
