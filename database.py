# database.py
from peewee import MySQLDatabase

db = MySQLDatabase('hotel_booking', user='root', password='root',
                   port=3306, host='localhost')