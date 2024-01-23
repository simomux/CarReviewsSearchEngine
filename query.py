import os
from whoosh import index
from whoosh.qparser import MultifieldParser  # , QueryParser
from whoosh.scoring import BM25F
from whoosh.sorting import FieldFacet
#   from whoosh.qparser.dateparse import DateParserPlugin
from whoosh.qparser.plugins import FuzzyTermPlugin
from sentiment import sentiment_analysis
import argparse

# Word2Vec modules
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
from whoosh.analysis import StemmingAnalyzer


def uiPrint():
    print("\n")
    # Show syntax of Full-text queries
    syntax = input("See syntax of queries? (y/n) ")
    if syntax.lower().strip() == "y":
        print("\nFull-text search: word1 word2")
        print("Phrasal search: \"word1 word2\"")
        print("Wildcard search: word*")
        print("Range search: [word1 TO word2]")
        print("Proximity search: \"word1 word2\"~N")
        print("Boolean search: word1 AND word2")
        print("Fuzzy search: word~")
        print("Digit 0 for exit")


def printResults(results, choice="n"):
    # Print query results
    print(f"\nRESULTS: {len(results)}\n")
    for hit in results:
        print(f"Path: {hit['file']}")
        print(f"Title: {hit['title']}")
        print(f"Author: {hit['author']}")
        print(f"Made on: {hit['date'].date()}")
        print(f"Terms: {hit.matched_terms()}")
        if choice.lower().strip() == "b" or choice.lower().strip() == "w":
            print(f"Sentiment: {round(hit['sentiment_value'], 5)}")
        elif choice.lower().strip() != "y":
            print(f"Score: {round(hit.score, 2)}")

        print("---------------\n")


def word2vec(results, query):
    # Tokenize and preprocess reference text
    analyzer = StemmingAnalyzer()
    tokens_reference = [token.text for token in analyzer(query) if token.text.lower() in model]
    vector_reference = model[tokens_reference].mean(axis=0) if tokens_reference else None

    # Calculate similarity scores for each text
    similarity_scores = []
    for result in results:
        text = result['content']
        tokens_text = [token.text for token in analyzer(text) if token.text.lower() in model]
        vector_text = model[tokens_text].mean(axis=0) if tokens_text else None

        if vector_reference is not None and vector_text is not None:
            similarity_score = cosine_similarity([vector_reference], [vector_text])[0][0]
            # model.cosine_similarities(vector_reference, [vector_text])
            similarity_scores.append((result['file'], similarity_score))
        else:
            similarity_scores.append((result['file'], None))

    # Sort based on similarity scores (higher scores first)
    sorted_texts = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Display the sorted texts
    for text, similarity_score in sorted_texts[:10]:
        print(f"Similarity Score: {similarity_score:.4f} - {text}")

    '''
    analogy_result = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
    print(f"Word most similar to 'king - man + woman': {analogy_result[0][0]}")
    print(model.doesnt_match(['fire', 'water', 'land', 'sea', 'air', 'car']))
    '''


if __name__ == "__main__":
    print("\033[2J\033[;H", end='')
    parser = argparse.ArgumentParser("Whoosh Query")
    parser.add_argument(dest='sentiment_indexdir', metavar="DIRECTORY", help="The directory of the index")

    ix = index.open_dir(parser.parse_args().__getattribute__('sentiment_indexdir'))  # Open index directory
    bm25f = BM25F(B=0.1, K1=2)
    with ix.searcher(weighting=bm25f) as searcher:
        boost = {
            "maker": 2,
            "model": 2,
            "year": 2,
            "content": 1,
        }

        query_parser = MultifieldParser(["content", "maker", "model", "year"], fieldboosts=boost, schema=ix.schema)
        query_parser.add_plugin(FuzzyTermPlugin)

        while True:
            uiPrint()

            query_text = input("\nInsert the query: ")

            if query_text == "0":
                break

            query = query_parser.parse(query_text)

            results = searcher.search(query, limit=10, terms=True)
            if len(results) == 0:
                print("No results found")

                #  Did you mean?
                didyoumean_choiche = input("\nDid you mean? (y/n) ")
                if didyoumean_choiche.lower().strip() == "y":
                    try:
                        new_query = searcher.correct_query(query, query_text)
                    except Exception as e:
                        print("Impossible to correct query with this syntax!\n")
                        continue

                    print(f"New query: {new_query.string}")

                    # Check if the query is different from the original one
                    if new_query.string == query_text:
                        print("No results found")
                        continue
                    results = searcher.search(new_query.query, limit=10, terms=True)

                    if len(results) == 0:
                        print("No results")
                        continue

                    # Allow did you mean results to get sorted by date
                    query = new_query.query

            # Sorting by date
            choice = input("Do you want to sort results by most recent date? (y/n) ")
            if choice.lower().strip() == "y":
                results = searcher.search(query, limit=10, sortedby="date", reverse=True, terms=True)
            printResults(results, choice)

            # Get sentiment of top 10 values
            choice = input("Do you want to get the sentiment of the top 10 full-text query? (y/n) ")
            if choice.lower().strip() == "y":
                sentiment_analysis(results)

            # Sorting by sentiment
            choice = input("Do you want to sort the results by their sentiment? (y/n) ")
            if choice.lower().strip() == "y":
                sorting = input("Do you want to sort the results by best or worst? (b/w) ")

                # Specify the sorting order based on the user's choice
                if sorting.lower().strip() == "b":
                    sorting_fields = FieldFacet("sentiment_value", reverse=True)
                    results = searcher.search(query, limit=10, sortedby=sorting_fields, terms=True)
                    printResults(results, sorting)

                elif sorting.lower().strip() == "w":
                    sorting_fields = FieldFacet("sentiment_value")
                    results = searcher.search(query, limit=10, sortedby=sorting_fields, terms=True)
                    printResults(results, sorting)

                else:
                    print("Invalid")

            # Still need to be optimized
            choice = input("Do you want to sort results by similarity? (y/n) ")
            if choice.lower().strip() == "y":
                # Load pre-trained Word2Vec model
                model_path = '../progettoGestione/GoogleNews-vectors-negative300.bin'
                model = KeyedVectors.load_word2vec_format(model_path, binary=True)  # limit=1000000)

                results = searcher.search(query, limit=None, terms=True)
                word2vec(results, query_text)
