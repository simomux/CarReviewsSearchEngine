# This module contains the custom classes for scoring
from whoosh.scoring import BM25F, TF_IDF
import gensim
from whoosh.analysis import StandardAnalyzer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def preprocessed_query(query, model):
    # Create a vector representation from the query
    dim = len(model.wv.vectors[0])
    analyzer = StandardAnalyzer()
    preprocessed_content = [token.text for token in analyzer(query)]
    words = [word for word in preprocessed_content if word in model.wv]
    if not words:
        query_vector = np.zeros(dim)
    else:
        query_vector = np.mean([model.wv[word] for word in words], axis=0)
    return query_vector


def word2vec_score(doc, score, query, loaded_data_dict, model):
    # Calculate cosine similarity of the query and the document
    query_vector = preprocessed_query(query, model)
    doc_vector = loaded_data_dict[doc['file']]
    similarity = cosine_similarity([query_vector], [doc_vector])[0][0]
    return score * similarity


# Sentiment scoring
# Each review has 3 sentiment values:
# - Neutral
# - Positive
# - Negative

# Where:
# 1 = neutral + positive + negative

# doc['sentiment_value'] = max(neutral, positive, negative)

def sentiment_score(doc, score):
    # Since the sentiment value is between 0 and 1 the function discredit the review with weak sentiment and boosts
    # the strong one

    # Ex query: maker:bmw sentiment:positive
    # 12 * 0.9  <-- 1st value
    # 16 * 0.5  <-- 2nd value

    return score * doc['sentiment_value']


def sentiment_score2(doc, score):
    # Utilize rating to boost/discredit reviews that do/don't match it with their sentiment
    value_fix = 1
    rating = int(doc['rating'])

    # If sentiment is positive but rating is low discredit the score
    # Progressive so that:
    # 5-star reviews got 100% of their original score
    # 4-star reviews got 80% of their original score
    # 3-star reviews got 60% of their original score
    # 2-star reviews got 40% of their original score
    # 1-star reviews got 20% of their original score
    if doc['sentiment_type'] == 'positive':
        value_fix = rating / 5

    # If sentiment is negative but rating is high discredit the score
    # Progressive so that:
    # 1-star reviews got 100% of their original score
    # 2-star reviews got 80% of their original score
    # 3-star reviews got 60% of their original score
    # 4-star reviews got 40% of their original score
    # 5-star reviews got 20% of their original score
    elif doc['sentiment_type'] == 'negative':
        value_fix = 1.2 - rating / 5

    # If sentiment is neutral but rating is extremely high/low discredit the score
    # Progressive so that:
    # 1-star reviews got 60% of their original score
    # 2-star reviews got 80% of their original score
    # 3-star reviews got 100% of their original score
    # 4-star reviews got 80% of their original score
    # 5-star reviews got 60% of their original score
    elif doc['sentiment_type'] == 'neutral':
        if rating > 3:
            value_fix = 0.4 - rating / 5
        elif rating < 3:
            value_fix = 0.4 + rating / 5

    return score * doc['sentiment_value'] * value_fix


class FullTextModel(BM25F):
    def __init__(self):
        super().__init__(B=0.5, K1=1.5)


class SentimentModelBM25F(FullTextModel):
    use_final = True

    def final(self, searcher, docnum, score):
        # Uncomment the score method you want to use
        return sentiment_score(searcher.stored_fields(docnum), score)


class SentimentModelRatingBM25F(FullTextModel):
    use_final = True

    def final(self, searcher, docnum, score):
        # Uncomment the score method you want to use
        return sentiment_score2(searcher.stored_fields(docnum), score)


class SentimentModelTFIDF(TF_IDF):
    use_final = True

    def final(self, searcher, docnum, score):
        # Uncomment the score method you want to use
        return sentiment_score(searcher.stored_fields(docnum), score)


class SentimentModelRatingTFIDF(TF_IDF):
    use_final = True

    def final(self, searcher, docnum, score):
        # Uncomment the score method you want to use
        return sentiment_score2(searcher.stored_fields(docnum), score)


class Word2VecModel(BM25F):
    se_final = True
    query_input = ""
    loaded_data_dict = {}
    model = gensim.models.Word2Vec.load("word2vec_review.model")  # window=5, min_count=5

    def __init__(self, loaded_data_dict):
        super().__init__(B=0.75, K1=1.5)
        self.loaded_data_dict = loaded_data_dict

    def set_query(self, query):
        self.query_input = query

    def final(self, searcher, docnum, score):
        return word2vec_score(searcher.stored_fields(docnum), score, self.query_input, self.loaded_data_dict,
                              self.model)
