# Project for the Information Management Exam A.Y. 2023/2024

## Modules Content

### `dataset_generator.py`
Creates approximately 300,000 files from a specified `.csv` file given as the first argument and stores them in a directory specified as the second argument. Each file corresponds to a line in the `.csv` file, with each argument separated by a newline. This forms the base dataset for the creation of the inverted index.

### `concurrent.py`
A parallel version of the script `dataset_generator.py` that utilizes threads to parallelize the computation, reducing the time by approximately 33%. This conclusion is based on various tests conducted on different PCs.

### `index_generator.py`
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

### `custom_model.py`
Module that contains the classes and methods for the custom scoring of the various models.

Current models:
- **Full-Text model:** Uses BM25F scoring with a slight tune to the free variables `B` and `K1`. Model used to query: BM25F Tuned values: `B=0.1, K1=2`

- **Sentiment model:** Uses the sentiment of the review to influence the score. It has 2 different types of scoring:
  - **Scoring with sentiment value:** Utilizes just the sentiment value of the review to influence the final score with the formula: `final_score = score * sentiment_value`

  - **Scoring with sentiment value and ranking:** Utilizes the sentiment value and the rating of the review to fix the score, avoiding any possible discordances with the rating and the sentiment value. It uses a series of formulae based on the type of sentiment:

    - **Positive sentiment:** `final_score = score * sentiment_value * rating/5`
    - **Negative sentiment:** `final_score = score * sentiment_value * 1.2 - rating/5`
    - **Neutral sentiment:** `if rating > 3: final_score = score * sentiment_value * 0.4 - rating/5` or `if rating < 3: final_score = score * sentiment_value * 0.4 + rating/5`

## Useful files:
- Dataset: [Kaggle dataset](https://www.kaggle.com/datasets/shreemunpranav/edmunds-car-review)
- Complete inverted index: [Link to be added later]()
- Pre-trained sentiment model: [Huggingface page](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest)
- Demo version on the inverted index (~20,000 reviews): [Inverted Index demo](https://www.mediafire.com/file/5mjbepqibwqd1le/indexdirRidotto.zip/file)

## How to use:

- **Creation of dataset:** You can create the index starting from the dataset by downloading it from the link above and pasting it in the project directory. Run `dataset_generator.py` as follows:
  ```python3 -s dataset_generator.py review.csv <output_directory>```


- **Creation of inverted index:** Once you have created the dataset, you can run `index_generator.py` to create the inverted index. Use the following command:
  ```python3 -s <dataset_directory>```
  I suggest trying the demo of the index before creating the entire one, as this script calculates the sentiment of each file during the index generation, and depending on the specs of your PC, this might take a while (It took me ~8 hours for the 1st version of the complete one and ~20 min for the demo one).


- **Querying the index:** After you have downloaded or created the index, you can start querying it. Run `query.py` as follows:
  ```python3 -s query.py <index_directory_path>```

## Requirements
This project was developed and tested with Python 3.11.5 ([Download here](https://www.python.org/downloads/release/python-3115/)). Any use of a different version might cause errors.

Module requirements are listed in `requirements.txt`.

For any info or questions, feel free to contact Mussini Simone at [mussini.simone01@outlook.com](mailto:mussini.simone01@outlook.com).

Project members: [Mussini Simone](https://github.com/simomux), [Siena Andrea](https://github.com/CodKyrat47), [Stomeo Paride](https://github.com/SupremeXGucci420)
