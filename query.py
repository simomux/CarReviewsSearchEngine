# Controls and UI modules
import argparse
import time
import blessed

# Query modules
from whoosh.qparser import MultifieldParser  # , QueryParser
from whoosh.qparser.plugins import FuzzyTermPlugin
import custom_model
from whoosh.scoring import BM25F

# Word2Vec modules
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
from whoosh import index
from whoosh.analysis import StemmingAnalyzer

# Create terminal for UI management
term = blessed.Terminal()


def uiPrint():
    print("\n")
    # Show syntax of Full-text queries
    syntax = input(term.orangered("See syntax of queries? (y/n) "))
    if syntax.lower().strip() == "y":
        print("\nFull-text search: word1 word2")
        print("Phrasal search: \"word1 word2\"")
        print("Wildcard search: word*")
        print("Range search: [word1 TO word2]")
        print("Proximity search: \"word1 word2\"~N")
        print("Boolean search: word1 AND word2")
        print("Fuzzy search: word~")
        print("Digit 0 for exit")


def printResults(results):
    # Print query results
    for hit in results:
        print(f"File: {hit['file']}")
        print(f"Title: {hit['title']}")
        print(f"Author: {hit['author']}")
        print(f"Made on: {hit['date'].date()}")
        print(f"Matches: {hit.matched_terms()}")
        print(f"Sentiment: {hit['sentiment']}, {hit['sentiment_value']}")

        print(f"Score: {round(hit.score, 4)}")
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
    # Argument control
    parser = argparse.ArgumentParser("Whoosh Query")
    parser.add_argument(dest='indexdir', metavar="DIRECTORY", help="The directory of the index")
    ix = index.open_dir(parser.parse_args().__getattribute__('indexdir'))  # Open index directory

    with ix.searcher(weighting=custom_model.SentimentModel) as searcher:
        # Boosts score if query arguments are found in metadate of review
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

            query_text = input(term.orangered("\n\nInsert the query: "))

            if query_text == "0":
                break

            query = query_parser.parse(query_text)

            results = searcher.search(query, limit=10, terms=True)
            if len(results) == 0:
                print("No results found")

                #  Did you mean?
                didyoumean_choice = input(term.orangered("\n\nDid you mean? (y/n) "))
                if didyoumean_choice.lower().strip() == "y":
                    try:
                        new_query = searcher.correct_query(query, query_text)
                    except (ValueError, TypeError, AttributeError) as e:
                        # Some queries with exact matches and long numbers don't work with searcher.correct_query()
                        # method because of the type they get converted to by the query_parser
                        print("Impossible to correct query with this syntax!\n")
                        time.sleep(1)
                        continue

                    print(f"New query: {new_query.string}")

                    # Check if the query is different from the original one
                    if new_query.string == query_text:
                        print("Couldn't find a correct version of the query")
                        continue
                    results = searcher.search(new_query.query, limit=10, terms=True)

                    if len(results) == 0:
                        print("No results found with the new query")
                        continue

                    # Allow did you mean results to get sorted
                    query = new_query.query

            print(term.orangered('\nRESULTS:') + str(len(results)))
            # Gives time to see results number
            time.sleep(2)
            printResults(results)

            # Sort results by Word2Vec
            # Still need to be optimized
            choice = input(term.orangered("\nDo you want to sort results by similarity? (y/n) "))
            if choice.lower().strip() == "y":
                # Load pre-trained Word2Vec model
                model_path = '../progettoGestione/GoogleNews-vectors-negative300.bin'
                model = KeyedVectors.load_word2vec_format(model_path, binary=True)  # limit=1000000)

                results = searcher.search(query, limit=None, terms=True)
                word2vec(results, query_text)
