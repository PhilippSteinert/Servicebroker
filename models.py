import os
from sqlalchemy import Column, String, Integer, DateTime, Boolean, create_engine, Float
from flask_sqlalchemy import SQLAlchemy
import json

database_user = 'postgres'
database_password = 'Murakami20'
database_host = 'localhost:5432'
database_name = "servicebroker"
database_path = "postgres://{}:{}@{}/{}".format(database_user, database_password, database_host, database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # PST: Temporarily commented out for database migration
    # db.create_all()


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename
    variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    print('Dropped and created all tables!')


'''
ServiceRequest
    database model for service requests
'''
class ServiceRequest(db.Model):  
  __tablename__ = 'servicerequests'

  id = Column(Integer, primary_key=True)
  service_type = Column(String, nullable=False)
  origin_airport = Column(String, nullable=False)
  destination_airport = Column(String, nullable=False)
  payload = Column(String, nullable=False)
  payload_weight = Column(Integer, nullable=False)
  status = Column(String)
  priority = Column(Boolean)
  user_id = Column(Integer, nullable=False)
  collection_datetime = Column(DateTime, nullable=False)
  delivery_datetime = Column(DateTime, nullable=False)
  latest_delivery_datetime = Column(DateTime, nullable=False)
  
  def __init__(self, service_type, origin_airport, destination_airport, payload, payload_weight, status, priority, 
  user_id, collection_datetime, delivery_datetime, latest_delivery_datetime):
    self.service_type = service_type
    self.origin_airport = origin_airport
    self.destination_airport = destination_airport
    self.payload = payload
    self.payload_weight = payload_weight
    self.status = status
    self.priority = priority
    self.user_id = user_id
    self.collection_datetime = collection_datetime
    self.delivery_datetime = delivery_datetime
    self.latest_delivery_datetime = latest_delivery_datetime

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'service_type': self.service_type,
      'origin_airport': self.origin_airport,
      'destination_airport': self.destination_airport,
      'payload': self.payload,
      'payload_weight': self.payload_weight,
      'status': self.status,
      'priority': self.priority,
      'user_id': self.user_id,
      'collection_datetime': self.collection_datetime.strftime("%Y-%m-%d, %H:%M"),
      'delivery_datetime': self.delivery_datetime.strftime("%Y-%m-%d, %H:%M"),
      'latest_delivery_datetime': self.latest_delivery_datetime.strftime("%Y-%m-%d, %H:%M"),
    }

'''
Hospital
    database model for hospitals
'''
class Hospital(db.Model):
  __tablename__ = 'hospitals'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  longitude = Column(Float, nullable=False)
  latitude = Column(Float, nullable=False)
  

  def __init__(self, name, longitude, latitude):
    self.name = name
    self.longitude = longitude
    self.latitude = latitude
  
  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'longitude': self.longitude,
      'latitude': self.latitude,
    }