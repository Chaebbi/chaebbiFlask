
from flask import request, jsonify, current_app, Response, g
from flask.json import JSONEncoder
from functools import wraps
import os
from werkzeug.utils import secure_filename

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)


def create_endpoints(app, services):
    app.json_encoder = CustomJSONEncoder

    foodService = services.foodService
    foodclassService = services.foodClassService

    @app.route("/ping", methods=['GET'])
    def ping():
        return "pong"

    @app.route("/api/foodrecommend", methods=['POST'])
    def recommend():

        return foodService.foodRecommend(request.get_json()['ingredients'])

    @app.route("/api/foodpredict", methods=['POST'])
    def predict():
        f = request.files['file']
        filename = secure_filename(f.filename)
        #f.save(os.path.join('./static/', filename))    #local 에서 돌릴떈 이 코드
        f.save(os.path.join('/home/ec2-user/app/ae_FlaskServer/static/', filename))     #EC2에서 돌릴땐 이코드
        print('>>>파일이 저장되었습니다')
        #이미지 분류 service
        food_type = foodclassService.predictFood(filename)
        # 분류된 이미지의 영양정보 조회 service
        return foodclassService.foodNutrient(food_type)






