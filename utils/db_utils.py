import sys
sys.path.append(".")
import pymongo
import config
from bson.objectid import ObjectId

class MongoDb:
    def __init__(self):
        self.get_connection()
        pass

    def get_connection(self):
        """
        This will create a connection to mongodb.
        """
        MONGODB_URI = config.MONGODB_URI
        self.client = pymongo.MongoClient(MONGODB_URI, ssl=False)

    def close_connection(self):
        """This will close the connection to Mongo
        """
        self.client.close()

    def add_entry(self, docs):
        """
        CREATES MONGODB ENTRY FOR A LIST OF DOC
        """
        try:
            try:
                self.client[config.MONGO_JOB_DB][config.MONGO_JOB_META_COLLECTION].insert(docs)
            except:
                self.get_connection()
                self.client[config.MONGO_JOB_DB][config.MONGO_JOB_META_COLLECTION].insert(docs)
        except:
            raise
