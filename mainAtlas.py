from pymongo import MongoClient
import certifi
import pprint
 
from src.mongo_query import mongo_query
from src.schema import get_atlas_schema

__version__ = "0.0.0"
__license__ = "MIT"

USERNAME = "XXX"
PASSWORD = "XXX"

def mainAtlas():
    # connect to MongoDB Atlas
    cluster = f"mongodb+srv://{USERNAME}:{PASSWORD}@sandbox.XXX.mongodb.net/Library?retryWrites=true&w=majority"
    client = MongoClient(cluster, tlsCAFile=certifi.where())
    db = client.DATABASE #DATABASE replace with database name

    selection = "COLLECTION" #COLLECTION replace with collection name

    collection = db[f"{selection}"]
    schema_result = get_atlas_schema(collection)

    xPath = ''
    filter = ()
    projection = dict()

    xPath = input("XPath Query: ")
    filter, projection = mongo_query(xPath, schema_result)
    
    results = collection.find(filter, projection)
    for result in results:
        pprint.pprint(result)

if __name__ == "__main__":
    mainAtlas()
