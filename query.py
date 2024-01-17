from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.scoring import BM25F
# from whoosh.qparser.dateparse import DateParserPlugin
from whoosh.qparser.plugins import FuzzyTermPlugin

def printResults(results, choice="n"):
    # Print query results
    print(f"\nRESULTS: {len(results)}\n")
    for hit in results:
        print(f"Path: {hit['file']}")
        print(f"Title: {hit['title']}")
        print(f"Author: {hit['author']}")
        print(f"Made on: {hit['date'].date()}")
        if choice.lower().strip() != "y":
            print(f"Score: {round(hit.score,2)}")
        print("---------------\n")



if __name__ == "__main__":
    ix = index.open_dir("indexdir")  # Open index directory
    bm25f = BM25F(B=0.1, K1=2)
    with ix.searcher(weighting=BM25F) as searcher:
        query_parser = QueryParser("content", schema=ix.schema)
        query_parser.add_plugin(FuzzyTermPlugin())

        while True:
            print("\n")
            # Show syntax of Full-text queries
            syntax = input("See syntax of queries? (y/n) ")
            if syntax.lower().strip() == "y":
                print("\nFull-text search: 'word1 word2'")
                print("Phrasal search: \"word1 word2\"")
                print("Wildcard search: 'word*'")
                print("Range search: '[word1 TO word2]'")
                print("Proximity search: \"word1 word2\"~N")
                print("Boolean search: 'word1 AND word2'")
                print("Fuzzy search: 'word~'")
                print("Digit 0 for exit")
            

            query_text = input("\nInsert the query: ")

            if query_text == "0":
                break

            query = query_parser.parse(query_text)

            results = searcher.search(query, limit=10)
            if len(results) == 0:
                print("No results found")

                # Did you mean?
                didyoumean_choiche = input("\nDid you mean? (y/n) ")
                if didyoumean_choiche.lower().strip() == "y":
                    try:
                        new_query = searcher.correct_query(query, query_text)
                    except TypeError:
                        print("Impossible to correct query with this syntax!\n")
                        continue
                    
                    print(f"New query: {new_query.string}")

                    # CHeck if the query is different from the original one
                    if new_query.string != query_text:
                        results = searcher.search(new_query.query, limit=10)
                        printResults(results)
                    else:
                        print("No results found")
            else:
                choice = input("Do you want to sort results by most recent date? (y/n) ")
                if choice.lower().strip() == "y":
                    results = searcher.search(query, limit=10, sortedby="date", reverse=True)

                printResults(results, choice)

