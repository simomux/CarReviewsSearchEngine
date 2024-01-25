# Project for the Information Management Exam A.Y. 2023/2024

## Modules Content

### `dataset_generator.py`
Creates approximately 300,000 files from a specified `.csv` file given as the first argument and stores them in a directory specified as the second argument. Each file corresponds to a line in the `.csv` file, with each argument separated by a newline. This forms the base dataset for the creation of the inverted index.

### `concurrent.py`
A parallel version of the script `dataset_generator.py` that utilizes threads to parallelize the computation, reducing the time by approximately 33%. This conclusion is based on various tests conducted on different PCs.

### `index_generator.py`
This script creates the inverted index from the files generated with `dataset_generator.py`, taking the directory of the files as the first argument. The inverted index is then saved in the current directory.

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
A script that works on the directory of the index (needs to be in the working directory) and allows asking queries on the inverted index.

Main search functions and syntax:
- Full-text search: `word1 word2`
- Phrasal search: `"word1 word2"`
- Wildcard search: `word*`
- Range search: `[word1 TO word2]`
- Proximity search: `"word1 word2"~N`
- Boolean search: `word1 AND/OR/NOT word2`
- Fuzzy search: `word~`
- Digit `0` for exit

Sorting functions:
- Sorting by date (sort results by the most recent date that matches the query and then print the top 10)
- Show sentiment of the top 10 Full-Text search results
- Sorting by sentiment (sort results by sentiment that matches the query and then print the top 10)
- STILL WIP: Sorting by Word2Vec (sort results by cosine similarity that matches the query and then print the top 10)

Model used to query: BM25F
Tuned values: `B=0.1, K1=2`

## Useful files:
- Dataset: [Link to the Kaggle dataset](https://www.kaggle.com/datasets/shreemunpranav/edmunds-car-review)
- Complete inverted index: [Link to Inverted Index](*TODO*)
- Word2Vec pre-trained module: [Link to Word2Vec Module](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?resourcekey=0-wjGZdNAUop6WykTtMip30g)
- Demo version on the inverted index: [Link to the Inverted Index demo](https://www.mediafire.com/file/5mjbepqibwqd1le/indexdirRidotto.zip/file)

## How to use:
You can create the index starting from the dataset by downloading the dataset from the link above and pasting it in the project directory and by running `dataset_generator.py` as such: `python3 -s dataset_generator.py review.csv <output_directory>`.

Once you have created the dataset, you have basically split the `.csv` creating a file for each review, you can run `index_generator` and actually create the inverted index, by using the following command: `python3 -s <dataset_directory> <type_of_index>`.

You can create the simple Full-Text index by using `'full-text'` as the second argument. This creates a simple Full-Text index.
A dedicated version of `query.py` for this index still needs to be done. To avoid this problem use the index for sentiment analysis.

You can create the index for sentiment analysis by using `'sentiment'`, which calculates the sentiment of each file one-by-one and stores it in a dedicated field of the index. I still advise downloading the index directly and avoiding this, since creating the final version of the sentiment index took me more than 7 hours.

Otherwise, you can download the entire index, or a demo version of it with only 20,000 files from the link above (use your unimore email to avoid confirmation (due to security reasons I can't avoid this issue)) and run directly `query.py` as such: `python3 -s query.py <index_directory_path>`.

Project Members: Mussini Simone, Siena Andrea, Stomeo Paride
