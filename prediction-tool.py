import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from flask import Flask
from flask_restful import Api, Resource, reqparse
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)


class Users(Resource):
    def get(self):
        data = pd.read_excel("data.xlsx")
        print(data.head())
        price = data.Price.values.reshape(-1, 1)

        categoryId = data.iloc[:, [0]]
        print(categoryId.head())
        regressionRandom = RandomForestRegressor(n_estimators=1000)
        regressionRandom.fit(categoryId, price)

        data = regressionRandom.predict([[1]])

        score = "Doğruluk Oranı: %" + \
            str(100*(r2_score(price, regressionRandom.predict(categoryId))))
        print(data)
        return data[0], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('age', required=True)
        parser.add_argument('city', required=True)
        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        new_data = pd.DataFrame({
            'name': [args['name']],
            'age': [args['age']],
            'city': [args['city']]
        })

        data = data.append(new_data, ignore_index=True)
        data.to_csv('users.csv', index=False)
        return {'data': new_data.to_dict('records')}, 201

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        data = data[data['name'] != args['name']]

        data.to_csv('users.csv', index=False)
        return {'message': 'Record deleted successfully.'}, 200

   
class Cities(Resource):
    def get(self):
        data = pd.read_csv('users.csv', usecols=[2])
        data = data.to_dict('records')

        return {'data': data}, 200


class Name(Resource):
    def get(self, name):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['name'] == name:
                return {'data': entry}, 200
        return {'message': 'No entry found with this name !'}, 200


# Add URL endpoints
api.add_resource(Users, '/users')
api.add_resource(Cities, '/cities')
api.add_resource(Name, '/<string:name>')


if __name__ == '__main__':
    #     app.run(host="0.0.0.0", port=5000)
    app.run()