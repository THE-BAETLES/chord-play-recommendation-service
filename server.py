from injector import Injector
from configs.config import get_development_config
from services.mongo_service import MongoModule
from services.recommendation_service import RecommendationService

if __name__ == '__main__':
    injector = Injector([get_development_config, MongoModule()])
    # print({**dotenv_values("development.env")})
    service = injector.get(RecommendationService)

    pass