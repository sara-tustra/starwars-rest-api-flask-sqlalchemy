from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100), nullable=False, unique=True)
    password=db.Column(db.String(100), nullable=False)
    favorites = db.relationship(
        'Favorite', cascade='all, delete', backref='user', uselist=False
    )
  
    def save(self):
        db.session.add(self) # INSERT
        db.session.commit() # SAVE THE INSERT
    
    def update(self):
        db.session.commit() # SAVE THE UPDATE
    
    def delete(self):
        db.session.delete(self) # DELETE
        db.session.commit() # Guarda el DELETE
    
    def check_password(self, password):
        return safe_str_cmp()

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username          
        }
    
    def serialize_with_favorites(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "favorites": {
                "vehicles": self.favorites.vehicles.serialize(),
                "characters": self.favorites.characters.serialize(),
                "planets": self.favorites.planets.serialize()
            }
        }
   
   
class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250))
    vehicle_class = db.Column(db.String(250))
    crew = db.Column(db.Integer)
    manufacturer = db.Column(db.String(250))
    cargo_capacity = db.Column(db.Integer)
    cost_in_credits = db.Column(db.Integer)
    consumables = db.Column(db.Integer)
    favorites = db.relationship('Favorite', secondary='vehicles_favorites', backref='vehicle')

    def save(self):
        db.session.add(self) # INSERT
        db.session.commit() # SAVE THE INSERT
    
    def update(self):
        db.session.commit() # SAVE THE UPDATE
    
    def delete(self):
        db.session.delete(self) # DELETE
        db.session.commit() # Guarda el DELETE

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "crew": self.crew,
            "manufacturer": self.manufacturer,
            "cargo_capacity": self.cargo_capacity,
            "cost_in_credits": self.cost_in_credits,
            "consumables": self.consumables
        }
    
class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250))
    hair_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    height = db.Column(db.String(250))
    skin_color = db.Column(db.String(250))
    birth_year = db.Column(db.String(250))
    favorites = db.relationship('Favorite', secondary='characters_favorites', backref='character')

    def save(self):
        db.session.add(self) # INSERT
        db.session.commit() # SAVE THE INSERT
    
    def update(self):
        db.session.commit() # SAVE THE UPDATE
    
    def delete(self):
        db.session.delete(self) # DELETE
        db.session.commit() # Guarda el DELETE

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "height": self.height,
            "skin_color": self.skin_color,
            "birth_year": self.birth_year
        }
    
class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(300), nullable=False)
    population = db.Column(db.String(300))
    terrain = db.Column(db.String(300))
    climate = db.Column(db.String(300))
    rotation_period = db.Column(db.String(300))    
    orbital_period = db.Column(db.String(300))
    gravity = db.Column(db.String(300))
    favorites = db.relationship('Favorite', secondary='planets_favorites', backref='planet') ## preguntar al profe

    def save(self):
        db.session.add(self) # INSERT
        db.session.commit() # SAVE THE INSERT
    
    def update(self):
        db.session.commit() # SAVE THE UPDATE
    
    def delete(self):
        db.session.delete(self) # DELETE
        db.session.commit() # Guarda el DELETE

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity
        }


## tabla de favoritos mas tablas pivote para cada categoria

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    #many to many
    vehicles = db.relationship('Vehicle', secondary='vehicles_favorites')
    characters = db.relationship('Character', secondary='characters_favorites')
    planets = db.relationship('Planet', secondary='planets_favorites')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
           "id": self.id,
           "user": {
               "id": self.user.id,
               "username": self.user.username
            },
           "vehicles": self.get_vehicles(),
           "characters": self.get_characters(),
           "planets": self.get_planets()
        }
    def get_vehicles(self):
        return list(map(lambda vehicle: vehicle.serialize(), self.vehicles))

    def get_characters(self):
        return list(map(lambda character: character.serialize(), self.characters))

    def get_planets(self):
        return list(map(lambda planet: planet.serialize(), self.planets))

class VehicleFavorite(db.Model):
    __tablename__='vehicles_favorites'
    vehicles_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), primary_key=True)
    favorites_id = db.Column(db.Integer, db.ForeignKey('favorites.id'), primary_key=True)


class CharacterFavorite(db.Model):
    __tablename__='characters_favorites'
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'), primary_key=True)
    favorites_id = db.Column(db.Integer, db.ForeignKey('favorites.id'), primary_key=True)

class PlanetFavorite(db.Model):
    __tablename__='planets_favorites'
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'), primary_key=True)
    favorites_id = db.Column(db.Integer, db.ForeignKey('favorites.id'), primary_key=True)
