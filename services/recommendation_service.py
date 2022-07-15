import numpy as np
import os
from injector import Module, provider, Injector, inject, singleton
from pymongo import MongoClient

class RecommendationService: 
    @inject
    def __init__(self, db: MongoClient):
        self.db = db
        print("Hello")
    

    