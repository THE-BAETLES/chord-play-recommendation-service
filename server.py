from injector import Injector
from configs.config import get_development_config
from services.mongo_service import MongoModule
from services.recommendation_service import RecommendationService
import dotenv
from flask import Flask, app, jsonify, request
import os
from typing import List

dotenv.load_dotenv("development.env")

global service

app = Flask(__name__)

listen_port = os.environ.get("SERVER_PORT")

@app.route('/recommendation/<user_id>', methods=["GET"])
def recommendation() -> List[str]:
    request_params = request.args.to_dict()
    user_id = request.view_args['user_id']
    offet = request_params["offset"]
    limit = request_params["limit"]
    
    
    recommendation_list = service.get_recommendation_list(user_id, int(limit))
    recommendation_video_id = list(map(lambda x: x['video_id'], recommendation_list))
    
    response = {
        'payload': {
            'number': limit,
            'recommendation_list':  recommendation_video_id
        }
    }
    
    return jsonify(response)
    
if __name__ == '__main__':
    injector = Injector([get_development_config, MongoModule()])
    # print({**dotenv_values("development.env")})
    service = injector.get(RecommendationService)
    print(f"[Recommendation Server] start listen on {listen_port}")
    app.run(host='0.0.0.0', port=listen_port)