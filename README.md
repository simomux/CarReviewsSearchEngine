# Project for the Information Management Exam A.Y. 2023/2024

## Modules Content

### `dataset_generator.py`
Creates approximately 300,000 files from a specified `.csv` file given as the first argument and stores them in a directory specified as the second argument. Each file corresponds to a line in the `.csv` file, with each argument separated by a newline. This forms the base dataset for the creation of the inverted index.

### `concurrent.py`
Parallel version of the script `dataset_generator.py` that utilizes threads to parallelize the computation, reducing the time by approximately 33%. This conclusion is based on various tests conducted on different PCs.

### `index_generator.py`
This script creates the inverted index from the files generated with `main.py`, taking the directory of the files as the first argument. The inverted index is then saved in the current directory.

#### Schema definition:
- `file`: field that contains the filename of a review
- `maker`: car manufacturer of the car reviewed
- `model`: car model of the car reviewed
- `year`: year of the car reviewed
- `author`: author of the review
- `date`: date of the review
- `title`: title of the review
- `rating`: rating of the review (still WIP; might use it to fix false results from sentiment)
- `content`: actual review

### `query.py`
Script that works on the directory of the index (needs to be in the working directory) and allows asking queries on the inverted index.

Main search functions and syntax:
- Full-text search: word1 word2
- Phrasal search: "word1 word2"
- Wildcard search: word*
- Range search: [word1 TO word2]
- Proximity search: "word1 word2"~N
- Boolean search: word1 AND/OR/NOT word2
- Fuzzy search: word~
- Digit 0 for exit

Sorting functions:
- Sorting by date (sort results by the most recent date that matches the query and then print the top 10)
- Show sentiment of the top 10 Full-Text search results
- Sorting by sentiment (sort results by sentiment that matches the query and then print the top 10)
- STILL WIP: Sorting by Word2Vec (sort results by cosine similarity that matches the query and then print the top 10)

Model used to query: BM25F
Tuned values: `B=0.1, K1=2`

Project Members: Mussini Simone, Siena Andrea, Stomeo Paride
