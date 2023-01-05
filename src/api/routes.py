"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Planets
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

# CREATE USER
@api.route("/signup", methods=["POST"])
def signup():

    if request.method == "POST":
        email = request.json.get("email", None)
        password = request.json.get("password", None)

    if not email:
        return "Email is required", 401
    if not password:
        return "Password is required", 401

    email_query = User.query.filter_by(email=email).first()
    if email_query:
        return "This email already exists", 401

    user = User()
    user.email = email
    user.password = password
    user.is_active = True
    print(user)
    db.session.add(user)
    db.session.commit()

    response = {
    "msg": "User added successfully",
    "email": email
    }
    return jsonify(response), 200

# GET USERS
@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    users = list(map(lambda index: index.serialize(), users))
    response_body = {
        "users": users
    }
    return jsonify(response_body), 200

# DELETE USER
@api. route("/users/<int:user>/", methods= ["DELETE"]) 
def delete_user(user):
    users = User.query.filter (User.id == user). first ()
    if users is None:
        return jsonify({
            "message": "User does not exist"
            }), 404
    db.session.delete(users)
    db.session.commit ()
    return jsonify({
        "message": "User was deleted successfully"
    }), 201

# GET 1 SPECIFIC USER
@api. route ("/users/<int:user>/", methods= ["GET"]) 
def get_specific_user (user):
    user = User.query.filter (User.id == user).first ()
    if user is None:
        return jsonify({
            "message": "No user found"
        }), 404
    return jsonify({
        "user": user.serialize ()
    }), 200



### PLANETS ###

# CREATE PLANET
@api.route("/planet", methods=["POST"])
def create_planet():

    if request.method == "POST":
        id = request.json.get("id", None)
        name = request.json.get("name", None)
        diameter = request.json.get("diameter", None)
        population = request.json.get("population", None)

    if not name:
        return "Name is required", 401
    if not diameter:
        return "Diameter is required", 401
    if not population:
        return "Population is required", 401

    planet_name_query = Planets.query.filter_by(name=name).first()
    if planet_name_query:
        return "This planet already exists", 401

    planet = Planets()
    planet.name = name
    planet.diameter = diameter
    planet.population = population
    print(planet) 
    db.session.add(planet)
    db.session.commit()

    response = {
    "msg": "Planet added successfully",
    "name":name,
    "diameter":diameter,
    "population":population
    }
    return jsonify(response), 200


# GET ALL PLANETS
@api.route("/planets", methods=["GET"])
def get_planets():
    planets = Planets.query.all()
    planets = list(map(lambda index: index.serialize(), planets))
    response_body = {
        "planets": planets
    }
    return jsonify(response_body), 200