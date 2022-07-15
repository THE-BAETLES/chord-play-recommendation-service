from injector import Module
from pymongo import MongoClient
from dotenv import dotenv_values
from urllib.parse import quote_plus

config = {
    **dotenv_values(".env.development")
}

class MongoModule(Module):
    def __init__(self) -> None:
        pass
    
class MongoService:
    def __init__(self) -> None:
        self.client = self.get_mongo_client()
        
    def get_mongo_client(self):
        user = config['MONGO_USER']
        password = config['MONGO_PASSWORD']
        host = config['MONGO_HOST']
        uri = "mongodb://%s:%s@%s" % (quote_plus(user), quote_plus(password), quote_plus(host))
        
        client = MongoClient(uri)
        
        return client
    
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(MongoService, self).__new__(self)
            return self.instance        
    
    def __call__(self):
        return self.client
        