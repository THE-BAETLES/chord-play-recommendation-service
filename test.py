import os
from fastapi import FastAPI
import dotenv
from injector import Injector
from configs.config import get_development_config
from services.mongo_service import MongoModule
from services.recommendation_service import RecommendationService
from services.test_service import TestService


dotenv.load_dotenv("development.env")
app = FastAPI()

listen_port = os.environ.get("SERVER_PORT")

injector = Injector([get_development_config, MongoModule()])
service = injector.get(TestService)

@app.get('/test')
async def test():
    service.write_test()
    service.read_test()
    pass

@app.get('/healthCheck')
async def health_check():
    return "I`m Healthy now"