from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.scoring import BM25F
from whoosh.qparser.dateparse import DateParserPlugin
from datetime import datetime

def search_results(results):
    if len(results) == 0:
            print("No results found")
            return
        
        # Print query results
    print("\nRESULTS:\n")
    for hit in results:
        print(f"Path: {hit['file']}")
        print(hit['content'])
        print(f"Score: {round(hit.score,2)}")
        print("---------------\n")
  

if __name__ == "__main__":
    ix = index.open_dir("indexdir")  # Open index directory
    bm25f = BM25F(B=0.1, K1=2)
    with ix.searcher(weighting=bm25f) as searcher:
        print("Select the type of search:")
        print("1) Search on content (Full-text search, Phrasal search, Wildcard search, Range search)")
        print("2) Search on Car Brand")
        print("3) Search on Car Model")
        print("4) Search on Car Year")
        print("5) Search on Review Date")
        print("\n\nAnswer: ")
        input_type = input()
        

        if input_type not in ["1", "2", "3", "4", "5"]:
            raise Exception('Invalid input type!')

        print("Insert the query:")
        query_text = input()

        if input_type == "1":
            query_parser = QueryParser("content", schema=ix.schema)
            query = query_parser.parse(query_text)
            results = searcher.search(query, limit=10)  # limit=None, filter=True
            search_results(results)
        elif input_type == "2":
            query_parser = QueryParser("auto", schema=ix.schema)
            query = query_parser.parse(query_text)
            results = searcher.search(query, limit=10)
            search_results(results)
        elif input_type == "3":
            # TODO: Implement search by model
            search_results(results)
        elif input_type == "4":
            # TODO: Implement search by year
            search_results(results)
        elif input_type == "5":
            query_parser = QueryParser("date", schema=ix.schema)
            query_parser.add_plugin(DateParserPlugin())
            query = query_parser.parse(query_text)
            print("Invalid date format!")
            results = searcher.search(query, limit=10) 
            search_results(results) 
    