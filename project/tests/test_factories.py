# tests/test_factories.py
from project.factories import ClientFactory, ParkingFactory
from project.models import Client, Parking


def test_create_client_factory(db_session):
    client = ClientFactory()
    db_session.add(client)
    db_session.commit()
    db_client = db_session.query(Client).first()
    assert db_client.id is not None


def test_create_parking_factory(db_session):
    parking = ParkingFactory()
    db_session.add(parking)
    db_session.commit()
    db_parking = db_session.query(Parking).first()
    assert db_parking.count_places == db_parking.count_available_places
