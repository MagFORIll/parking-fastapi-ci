# factories.py
import factory
from faker import Faker

from project.models import Client, Parking, db

fake = Faker()


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    name = factory.LazyAttribute(lambda _: fake.first_name())
    surname = factory.LazyAttribute(lambda _: fake.last_name())
    credit_card = factory.LazyAttribute(
        lambda _: fake.credit_card_number(
            card_type=None
        ) if fake.boolean() else None
    )
    car_number = factory.LazyAttribute(lambda _: fake.license_plate())


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    address = factory.LazyAttribute(lambda _: fake.address())
    opened = factory.LazyAttribute(lambda _: fake.boolean())
    count_places = factory.LazyAttribute(
        lambda _: fake.random_int(min=5, max=50)
    )
    count_available_places = factory.LazyAttribute(lambda o: o.count_places)
