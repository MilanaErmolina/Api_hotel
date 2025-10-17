# models.py
from peewee import Model, AutoField, CharField, IntegerField, FloatField, ForeignKeyField, DateField
from database import db

class BaseModel(Model):
    class Meta:
        database = db

class Hotel(BaseModel):
    id = AutoField()
    name = CharField()
    address = CharField()
    city = CharField()
    rating = FloatField()

class RoomType(BaseModel):
    id = AutoField()
    name = CharField()
    description = CharField()
    capacity = IntegerField()

class Room(BaseModel):
    id = AutoField()
    hotel = ForeignKeyField(Hotel, backref='rooms')
    room_type = ForeignKeyField(RoomType, backref='rooms')
    room_number = CharField()
    price_per_night = FloatField()
    is_available = IntegerField(default=1)

class Guest(BaseModel):
    id = AutoField()
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    phone = CharField()

class Booking(BaseModel):
    id = AutoField()
    guest = ForeignKeyField(Guest, backref='bookings')
    room = ForeignKeyField(Room, backref='bookings')
    check_in_date = DateField()
    check_out_date = DateField()
    total_price = FloatField()
    status = CharField(default='confirmed')