# app.py
from datetime import datetime

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from project.models import Client, ClientParking, Parking

    @app.route("/clients", methods=["GET"])
    def get_clients():
        clients = Client.query.all()
        return jsonify([c.as_dict() for c in clients])

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def get_client(client_id):
        client = Client.query.get_or_404(client_id)
        return jsonify(client.as_dict())

    @app.route("/clients", methods=["POST"])
    def create_client():
        data = request.json
        client = Client(
            name=data["name"],
            surname=data["surname"],
            credit_card=data.get("credit_card"),
            car_number=data.get("car_number"),
        )
        db.session.add(client)
        db.session.commit()
        return jsonify(client.as_dict()), 201

    @app.route("/parkings", methods=["POST"])
    def create_parking():
        data = request.json
        parking = Parking(
            address=data["address"],
            opened=data.get("opened", True),
            count_places=data["count_places"],
            count_available_places=data["count_places"],
        )
        db.session.add(parking)
        db.session.commit()
        return jsonify(parking.as_dict()), 201

    @app.route("/client_parkings", methods=["POST"])
    def enter_parking():
        data = request.json
        client = Client.query.get_or_404(data["client_id"])
        parking = Parking.query.get_or_404(data["parking_id"])

        if not parking.opened:
            return jsonify({"error": "Парковка закрыта"}), 400
        if parking.count_available_places <= 0:
            return jsonify({"error": "Нет свободных мест"}), 400

        log = ClientParking(
            client_id=client.id, parking_id=parking.id, time_in=datetime.now()
        )
        parking.count_available_places -= 1
        db.session.add(log)
        db.session.commit()
        return jsonify(log.as_dict()), 201

    @app.route("/client_parkings", methods=["DELETE"])
    def exit_parking():
        data = request.json
        client = Client.query.get_or_404(data["client_id"])
        parking = Parking.query.get_or_404(data["parking_id"])

        log = ClientParking.query.filter_by(
            client_id=client.id, parking_id=parking.id, time_out=None
        ).first()
        if not log:
            return jsonify({"error": "Запись не найдена"}), 404

        if not client.credit_card:
            return jsonify({"error": "У клиента нет карты"}), 400

        log.time_out = datetime.now()
        parking.count_available_places += 1
        db.session.commit()
        return jsonify(log.as_dict()), 200

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
