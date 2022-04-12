import json

from src.theme.colors import text_colors 
from src.mongo_query import mongo_query
from src.schema import get_schema
from src.queries.queries import bookstore_queries, library_queries, query_classifier

__version__ = "1.0.0"
__license__ = "MIT"

def selection_collection(collection_input):
    if (collection_input == 1):
        return 'library'
    else:
        return "bookstore"

def main():
    # Choose either Library or Bookstore database
    collection_input = int(input("1. Library \n2. Bookstore\nSelect collection(1 or 2): "))
    selection = selection_collection(collection_input)
    queries = library_queries if collection_input == 1 else bookstore_queries

    collection = None
    f = None

    if collection_input == 1:
        f = open("src/sample/library.json", "r")
    else:
        f = open("src/sample/Bookstore.json", "r")

    collection = json.load(f)
    schema_result = get_schema(collection)

    xPath = ''
    filter = ()
    projection = dict()

    query_option = int(input("1. Sample Queries \n2. DIY\nSelect the following options (1 or 2): "))
    if query_option == 1: 
        print(f"QUERY TYPE\n---------------------------------------")
        index = 1
        for key in queries.keys():
            print(f"{text_colors.HEADER}{index}: {key}{text_colors.HEADER} {text_colors.ENDC}")
            index += 1
        print("---------------------------------------")
        xPathType = query_classifier[int(input("Choose your query type: "))]

        print(f"QUERIES\n---------------------------------------")
        for key, query in queries[xPathType].items():
            print(f"{text_colors.OKCYAN}{key}: {query}{text_colors.OKCYAN} {text_colors.ENDC}")
        print("---------------------------------------")
        xPath = int(input("Choose your query: "))

        filter, projection = mongo_query(queries[xPathType][xPath], schema_result)
    else:
        xPath = input("XPath Query: ")
        filter, projection = mongo_query(xPath, schema_result)
    
    if projection != 'Invalid Syntax':
        print(f"query: {text_colors.OKGREEN}{filter} {projection}{text_colors.OKGREEN} {text_colors.ENDC}\n")

    else:
        print(f"\n{text_colors.FAIL}Invalid Syntax{text_colors.FAIL} {text_colors.ENDC}")

if __name__ == "__main__":
    main()
