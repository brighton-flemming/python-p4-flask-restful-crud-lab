#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse

from models import db, Plant



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('image', type=str)
parser.add_argument('price', type=float)
parser.add_argument('is_in_stock', type=bool)


class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


api.add_resource(Plants, '/plants')


class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)
    
    def patch(self, id):
        data = parser.parse_args()


        plant = Plant.query.get(id)

        if not plant:
            return {"error":"Plant Not Found"}
    
        if 'name' in data:
            plant.name = data['name']
        elif 'image' in data:
            plant.image = data['image']
        elif 'price' in data:
            plant.price = data['price']
        elif 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']

        db.session.commit()

        return {"message":"Plant Updated Successfully.", "is_in_stock":plant.is_in_stock}

    def delete(self, id):
        plant = Plant.query.get(id)

        if plant:
          db.session.delete(plant)
          db.session.commit()
          return {"message":"Plant Deleted"}, 200
        else:
            return {"error": "Plant Not Found."}



api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
