# models.py
from project.app import db


class Client(db.Model):  # type: ignore
    __tablename__ = "client"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parking(db.Model):  # type: ignore
    __tablename__ = "parking"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean, default=True)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ClientParking(db.Model):  # type: ignore
    __tablename__ = "client_parking"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    parking_id = db.Column(db.Integer, db.ForeignKey("parking.id"))
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    __table_args__ = (db.UniqueConstraint("client_id", "parking_id"),)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
