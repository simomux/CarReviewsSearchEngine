import sys
import time
import os
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import Schema, TEXT, NUMERIC, DATETIME, STORED, ID
from whoosh.index import create_in
from datetime import datetime

def index_files_in_directory(directory):
    # Schema definition
    schema = Schema(
        file = STORED,
        maker = ID(stored=True),
        model = ID(stored=True),
        year = NUMERIC,
        author = STORED,
        date = DATETIME(stored=True, sortable=True),
        title = STORED,
        rating = NUMERIC,
        content = TEXT(analyzer=StemmingAnalyzer())
    )

    # Index directory creation
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    ix = create_in("indexdir", schema)

    # Open index writer
    writer = ix.writer()

    # Read all files in the input directory
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            content = file.read()

            # Separate fields by newline
            fields = content.split('\n')
            print(filename)

            # Convert date to datetime
            try:
                tmpdate = datetime.strptime(fields[4], "%m/%d/%Y")
            except ValueError:
                tmpdate = datetime(1970, 1, 1, 0, 0, 0)
            # Add document to index
            writer.add_document(file=filename, maker=fields[0], model=fields[1], year=fields[2], author=fields[3], date=tmpdate, title=fields[5], rating=fields[6], content=''.join(fields[7:]))

    # Close index writer
    writer.commit()


if __name__ == "__main__":
    # Check arguments
    if len(sys.argv) != 2:
        raise Exception('Too many or too less arguments!')
    
    tic = time.perf_counter()

    output_directory = sys.argv[1]

    index_files_in_directory(output_directory)

    toc = time.perf_counter()
    elapsed_time = toc - tic
    print(f"\n\nElapsed time: " + str(round(elapsed_time, 2)))