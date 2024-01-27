# Controls and UI modules
import argparse
import time
import blessed

# Query modules
from whoosh.qparser import MultifieldParser  # , QueryParser
from whoosh.qparser.plugins import FuzzyTermPlugin
import custom_model
# from whoosh.scoring import BM25F

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
        print(f"Rating: {hit['rating']}")
        print(f"Made on: {hit['date'].date()}")
        print(f"Matches: {hit.matched_terms()}")
        print(f"Sentiment: {hit['sentiment_type']}, {hit['sentiment_value']}")

        print(f"Score: {round(hit.score, 4)}")
        print("---------------\n")


if __name__ == "__main__":
    # Argument control
    parser = argparse.ArgumentParser("Whoosh Query")
    parser.add_argument(dest='indexdir', metavar="DIRECTORY", help="The directory of the index")
    ix = index.open_dir(parser.parse_args().__getattribute__('indexdir'))  # Open index directory

    with ix.searcher(weighting=custom_model.FullTextModel) as searcher:
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
