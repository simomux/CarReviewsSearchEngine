from whoosh.scoring import BM25F, TF_IDF


def sentiment_score(doc, score):
    # Since the sentiment value is between 0 and 1 the function discredit the review with weak sentiment and boosts
    # the strong one
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
        value_fix = rating/5

    # If sentiment is negative but rating is high discredit the score
    # Progressive so that:
    # 1-star reviews got 100% of their original score
    # 2-star reviews got 80% of their original score
    # 3-star reviews got 60% of their original score
    # 4-star reviews got 40% of their original score
    # 5-star reviews got 20% of their original score
    elif doc['sentiment_type'] == 'negative':
        value_fix = 1.2 - rating/5

    # If sentiment is neutral but rating is extremely high/low discredit the score
    # Progressive so that:
    # 1-star reviews got 60% of their original score
    # 2-star reviews got 80% of their original score
    # 3-star reviews got 100% of their original score
    # 4-star reviews got 80% of their original score
    # 5-star reviews got 60% of their original score
    elif doc['sentiment_type'] == 'neutral':
        if rating > 3:
            value_fix = 0.4 - rating/5
        elif rating < 3:
            value_fix = 0.4 + rating/5

    return score * doc['sentiment_value'] * value_fix


class FullTextModel(BM25F):
    def __init__(self):
        super().__init__(B=0.75, K1=1.5)


class SentimentModelBM25F(FullTextModel):
    use_final = True

    def final(self, searcher, docnum, score):
        # Uncomment the score method you want to use
        # return sentiment_score(searcher.stored_fields(docnum), score)
        return sentiment_score2(searcher.stored_fields(docnum), score)


class SentimentModelTFIDF(TF_IDF):
    use_final = True

    def final(self, searcher, docnum, score):
        # Uncomment the score method you want to use
        # return sentiment_score(searcher.stored_fields(docnum), score)
        return sentiment_score2(searcher.stored_fields(docnum), score)


class Word2VecModel(BM25F):
    pass