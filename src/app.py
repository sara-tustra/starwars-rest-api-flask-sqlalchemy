from flask import Flask, json, jsonify, request, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager 
from flask_cors import CORS
from models import db, User, Vehicle, Character, Planet, Favorite, VehicleFavorite, CharacterFavorite, PlanetFavorite


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
Migrate(app, db) #init, migrate, upgrade
CORS(app)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/users', methods=['GET', 'POST'])
@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def users(id=None):
    if request.method == 'GET':
        if id is not None:
            user = User.query.get(id)    
            if not user:
                return jsonify({"fail": "User not found"}), 404
            return jsonify({
                "success": "User found",
                "user": user.serialize()
            }), 200
        else:
            users = User.query.all()
            users = list(map(lambda user: user.serialize(), users))
            return jsonify({
                "total": len(users),
                "results": users
            }), 200

    if request.method == 'POST':
        request_body = request.data
        decoded_object = json.loads(request_body)
        user = User()
        user.username = decoded_object ['username']
        user.email = decoded_object ['email']
        user.password = decoded_object ['password']
        user.save()
        return jsonify({
            "success": "user created!",
            "user": user.serialize()
        }), 201

    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        user = User.query.get(id)
        if not user: 
            return jsonify({"fail": "user not found"}), 404
        user.delete()
        return jsonify({"success": "user deleted"}), 200


####### VEHICLES ######
@app.route('/vehicles', methods=['GET', 'POST'])
@app.route('/vehicles/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def vehicles(id=None):
    if request.method == 'GET':
        if id is not None:
            vehicle = Vehicle.query.get(id)    
            if not vehicle:
                return jsonify({"fail": "Vehicle not found"}), 404
            return jsonify({
                "success": "Vehicle found",
                "vehicle": vehicle.serialize_vehicle_with_users()
            }), 200
        else:
            vehicles = Vehicle.query.all()
            vehicles = list(map(lambda vehicle: vehicle.serialize_vehicle_with_users(), vehicles))
            return jsonify({
                "total": len(vehicles),
                "results": vehicles
            }), 200

    if request.method == 'POST':
        request_body = request.data
        decoded_object = json.loads(request_body)
        vehicle = Vehicle()
        vehicle.name = decoded_object ['name']
        vehicle.model = decoded_object ['model']
        vehicle.vehicle_class = decoded_object ['vehicle_class']
        vehicle.crew = decoded_object['crew']
        vehicle.manufacturer = decoded_object['manufacturer']
        vehicle.cargo_capacity = decoded_object['cargo_capacity']
        vehicle.cost_in_credits = decoded_object['cost_in_credits']
        vehicle.consumables = decoded_object['consumables']
        vehicle.save()
        return jsonify({
            "success": "vehicle created!",
            "vehicle": vehicle.serialize_vehicle_with_users()
        }), 201

    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        vehicle = Vehicle.query.get(id)
        if not vehicle: 
            return jsonify({"fail": "vehicle not found"}), 404
        vehicle.delete()
        return jsonify({"success": "vehicle deleted"}), 200



####### CHARACTERS ######

@app.route('/characters', methods=['GET', 'POST'])
@app.route('/characters/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def characters(id=None):
    if request.method == 'GET':
        if id is not None:
            character = Character.query.get(id)    
            if not character:
                return jsonify({"fail": "Character not found"}), 404
            return jsonify({
                "success": "Character found",
                "character": character.serialize_character_with_users()
            }), 200
        else:
            characters = Character.query.all()
            characters = list(map(lambda character: character.serialize_character_with_users(), characters))
            return jsonify({
                "total": len(characters),
                "results": characters
            }), 200
    if request.method == 'POST':
        request_body = request.data
        decoded_object = json.loads(request_body)
        character = Character()
        character.name = decoded_object['name']
        character.gender = decoded_object['gender']
        character.hair_color = decoded_object['hair_color']
        character.eye_color = decoded_object['eye_color']
        character.height = decoded_object['height']
        character.skin_color = decoded_object['skin_color']
        character.birth_year = decoded_object['birth_year']
        character.save()

        return jsonify({
            "success": "character created!",
            "character": character.serialize_character_with_users()
        }), 201

    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        character = Character.query.get(id)
        if not character: 
            return jsonify({"fail": "character not found"}), 404
        character.delete()
        return jsonify({"success": "character deleted"}), 200


####### PLANETS ######

@app.route('/planets', methods=['GET', 'POST'])
@app.route('/planets/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def planets(id=None):
    if request.method == 'GET':
        if id is not None:
            planet = Planet.query.get(id)    
            if not planet:
                return jsonify({"fail": "Planet not found"}), 404
            return jsonify({
                "success": "Planet found",
                "planet": planet.serialize_planet_with_users()
            }), 200
        else:
            planets = Planet.query.all()
            planets = list(map(lambda planet: planet.serialize_planet_with_users(), planets))
            return jsonify({
                "total": len(planets),
                "results": planets
            }), 200

    if request.method == 'POST':
        request_body = request.data
        decoded_object = json.loads(request_body)
        planet = Planet()
        planet.name = decoded_object['name']
        planet.population = decoded_object['population']
        planet.terrain = decoded_object['terrain']
        planet.climate = decoded_object['climate']
        planet.rotation_period = decoded_object['rotation_period']
        planet.orbital_period = decoded_object['orbital_period']
        planet.gravity = decoded_object['gravity']
        planet.save()
        return jsonify({
            "success": "planet created!",
            "planet": planet.serialize_planet_with_users()
        }), 201

    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        planet = Planet.query.get(id)
        if not planet: 
            return jsonify({"fail": "planet not found"}), 404
        planet.delete()
        return jsonify({"success": "planet deleted"}), 200



        

@app.route('/users/<int:user_id>/favorites', methods=['GET', 'POST', 'DELETE'])
def favorites(user_id=None):
    if request.method == 'GET':
        if user_id is not None:
            user = User.query.get(user_id)
            if not user.favorites:
                return jsonify({ "fail": "user does not have favorites" }), 404
            
            return jsonify({
                "success": "Favorites found",
                "favorites": user.favorites.serialize()
                }),200
        else:
            users= User.query.all()
            users = list(
                map(lambda user_favs: user.serialize_with_favorites(), users)
            )

    if request.method == 'POST':
        if user_id is None:
            return jsonify({"fail": "please indicate a valid user"})
        
        vehicles = request.json.get('vehicles')
        characters = request.json.get('characters')
        planets = request.json.get('planets')

        user = User() #Preguntar al profe
        favorite = Favorite()
        for vehicle_id in vehicles:
            vehicle = Vehicle.query.get(vehicle_id)
            favorite.vehicles.append(vehicle)

        for character_id in characters:
            character = Character.query.get(character_id)
            favorite.characters.append(character)

        for planet_id in planets:
            planet = Planet.query.get(planet_id)
            favorite.planets.append(planet)


        user.favorites = favorites
        favorite.save()
        user.save()

        
        return jsonify({
            "success": "favorites added",
            "user": user.serialize_with_favorites()
        })

    



            

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=3245, debug=True)
    manager.run()