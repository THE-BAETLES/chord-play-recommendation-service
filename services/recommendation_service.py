import os
from bson import DBRef, ObjectId
from injector import Module, provider, Injector, inject, singleton
from pymongo import MongoClient
from typing import Dict, List


class RecommendationService: 
    @inject
    def __init__(self, db: MongoClient):
        self.db = db['chordplay']
    
    def test(self):
        return self.db['WATCH_HISTORY'].find({'user': DBRef('USER', ObjectId('62e50e3b74b7f274bb324516'))})[0]['play_count']
    
    def find_all_video_id(self):     
        video_id_list = list(map(lambda x: x['_id'], self.db['VIDEO'].find()))
        
        return video_id_list
    
    def get_lower_tags(self,video_id):
        video_collection = self.db['VIDEO']
        tags = list(map(lambda x: x['tags'] if 'tags' in x.keys() else '',video_collection.find({'_id': video_id})))
        if len(tags) == 0:
            return ['']
        tags = tags[0]
        lower_tags = list(map(lambda x: x.lower(), tags))
        return lower_tags
    
    def update_tag_map(self, user_tag_map, video_id, addCount):
        tags = self.get_lower_tags(video_id)
        for tag in tags:
            if tag not in user_tag_map.keys():
                user_tag_map[tag] = addCount
                continue
                
            user_tag_map[tag] += addCount

    def create_watch_history_user_tag_map(self, user_tag_map, user_id: str):
        watch_history_collection = self.db['WATCH_HISTORY']
        watch_info_list = watch_history_collection.find({'user': DBRef('USER', ObjectId(f'{user_id}'))}).sort("last_played", -1)
        
        for watch_info in watch_info_list[:40]:
            video_id = watch_info['video'].id
            count = watch_info['play_count']
            self.update_tag_map(user_tag_map, video_id, count)
                                
    def create_signup_favorite_user_tag_map(self, user_tag_map, user_id: str):
        user_db = self.db['USER']
        
        user_signup_favorite_list = []
        user_table = user_db.find_one({'_id': ObjectId(user_id)})
        
        if 'signup_favorite' in user_table.keys():
            user_signup_favorite_list: List[str]= user_db.find_one({'_id': ObjectId(user_id)})['signup_favorite']
        
        for video_id in user_signup_favorite_list:
            self.update_tag_map(user_tag_map, video_id, 1)
    
    def get_user_tag_map(self, user_id: str):
        user_tag_map = {}
        self.create_signup_favorite_user_tag_map(user_tag_map,user_id)
        self.create_watch_history_user_tag_map(user_tag_map, user_id)
        return user_tag_map
    
    def get_recommendation_list(self, user_id: str, offset: int,limit=40) -> List[str]:
        user_tag_map = self.get_user_tag_map(user_id)
        video_id_list = self.find_all_video_id()
        
        candidate_music = []
        
        for video_id in video_id_list:
            candidate_music.append(self.get_jaccard_sim(user_tag_map, video_id))
            
        sorted_candidate_music = sorted(candidate_music, key=lambda x: -x['jaccard_sim'])
        
        candidate_music_length = len(sorted_candidate_music)        
        # To avoid out of index error
        
        start_index = min(int(offset), candidate_music_length)
        limit_index = min(candidate_music_length, int(offset)+int(limit))
        
        return sorted_candidate_music[start_index:limit_index]

    def get_jaccard_sim(self, user_tag_map, video_id):
        tags = self.get_lower_tags(video_id)
        weight_sum = 0
        for tag in tags:
            if tag in user_tag_map.keys():
                weight_sum += user_tag_map[tag]
        
        user_tag_map_length = len(user_tag_map.keys()) if len(user_tag_map.keys()) != 0 else 987654321
        jaccard_sim = weight_sum / user_tag_map_length
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