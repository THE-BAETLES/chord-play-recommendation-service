from injector import Module, provider, singleton
from pymongo import MongoClient
from dotenv import dotenv_values
from urllib.parse import quote_plus
from configs.config import Configuration

class MongoModule(Module):
    @singleton
    @provider
    def provide_mongo_connection(self, configuration: Configuration) -> MongoClient:
        user = configuration.config['MONGO_USER']
        password = configuration.config['MONGO_PASSWORD']
        host = configuration.config['MONGO_HOST']
        uri = "mongodb://%s:%s@%s" % (quote_plus(user), quote_plus(password), quote_plus(host))
        client = MongoClient(uri)
        
        return client

        