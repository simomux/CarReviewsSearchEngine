from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.scoring import BM25F
from whoosh.qparser.dateparse import DateParserPlugin

def search_results(results):
    if len(results) == 0:
            print("No results found")
            return
        
        # Print query results
    print(f"\nRESULTS: {len(results)}\n")
    for hit in results:
        print(f"Path: {hit['file']}")
        print(f"Made on: {hit['date'].date()}")
        print(hit['content'])
        print(f"Score: {round(hit.score,2)}")
        print("---------------\n")
  

if __name__ == "__main__":
    ix = index.open_dir("indexdir")  # Open index directory
    bm25f = BM25F(B=0.1, K1=2)
    with ix.searcher(weighting=bm25f) as searcher:
        print("Select the type of search:")
        print("1) Search on content")
        print("2) Search on Car Brand")
        print("3) Search on Car Model")
        print("4) Search on Car Year")
        print("5) Search on Review Date")
        input_type = input("\n\nAnswer: ")
        

        if input_type not in ["1", "2", "3", "4", "5"]:
            raise Exception('Invalid input type!')
        
        if input_type == "1":
            syntax = input("See syntax of queries? (y/n)\n")
            if syntax.lower().strip() == "y":
                print("\nFull-text search: 'word1 word2'")
                print("Phrasal search: \"word1 word2\"")
                print("Wildcard search: 'word*'")
                print("Range search: '[word1 TO word2]'")
                print("Proximity search: \"word1 word2\"~N")
                print("Boolean search: 'word1 AND word2'")
                print("Fuzzy search: 'word~'")

        query_text = input("\nInsert the query:")

        # Search on content
        if input_type == "1":
            query_parser = QueryParser("content", schema=ix.schema)
            query = query_parser.parse(query_text)
            results = searcher.search(query, limit=10)  # limit=None, filter=True
            search_results(results)
        
        # Search on car brand
        elif input_type == "2":
            query_parser = QueryParser("auto", schema=ix.schema)
            query = query_parser.parse(query_text)
            results = searcher.search(query, limit=10)
            search_results(results)
        
        # Search on car model
        elif input_type == "3":
            # TODO: Implement search by model
            search_results(results)
        
        # Search on car year
        elif input_type == "4":
            # TODO: Implement search by year
            search_results(results)
        
        # Search on review date
        elif input_type == "5":
            query_parser = QueryParser("date", schema=ix.schema)
            query_parser.add_plugin(DateParserPlugin())
            query = query_parser.parse(query_text)
            results = searcher.search(query, limit=10) 
            search_results(results) 
    