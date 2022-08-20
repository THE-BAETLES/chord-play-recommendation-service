from injector import inject
from pymongo import MongoClient


class TestService: 
    @inject
    def __init__(self, db: MongoClient):
        self.db = db['chordplay']
    
    def write_test(self):
        insert = self.db['TEST'].insert_one({'test':'test'})
        print(insert)    
        
    def read_test(self):
        read = self.db['TEST'].find({})
        print(read)
    
    