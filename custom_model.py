from whoosh.scoring import BM25F


def sentiment_score(doc, score):
    return score * doc['sentiment_value']


class FullTextModel(BM25F):
    def __init__(self):
        super().__init__(B=0.1, K1=2)


class SentimentModel(FullTextModel):

    def final(self, searcher, docnum, score):
        return sentiment_score(searcher.store_fields(docnum), score)


class Word2VecModel(BM25F):
    def __init__(self):
        super().__init__(self)
