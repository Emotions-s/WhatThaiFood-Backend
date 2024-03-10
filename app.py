import os
import base64
import imghdr

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from util.process_image import prepare_image
from util.prediction import predict
from service.food import get_foods

app = Flask(__name__)
api = Api(app)

class Model(Resource):
    def post(self):
        image_type = request.form['image_type']

        if image_type == '':
            return {"error": "Image type required1."}, 400

        if not image_type.isnumeric():
            return {"error": "Image type incorrect2."}, 400

        if int(image_type) < 1 or int(image_type) > 3:
            return {"error": "Image type incorrect3."}, 400

        image_base64 = request.form['image']

        if image_base64 == '':
            return {"error": "Image required."}, 400

        try:
            image_data = base64.b64decode(image_base64)
        except Exception as e:
            return {'error': 'Invalid Base64 data'}, 400

        allow_file_type = ["jpg", "jpeg"]

        file_type = imghdr.what(None, h=image_data)
        if file_type not in allow_file_type:
            return {"error": "file type not allow."}

        image = prepare_image(image_data)

        result = predict(image_type, image)

        index_list = [index[0] for index in result]
        foods_list = get_foods(image_type, index_list)

        response_list = []
        for i in range (len(foods_list)):
            tmp = {
                'name': foods_list[i][2],
                'description': foods_list[i][3],
                'ingredients': foods_list[i][4],
                'google_link': foods_list[i][5],
                'image_url': foods_list[i][6],
                'probability': '{:.2f}%'.format(result[i][1])
            }
            response_list.append(tmp)

        return jsonify(response_list)

api.add_resource(Model, '/predict')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)