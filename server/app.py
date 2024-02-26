#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route("/")
def home():
    return ""

@app.route("/campers", methods=["GET", 'POST'])
def get_campers():
    if request.method == "GET":
        campers = Camper.query.all()
        campers_dict = [camper.to_dict(rules=("-signups",)) for camper in campers]
        response = make_response(campers_dict, 200)
    elif request.method == "POST":
        try:
            form_data = request.get_json()
            new_camper = Camper(
                name=form_data["name"],
                age=form_data["age"]
            )
            db.session.add(new_camper)
            db.session.commit()
            response = make_response(new_camper.to_dict(), 201)
        except ValueError:
            response = make_response({"errors": ["Validation errors"]}, 400)
    return response

@app.route("/campers/<int:id>", methods=["GET", 'PATCH'])
def get_camper_by_id(id):
    camper = Camper.query.filter_by(id=id).first()
    if camper:
        if request.method == "GET":
            camper_dict = camper.to_dict()
            response = make_response(camper_dict, 200)
        elif request.method == "PATCH":
            try:
                form_data = request.get_json()
                camper = Camper.query.filter_by(id=id).first()
                camper.name = form_data["name"]
                camper.age = form_data["age"]
                db.session.commit()
                response = make_response(camper.to_dict(), 202)
            except ValueError:
                response = make_response({"errors": ["validation errors"]}, 400)
        return response
    else:
        response = make_response({"error": "Camper not found"}, 404)
    return response

@app.route("/activities", methods=["GET"])
def get_activities():
    activities = Activity.query.all()
    activities_dict = [activity.to_dict(rules=("-signups",)) for activity in activities]
    response = make_response(activities_dict, 200)
    return response

@app.route("/activities/<int:id>", methods=["DELETE"])
def delete_activity(id):
    activity = Activity.query.filter(Activity.id == id).first()
    if activity:
        db.session.delete(activity)
        db.session.commit()
        response = make_response({}, 204)
    else:
        response = make_response({"error": "Activity not found"}, 404)
    return response

@app.route('/signups', methods=['POST'])
def signup():
    try:
        new_signup = Signup(
            time=request.get_json()["time"],
            camper_id=request.get_json()["camper_id"],
            activity_id=request.get_json()["activity_id"]
        )
        db.session.add(new_signup)
        db.session.commit()
        response = make_response(new_signup.to_dict(), 201)
    except ValueError:
        response = make_response({"errors": ["validation errors"]}, 400)
    return response

if __name__ == "__main__":
    app.run(port=5555, debug=True)
