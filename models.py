import json, os
# from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Column, String, create_engine
from common_handles import db, migrate

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


"""Table that defines which actors are cast in a film"""
film_actors = db.Table( "film_actors",
#    db.Model.metadata,
    Column("actor_id", db.Integer, ForeignKey("actor.id"), primary_key=True),
    Column("film_id", db.Integer, ForeignKey("film.id"), primary_key=True),
)

# @dataclass
class Actor(db.Model):
  """Actor class for data in the "actor" table."""
  __tablename__ = 'actor'
  id = Column(db.Integer, primary_key=True)
  name = Column(db.String, nullable=False)
  gender = Column(db.String, nullable=False)
  age = Column(db.Integer, nullable=False)
  film = db.relationship("Film", secondary="film_actors",
#   backref=db.backref('films', lazy=True),
   back_populates="actor")


  def __init__(self, name, gender="", age=0):
    """Initialise an actor instance.
      
      Takes three parameters:
      * name: db.String - Name of the actor
      * gender: db.String - Male or Female - Gender of the actor
      * age: db.Integer - Age of the actor
    """
    self.name = name
    self.gender = gender
    self.age = age

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'gender': self.gender,
      'age': self.age}

  def __repr__(self):
    """Print a friendly representation of an Actor."""
    actor = "Actor (" + str(self.format()) + ")" + '\n'
    return actor
  
  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.commit()

  def update(self):
    db.session.commit()

class Film(db.Model):
  """Film class for data in the "film" table."""
  __tablename__ = 'film'
  id = Column(db.Integer, primary_key=True)
  name = Column(db.String, nullable=False)
  date_of_release = Column(db.String, nullable=False)
  actor = db.relationship("Actor", secondary="film_actors",
#   backref=db.backref('actors', lazy=True), 
   back_populates="film")

  def __init__(self, name, date_of_release=""):
    """Initialise a film instance.

      Takes two parameters:
      * name: db.String - Name of the film e.g. "Casablanca"
      * date_of_release: db.String - Date the film was released e.g. "26-Nov-1942"
    """
    self.name = name
    self.date_of_release = date_of_release
  
  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'date_of_release': self.date_of_release}

  def __repr__(self):
    """Print a friendly representation of a Film."""
    film = "Film (" + str(self.format()) + ")" + '\n'
    return film
