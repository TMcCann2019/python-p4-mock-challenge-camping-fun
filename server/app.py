#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/campers')
def get_campers():
    campers = Camper.query.all()
    camper_response = []
    for camper in campers:
        camp_response = {
            'id': camper.id,
            'name': camper.name,
            'age': camper.age
        }
        camp_response.append(camper_response)
    return make_response(jsonify(camper_response), 200)

@app.route('/campers')  
def post(self):
    new_camper = Camper(
        name = request.get_json()['name'],
        age = request.get_json()['age']
    )
    db.session.add(new_camper)
    db.session.commit()

    response_dict = new_camper.to_dict()
    return make_response(response_dict, 201)

@app.route('/camper/<int:id>')
def get(self, camper_id):
    camper = Camper.query.filter_by(id=camper_id).first()
    if not camper:
        return {'error': 'Camper not found'}, 404
    return camper.to_dict(), 200

@app.route('/camper/<int:id>')
def patch(self, camper_id):
    camper = Camper.query.filter_by(id=camper_id).first()
    if not camper:
        return {'error': 'Camper not found'}, 404
    camper.name = request.get_json()['name']
    camper.age = request.get_json()['age']
    db.session.commit()
    return camper.to_dict(), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
