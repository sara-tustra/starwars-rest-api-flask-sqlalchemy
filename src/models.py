from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(250), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String (150), nullable=False)
    
    def save(self):
        db.session.add(self) # INSERT
        db.session.commit() # SAVE THE INSERT
    
    def update(self):
        db.session.commit() # SAVE THE UPDATE
    
    def delete(self):
        db.session.delete(self) # DELETE
        db.session.commit() # Guarda el DELETE

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,           
        }


class Vehicles(db.Model):
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

    def save(self):
        db.session.add(self) # INSERT
        db.session.commit() # SAVE THE INSERT
    
    def update(self):
        db.session.commit() # SAVE THE UPDATE
    
    def delete(self):
        db.session.delete(self) # DELETE
        db.session.commit() # Guarda el DELETE

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle class": self.vehicle_class,
            "crew": self.crew,
            "manufacturer": self.manufacturer,
            "cargo_capacity": self.cargo_capacity,
            "cost_in_credits": self.cost_in_credits,
            "consumables": self.consumables
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250))
    hair_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    height = db.Column(db.String(250))
    skin_color = db.Column(db.String(250))
    birth_year = db.Column(db.String(250))

    def save(self):
        db.session.add(self) # INSERT
        db.session.commit() # SAVE THE INSERT
    
    def update(self):
        db.session.commit() # SAVE THE UPDATE
    
    def delete(self):
        db.session.delete(self) # DELETE
        db.session.commit() # Guarda el DELETE

    def to_dict(self):
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

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(300), nullable=False)
    population = db.Column(db.String(300))
    terrain = db.Column(db.String(300))
    climate = db.Column(db.String(300))
    rotation_period = db.Column(db.String(300))    
    orbital_period = db.Column(db.String(300))
    gravity = db.Column(db.String(300))

    def save(self):
        db.session.add(self) # INSERT
        db.session.commit() # SAVE THE INSERT
    
    def update(self):
        db.session.commit() # SAVE THE UPDATE
    
    def delete(self):
        db.session.delete(self) # DELETE
        db.session.commit() # Guarda el DELETE

    def to_dict(self):
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