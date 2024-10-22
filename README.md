# Project for my Information Management Exam A.Y. 2023/2024

## Abstract
Buying a new car can be tricky and complicated due to the vast number of carmakers and models, each with its own pros, cons, and special features. This search engine aims to help people filter down reviews for car models, suggesting the most interesting and relevant ones to them first.

## Modules Content

### [dataset_generator.py](https://github.com/simomux/progettoGestione/blob/a0489d38bbda6fa0dfb621d6adf7c1a8be7930d3/dataset_generator.py)
Creates approximately 300,000 files from a specified `.csv` file given as the first argument and stores them in a directory specified as the second argument. Each file corresponds to a line in the `.csv` file, with each argument separated by a newline. This forms the base dataset for the creation of the inverted index.

### [concurrent_generator.py](https://github.com/simomux/progettoGestione/blob/a0489d38bbda6fa0dfb621d6adf7c1a8be7930d3/concurrent_generator.py)
A parallel version of the script `dataset_generator.py` that concurrently create the dataset, reducing the time by approximately 33%. This conclusion is based on various tests conducted on different PCs.

### [index_generator.py](https://github.com/simomux/progettoGestione/blob/a0489d38bbda6fa0dfb621d6adf7c1a8be7930d3/index_generator.py)
This script creates the inverted index from the files generated with `dataset_generator.py`, taking the directory of the files as the first argument. The inverted index is then saved in the current directory.

#### Index Schema definition:
- `file`: filename of a review
- `maker`: car manufacturer of the reviewed car
- `model`: car model of the reviewed car
- `year`: year of the reviewed car
- `author`: author of the review
- `date`: date of the review
- `title`: title of the review
- `rating`: rating of the review
- `content`: actual review

### [query.py](https://github.com/simomux/progettoGestione/blob/a0489d38bbda6fa0dfb621d6adf7c1a8be7930d3/query.py)
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

Wildcards don't work on query with specified fields (ex. `maker:a*`), because `maker` and `model` fields are set as ID in the schema definition to avoid the preprocessing of them, since it worsen the query results. 

### [custom_model.py](https://github.com/simomux/progettoGestione/blob/a0489d38bbda6fa0dfb621d6adf7c1a8be7930d3/custom_model.py)
Module that contains the classes and methods for the custom scoring of the various models.

Current models:
- **Full-Text model:** Uses BM25F scoring with a slight tune to the free variables `B` and `K1`. Model used to query: BM25F Tuned values: `B=0.5, K1=1.5`.


- **Sentiment model:** Uses the sentiment of the review to influence the score. It's been designed to work both for `BM25F` and `TF_IDF`. It has 2 different types of scoring:
  - **Scoring with sentiment value:** Utilizes just the sentiment value of the review to influence the final score with the formula: `final_score = score * sentiment_value`.

  - **Scoring with sentiment value and ranking:** Utilizes the sentiment value and the rating of the review to fix the score, avoiding any possible discordances with the rating and the sentiment value. It uses a series of formulae based on the type of sentiment (see code comment for more):

    - **Positive sentiment:** `final_score = score * sentiment_value * rating/5`.
    - **Negative sentiment:** `final_score = score * sentiment_value * 1.2 - rating/5`.
    - **Neutral sentiment:** `if rating > 3: final_score = score * sentiment_value * 0.4 - rating/5` or `if rating < 3: final_score = score * sentiment_value * 0.4 + rating/5`.


- **Word2Vec model:** The model has been custom trained on our dataset using the **CBOW** (Continuous Bag Of Words) architecture. For each word in a document it calculates a vector and then compute the vector mean of a document. The mean are stored in a `.json` file that is used by the custom model class that calculates the cosine similarity between each document and the preprocessed query vector. Then utilize the following formula to get the final score: `final_score = score * cosine_similarity`.


## Useful files:
- Dataset: [Kaggle dataset](https://www.kaggle.com/datasets/shreemunpranav/edmunds-car-review)
- Complete inverted index: [Link to be added later]()
- Pre-trained sentiment model: [Huggingface page](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest)
- Demo version on the inverted index (~20,000 reviews): [Inverted Index demo](https://www.mediafire.com/file/mqfcztpq35x6n13/indexdirRidotto.zip/file)
- Word2Vec model trained by us: [Word2Vec model](https://www.mediafire.com/file/f43lx8ymrx286yc/word2vec_review.model/file)
- Word2Vec vectors of all dataset: [Word2Vec vectors](https://www.mediafire.com/file/1j63wkiyaeard1w/document_vectors_fields.json/file)

## How to use:

- **Creation of dataset:** You can create the index starting from the dataset by downloading it from the link above and pasting it in the project directory. Run `dataset_generator.py` as follows:
  ```python3 -s dataset_generator.py review.csv <output_directory>```.


- **Creation of inverted index:** Once you have created the dataset, you can run `index_generator.py` to create the inverted index. Use the following command:
  ```python3 -s index_generator.py <dataset_directory>```
  I suggest trying the demo of the index before creating the entire one, as this script calculates the sentiment of each file during the index generation, and depending on the specs of your PC, this might take a while (It took me ~8 hours for the 1st version of the complete one and ~20 min for the demo one).


- **Querying the index:** After you have downloaded or created the index, you can now download the Word2Vec model and the Word2Vec vectors in the working directory. Then simply run `query.py` as follows:
  ```python3 -s query.py <index_directory_path>```.

## Requirements
This project was developed and tested with Python 3.11.5 ([Download here](https://www.python.org/downloads/release/python-3115/)). Any use of a different version might cause errors.

Module requirements are listed in [requirements.txt](https://github.com/simomux/CarReviewsSearchEngine/blob/5fb045b1c24db719de011c4c2bc6061400b77e35/requirements.txt).

Project members: [Mussini Simone](https://github.com/simomux), [Siena Andrea](https://github.com/CodKyrat47), [Stomeo Paride](https://github.com/paridestomeo)
