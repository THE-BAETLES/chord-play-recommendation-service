from injector import Module, provider, singleton
from pymongo import MongoClient
from dotenv import dotenv_values
from urllib.parse import quote_plus
from configs.config import Configuration

class MongoModule(Module):
    @singleton
    @provider
    def provide_mongo_connection(configuration: Configuration) -> MongoClient:
        user = configuration['MONGO_USER']
        password = configuration['MONGO_PASSWORD']
        host = configuration['MONGO_HOST']
        database = configuration['MONGO_DATABASE']
        port = configuration['MONGO_PORT']
        
        uri = "mongodb://%s:%s@%s:%s/%s" % (user), (password), (host), (port) ,(database)
        client = MongoClient(uri)
        
        return client

        