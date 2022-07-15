import numpy as np
import os
from injector import Module, provider, Injector, inject, singleton
from pymongo import MongoClient
from typing import Dict, List


class RecommendationService: 
    @inject
    def __init__(self, db: MongoClient):
        self.db = db
        
    
    def get_tag_distance(self):
        
        pass
    
    def find_all(self):
        pass
    
    
    def find_one(self):
        pass
    
    def find_all_video_tags(self) -> Dict[str, List[str]]:
        """_summary_
        

        Returns:
            Dict[str, int]: 전처리된 tag, 해당 tag의 개수
        """
        pass
    
    def tags_to_dict(self):
        pass
    
    def find_user_video_tags(self):
        pass
    

    def get_user_video_tag_map(self, limit=1000):
        """_summary_
        Find users tag map limit means recently watch_list
        태그 찾고 -> 태그 전처리 -> 
        Args:
            limit (int, optional): _description_. Defaults to 1000.
        """
        pass
    def get_recommendation_list(self, ):
        
        video_tag_map = self.find_all_video_tags()
        user_tag_map = self.get_user_video_tag_map()
        
        return         
        
    
    
    
    
    
    