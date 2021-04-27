from flask import Flask, json, jsonify, request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager 
from models import db, User, Vehicles, Characters, Planets


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
Migrate(app, db) #init, migrate, upgrade
manager = Manager(app)
manager.add_command('db', MigrateCommand)

####### USERS ######
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.to_dict(), users))
    return jsonify(users), 200

@app.route('/users', methods=['POST'])
def add_new_user():
    request_body = request.data
    decoded_object = json.loads(request_body)
    user = User()
    user.username = decoded_object ['username']
    user.email = decoded_object ['email']
    user.password = decoded_object ['password']
    user.save()
    return jsonify(user.to_dict()), 201


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if not user: 
        return jsonify({"msg": "user not found"}), 404
    user.delete()
    return jsonify({"success": "user deleted"}), 200

####### VEHICLES ######
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicles.query.all()
    vehicles = list(map(lambda vehicle: vehicle.to_dict(), vehicles))
    return jsonify(vehicles), 200

@app.route('/vehicles', methods=['POST'])
def add_new_vehicle():
    request_body = request.data
    decoded_object = json.loads(request_body)
    vehicle = Vehicles()
    vehicle.name = decoded_object['name']
    vehicle.model = decoded_object['model']
    vehicle.vehicle_class = decoded_object['vehicle_class']
    vehicle.crew = decoded_object['vehicle_crew']
    vehicle.manufacturer = decoded_object['manufacturer']
    vehicle.cargo_capacity = decoded_object['cargo_capacity']
    vehicle.cost_in_credits = decoded_object['cost_in_credits']
    vehicle.consumables = decoded_object['consumables']
    vehicle.save()
    return jsonify(vehicle.to_dict()), 201


@app.route('/vehicles/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    vehicle = Vehicles.query.get(id)

    if not vehicle: 
        return jsonify({"msg": "vehicle not found"}), 404
    vehicle.delete()
    return jsonify({"success": "vehicle deleted"}), 200


####### CHARACTERS ######

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    characters = list(map(lambda character: character.to_dict(), characters))
    return jsonify(characters), 200

@app.route('/characters', methods=['POST'])
def add_new_character():
    request_body = request.data
    decoded_object = json.loads(request_body)
    character = Characters()
    character.name = decoded_object['name']
    character.gender = decoded_object['gender']
    character.hair_color = decoded_object['hair_color']
    character.eye_color = decoded_object['eye_color']
    character.height = decoded_object['height']
    character.skin_color = decoded_object['skin_color']
    character.birth_year = decoded_object['birth_year']  
    character.save()
    return jsonify(character.to_dict()), 201


@app.route('/characters/<int:id>', methods=['DELETE'])
def delete_character(id):
    character = Characters.query.get(id)

    if not character: 
        return jsonify({"msg": "character not found"}), 404
    character.delete()
    return jsonify({"success": "character deleted"}), 200


####### PLANETS ######

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets = list(map(lambda planet: planet.to_dict(), planets))
    return jsonify(planets), 200

@app.route('/planets', methods=['POST'])
def add_new_planet():
    request_body = request.data
    decoded_object = json.loads(request_body)
    planet = Planets()
    planet.name = decoded_object['name']
    planet.population = decoded_object['population']
    planet.terrain = decoded_object['terrain']
    planet.climate = decoded_object['climate']
    planet.rotation_period = decoded_object['rotation_period']
    planet.orbital_period = decoded_object['orbital_period']
    planet.gravity = decoded_object['gravity']
    planet.save()
    return jsonify(planet.to_dict()), 201


@app.route('/planets/<int:id>', methods=['DELETE'])
def delete_planets(id):
    planet = Planets.query.get(id)

    if not planet: 
        return jsonify({"msg": "planet not found"}), 404
    planet.delete()
    return jsonify({"success": "planet deleted"}), 200

 


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=3245, debug=True)
    manager.run()