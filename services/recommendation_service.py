import os
from injector import Module, provider, Injector, inject, singleton
from pymongo import MongoClient
from typing import Dict, List


class RecommendationService: 
    @inject
    def __init__(self, db: MongoClient):
        # 
        print("reco start")
        self.db = db['chordplay']
    

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

    
    def get_user_tag_map(self, user_id: str):
        user_tag_map = {}
            
    #   sort by date
        watch_history_collection = self.db['WATCH_HISTORY']
        
        watch_info_list = watch_history_collection.find({'user_id': user_id}).sort("last_played", -1)
        
        for watch_info in watch_info_list[:min(40, len(watch_info_list))]:
            video_id = watch_info['video_id']
            count = watch_info['play_count']
            tags = self.get_lower_tags(video_id)
            for tag in tags:
                if tag not in user_tag_map.keys():
                    user_tag_map[tag] = count
                    continue
                    
                user_tag_map[tag] += count
                    
        return user_tag_map
    

    def get_recommendation_list(self, user_id: str, offset: int,limit=40) -> List[str]:
        user_tag_map = self.get_user_tag_map(user_id)
        video_id_list = self.find_all_video_id()
        
        candidate_music = []
        print("video_id_list = ", len(video_id_list))
        for video_id in video_id_list:
            candidate_music.append(self.get_jaccard_sim(user_tag_map, video_id))
        
        sorted_candidate_music = sorted(candidate_music, key=lambda x: -x['jaccard_sim'])
        
        print("sroted candidate", type(sorted_candidate_music))
    
        candidate_music_length = len(sorted_candidate_music)        
        # To avoid out of index error
        
        start_index = min(int(offset), candidate_music_length)
        limit_index = min(candidate_music_length, int(offset)+int(limit))
        
        print("start_index = ", start_index, "limit_index = ", limit_index)
        return sorted_candidate_music[start_index:limit_index]

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