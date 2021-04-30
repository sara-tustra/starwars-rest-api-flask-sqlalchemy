from flask import Flask, json, jsonify, request, render_template
from flask_script import Manager 
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS

from flask_jwt_extended import JWTManager, get_jwt_identity, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Vehicle, Character, Planet, Favorite, VehicleFavorite, CharacterFavorite, PlanetFavorite


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "33b9b3de94a42d19f47df7021954eaa8"

db.init_app(app)
Migrate(app, db) #init, migrate, upgrade
CORS(app)
jwt=JWTManager(app)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username= request.json.get('username')
    password= request.json.get('password')

    if not username:
        return jsonify({"fail": "username required"}), 400
    
    if not password:
        return jsonify({"fail": "password required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user: 
        return jsonify({"fail": "username or password is incorrect"}), 401

    if not check_password_hash(user.password, password): 
        return jsonify({"fail": "username or password is incorrect"}), 401

    access_token = create_access_token(identity=username)

    return jsonify({"token": access_token}), 200

@app.route('/register', methods=['POST'])
def register():
    username= request.json.get('username')
    password= request.json.get('password')

    if not username:
        return jsonify({"fail": "username required"}), 400
    
    if not password:
        return jsonify({"fail": "password required"}), 400

    user = User.query.filter_by(username=username).first()
    if user: return jsonify({"fail": "username already exists"})

    user = User()
    user.username = username
    user.password = generate_password_hash(password)
    user.save()

    return jsonify({
        "success": "user created!",
        "user" :user.serialize()
    }), 201   


@app.route('/profile')
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({
        "success": "private route",
        "user": current_user
    }), 200    

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
        username = request.json.get('username')
        password= request.json.get('password')

        user = User()
        user.username = username
        user.password = password

        favorite = Favorite()
        user.favorites = favorite
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
                "vehicle": vehicle.serialize()
            }), 200
        else:
            vehicles = Vehicle.query.all()
            vehicles = list(map(lambda vehicle: vehicle.serialize(), vehicles))
            return jsonify({
                "total": len(vehicles),
                "results": vehicles
            }), 200

    if request.method == 'POST':
        name = request.json.get('name')
        model = request.json.get('model')
        vehicle_class = request.json.get('vehicle_class')
        crew = request.json.get('crew')
        manufacturer = request.json.get('manufacturer')
        cargo_capacity = request.json.get('cargo_capacity')
        cost_in_credits = request.json.get('cost_in_credits')
        consumables = request.json.get('consumables')
       
        

        vehicle = Vehicle()
        vehicle.name = name
        vehicle.model = model
        vehicle.vehicle_class = vehicle_class
        vehicle.crew = crew
        vehicle.manufacturer = manufacturer
        vehicle.cargo_capacity = cargo_capacity
        vehicle.cost_in_credits = cost_in_credits
        vehicle.consumables = consumables
        
        vehicle.save()
        return jsonify({
            "success": "vehicle created!",
            "vehicle": vehicle.serialize()
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
                "character": character.serialize()
            }), 200
        else:
            characters = Character.query.all()
            characters = list(map(lambda character: character.serialize(), characters))
            return jsonify({
                "total": len(characters),
                "results": characters
            }), 200
    if request.method == 'POST':
        name = request.json.get('name')
        gender = request.json.get('gender')
        hair_color = request.json.get('hair_color')
        eye_color = request.json.get('eye_color')
        height = request.json.get('height')
        skin_color = request.json.get('skin_color')
        birth_year = request.json.get('birth_year')


        character = Character()
        character.name = name
        character.gender = gender
        character.hair_color = hair_color
        character.eye_color = eye_color
        character.height = height
        character.skin_color = skin_color
        character.birth_year = birth_year
        character.save()

        return jsonify({
            "success": "character created!",
            "character": character.serialize()
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
                "planet": planet.serialize()
            }), 200
        else:
            planets = Planet.query.all()
            planets = list(map(lambda planet: planet.serialize(), planets))
            return jsonify({
                "total": len(planets),
                "results": planets
            }), 200

    if request.method == 'POST':
        name = request.json.get('name')
        population = request.json.get('population')
        terrain = request.json.get('terrain')
        climate = request.json.get('climate')
        rotation_period = request.json.get('rotation_period')
        orbital_period = request.json.get('orbital_period')
        gravity = request.json.get('gravity')



        planet = Planet()
        planet.name = name
        planet.population = population
        planet.terrain = terrain
        planet.climate = climate
        planet.rotation_period = rotation_period
        planet.orbital_period = orbital_period
        planet.gravity = gravity
        planet.save()
        return jsonify({
            "success": "planet created!",
            "planet": planet.serialize()
        }), 201

    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        planet = Planet.query.get(id)
        if not planet: 
            return jsonify({"fail": "planet not found"}), 404
        planet.delete()
        return jsonify({"success": "planet deleted"}), 200


###################
###################
###################
        

@app.route('/users/<int:user_id>/favorites', methods=['GET', 'POST', 'DELETE'])
def favorites(user_id=None):
    if request.method == 'GET':
        if user_id is not None:
            users = User.query.all()
            if user_id > len(users):
                return jsonify({ "fail": "user does not exist" }), 404
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
                map(lambda user_favs: user.serialize(), users)
            )

    if request.method == 'POST':
      
        id_vehicle = request.json.get('id_vehicle',)
        id_character = request.json.get('id_character')
        id_planet = request.json.get('id_planet')

        user = User.query.filter_by(id = user_id).first()
        if not user:
            return jsonify({"fail": "the indicated user does not exist"})
            
        vehicle = Vehicle.query.filter_by(id= id_vehicle).first()
        character = Character.query.filter_by(id=id_character).first()
        planet = Planet.query.filter_by(id=id_planet).first()

        favorite = Favorite()
        user.favorites = favorite
        favorite.vehicles.append(vehicle)
        favorite.characters.append(character)
        favorite.planets.append(planet)

        favorite.save()
        user.update()

        return jsonify({
            "success": "favorites added",
            "favorites": favorite.serialize()
        })


if __name__ == '__main__':
    manager.run()