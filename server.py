from injector import Injector
from configs.config import get_development_config
from services.mongo_service import MongoModule
from services.recommendation_service import RecommendationService
import dotenv
from flask import Flask, app, jsonify, request
import os
from typing import List
from fastapi import FastAPI
dotenv.load_dotenv("development.env")
app = FastAPI()

listen_port = os.environ.get("SERVER_PORT")

injector = Injector([get_development_config, MongoModule()])
service = injector.get(RecommendationService)
print(f"[Recommendation Server] start listen on {listen_port}")

@app.get('/test')
async def test(): 
    recommendation_list = service.find_all_video_id()
    print(recommendation_list)
    return "hello"

@app.get('/recommendation/{user_id}')
async def recommendation(user_id: str, offset: int, limit: int) -> List[str]:
    offset = int(offset)
    limit = int(limit)
    recommendation_list = service.get_recommendation_list(user_id, offset, limit)
    recommendation_video_id = list(map(lambda x: x['video_id'], recommendation_list))
    response = {
        'payload': {
            'number': limit,
            'recommendation_list':  recommendation_video_id
        }
    }
    return jsonify(response)
    
    
