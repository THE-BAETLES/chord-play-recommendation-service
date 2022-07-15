from injector import Injector
from configs.config import get_development_config
from services.mongo_service import MongoModule
from services.recommendation_service import RecommendationService
import dotenv
from flask import app, jsonify, request
import os
from typing import List
dotenv.load_dotenv()

global service

listen_port = os.environ.get("SERVER_PORT")

@app.route('/recommendation', methods=["GET"])
def recommendation() -> List[str]:
    request_params = request.args.to_dict()
    user_id = request_params["user_id"]
    number = request_params["number"]
    
    recommendation_list = service.get_recommendation_list(user_id, number)
    recommendation_video_id = list(map(lambda x: x['video_id'], recommendation_list))
    
    response = {
        'number': number,
        'recommendation_list':  recommendation_video_id
    }
    
    return jsonify(response)
    
if __name__ == '__main__':
    injector = Injector([get_development_config, MongoModule()])
    # print({**dotenv_values("development.env")})
    service = injector.get(RecommendationService)
    
    print(f"[Recommendation Server] start listen on {listen_port}")
    app.run(host='0.0.0.0', port=listen_port)