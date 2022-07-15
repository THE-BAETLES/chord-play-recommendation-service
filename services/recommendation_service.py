import numpy as np
import os
from injector import Module, provider, Injector, inject, singleton
from pymongo import MongoClient
from typing import Dict, List


class RecommendationService: 
    @inject
    def __init__(self, db: MongoClient):
        self.db = db
        
    def find_all_video_id(self):     
        video_id_list = list(map(lambda x: x['_id'], self.db['VIDEO'].find()))
        
        return video_id_list

    def get_recommendation_list(self, user_id, limit=40) -> List[str]:
        user_tag_map = self.get_user_tag_map(user_id)
        video_id_list = self.find_all_video_id()
        
        candidate_music = []
        for video_id in video_id_list:
            candidate_music.append(self.get_jaccard_sim(user_tag_map, video_id))
        
        sorted_candidate_music = sorted(candidate_music, key=lambda x: -x['jaccard_sim'])
        
        return sorted_candidate_music[0:limit]

    def get_jaccard_sim(self, user_tag_map, video_id):
        tags = self.get_lower_tags(video_id)
        weight_sum = 0
        for tag in tags:
            if tag in user_tag_map.keys():
                weight_sum += user_tag_map[tag]
        
        jaccard_sim = weight_sum / len(user_tag_map.keys())
        return {
            'video_id': video_id,
            'jaccard_sim': jaccard_sim
        }

    def get_lower_tags(self, video_id):
        video_collection = self.db['VIDEO']
        tags = list(map(lambda x: x['tags'] if 'tags' in x.keys() else '',video_collection.find({'_id': video_id})))
        
        if len(tags) == 0:
            return ['']
        
        tags = tags[0]
        lower_tags = list(map(lambda x: x.lower(), tags))
        
        return lower_tags