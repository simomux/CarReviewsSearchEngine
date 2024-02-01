import gensim
import pandas as pd
from whoosh.analysis import StandardAnalyzer
import numpy as np
import os
import json


def word2vec_creation():
    analyzer = StandardAnalyzer()
    csv = "Review.csv"  # csv file path
    df = pd.read_csv(csv, sep=',', encoding='utf-8')
    columns_to_concat = ['Company', 'Model', 'Year', 'Title', 'Review']  # fields to consider
    content = df[columns_to_concat].apply(lambda row: [token.text for token in analyzer(' '.join(map(str, row)))], axis=1)   # analyze the fields
    model = gensim.models.Word2Vec(sentences=content, window=5, min_count=5, workers=4)  # create and train the model
    model.save("word2vec_review.model")  # save the model


def to_json():
    analyzer = StandardAnalyzer()
    model = gensim.models.Word2Vec.load("word2vec_review.model")  # load the model
    dim = len(model.wv.vectors[0])
    docs_vector = {}
    directory = "Documents"  # directory containing the documents
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            content = ''.join(file.read().split("\n")[7:])
            preprocessed_content = [token.text for token in analyzer(content)]
            words = [word for word in preprocessed_content if word in model.wv]
            if not words:
                docs_vector[filename] = np.zeros(dim)
            else:
                docs_vector[filename] = np.mean([model.wv[word] for word in words], axis=0)
    #  create a dictionary with the document name as key and the vector as value
    #  convert the dictionary to a json file
    serializable_data = {key: value.tolist() for key, value in docs_vector.items()}
    json_file_path = 'document_vectors_fields.json'  # json file path
    with open(json_file_path, 'w') as json_file:
        json.dump(serializable_data, json_file)