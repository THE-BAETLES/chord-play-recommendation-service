from injector import Module, provider, singleton
from pymongo import MongoClient
from dotenv import dotenv_values
from urllib.parse import quote_plus
from configs.config import Configuration

class MongoModule(Module):
    @singleton
    @provider
    def provide_mongo_connection(self, configuration: Configuration) -> MongoClient:
        print("[MONGO_CLIENT_CONNECTION] start")
        user = configuration.config['MONGO_USER']
        password = configuration.config['MONGO_PASSWORD']
        host = configuration.config['MONGO_HOST']
        replicaset = configuration.config['MONGO_REPLICASET']
        uri = f"mongodb://{user}:{password}@{host}/?replicaSet={replicaset}&readPreference=primary"
        print("uri = ", uri)
        print("[MONGO_CLIENT_CONNECTION] end")
        client = MongoClient(uri)
        return client

        