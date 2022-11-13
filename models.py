import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
from common_handles import db, migrate
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

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
    migrate.init_app(app,db)



class Actor(db.Model):  
  __tablename__ = 'actor'

  id = Column(db.Integer, primary_key=True)
  name = Column(db.String, nullable=False)
  gender = Column(db.String, nullable=False)
  age = Column(db.Integer, nullable=False)

  def __init__(self, name, gender="", age=0):
    self.name = name
    self.gender = gender
    self.age = age

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'gender': self.gender,
      'age': self.age}

class Film(db.Model):
  __tablename__ = 'film'
  id = Column(db.Integer, primary_key=True)
  name = Column(db.String, nullable=False)
  date_of_release = Column(db.String, nullable=False)

  def __init(self, name, date_of_release):
    self.name = name
    self.date_of_release = date_of_release
  
  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'date_of_release': self.date_of_release}