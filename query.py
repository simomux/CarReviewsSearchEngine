from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.scoring import BM25F
from whoosh.qparser.dateparse import DateParserPlugin
from whoosh.qparser.plugins import FuzzyTermPlugin


if __name__ == "__main__":
    ix = index.open_dir("indexdir")  # Open index directory
    bm25f = BM25F(B=0.1, K1=2)
    with ix.searcher(weighting=bm25f) as searcher:
        print("Select the type of search:")
        print("1) Search on content")
        print("2) Search on Car Maker")
        print("3) Search on Car Model")
        print("4) Search on Car Year")
        print("5) Search on Review Date")
        input_type = input("\n\nAnswer: ")
        
        # Dictionary to manage input options
        input_options = {
            "1": "content",
            "2": "maker",
            "3": "model",
            "4": "year",
            "5": "date"
        }

        if input_type not in input_options.keys():
            raise Exception('Invalid input type!')
        
        query_parser = QueryParser(input_options[input_type], schema=ix.schema)

        # Show syntax of Full-text queries
        if input_type == "1":
            query_parser.add_plugin(FuzzyTermPlugin())
            syntax = input("See syntax of queries? (y/n)\n")
            if syntax.lower().strip() == "y":
                print("\nFull-text search: 'word1 word2'")
                print("Phrasal search: \"word1 word2\"")
                print("Wildcard search: 'word*'")
                print("Range search: '[word1 TO word2]'")
                print("Proximity search: \"word1 word2\"~N")
                print("Boolean search: 'word1 AND word2'")
                print("Fuzzy search: 'word~'")

            
        query_text = input("\nInsert the query: ")

        query = query_parser.parse(query_text)

        # Add date parser plugin in case of date search
        if input_type == "5":
            query_parser.add_plugin(DateParserPlugin())

        results = searcher.search(query, limit=10)
        if len(results) == 0:
            print("No results found")
            exit()

        choiche = input("Do you want to sort results by most recent date? (y/n)\n")
        if choiche.lower().strip() == "y":
            results = searcher.search(query, limit=10, sortedby="date", reverse=True)
        
        # Print query results
        print(f"\nRESULTS: {len(results)}\n")
        for hit in results:
            print(f"Path: {hit['file']}")
            print(f"Made on: {hit['date'].date()}")
            print(f"Score: {round(hit.score,2)}")
            print("---------------\n")
    