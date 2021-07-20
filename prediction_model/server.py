import numpy as np
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import pickle, sys
from models import Model


app = Flask(__name__)
api = Api(app)

with open('model.p', 'rb') as file:
    model = pickle.load(file)

with open('lat_dict.p', 'rb') as file:
    lat_dict = pickle.load(file)

with open('lng_dict.p', 'rb') as file:
    lng_dict = pickle.load(file)

gender_encode = {'Male': 0, 'Female': 1, 'Unknown': 0}

mean_lat = lat_dict.pop('KeyError')
mean_lng = lng_dict.pop('KeyError')

max, min = max(lng_dict.keys()), min(lng_dict.keys())


class Result(Resource):
    '''
    resourceful routing from Flask-RESTful service
    '''
    def get(self):
        gender = request.args.get('gender')
        age = request.args.get('age')
        stationId = request.args.get('id')
        flag = 0

        try:
            lat = lat_dict[int(stationId)]
            lng = lng_dict[int(stationId)]

        except:
            # when user keyed in station ID not in the data
            flag = 1
            lat = mean_lat
            lng = mean_lng

        X = [float(age), float(lat), float(lng), float(gender_encode[gender])]

        pred = np.dot(X, model.weight) + model.bias

        if flag: # the case to enlighten the user as it emits a compromising prediction
            return jsonify({'Minimum and Maximum station IDs the Data Accepts': [min, max],
                             'Duration of Ride Estimated for average lat/lng': pred[0]
                            })

        return jsonify({'Given': {'age': age,
                                  'gender': gender,
                                  'station ID': stationId
                                  },
                        'Duration of Ride Predicted based on the Model': pred[0]})

if __name__ == '__main__':
    api.add_resource(Result, '/parameters')

    app.run(host='0.0.0.0', port=8000, debug=True)
