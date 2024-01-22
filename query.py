from whoosh import index
from whoosh.qparser import MultifieldParser  # , QueryParser
from whoosh.scoring import BM25F
#  from whoosh.qparser.dateparse import DateParserPlugin
from whoosh.qparser.plugins import FuzzyTermPlugin
from sentiment import sentiment_analysis


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
            print(f"Sentiment: {hit['sentiment_value']}")
        elif choice.lower().strip() != "y":
            print(f"Score: {round(hit.score, 2)}")

        print("---------------\n")


if __name__ == "__main__":

    index = 'indexdir'
    ix = index.open_dir(index)  # Open index directory
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

            # if index == 'sentiment_index':
            choice = input("Do you want to sort the results by their sentiment? (y/n) ")
            if choice.lower().strip() == "y":
                sorting = input("Do you want to sort the results by best or worst? (b/w) ")

                # Specify the sorting order based on the user's choice
                if sorting.lower().strip() == "b":
                    results = searcher.search(query, limit=10, sortedby="sentiment_value", reverse=True, terms=True)
                    printResults(results, sorting)

                elif sorting.lower().strip() == "w":
                    results = searcher.search(query, limit=10, sortedby="sentiment_value", terms=True)
                    printResults(results, sorting)

                else:
                    print("Invalid")
