import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from auth import AuthError, RequiresAuth
from common_handles import db, migrate
from models import film_actors, Actor, Film, setup_db


def create_app():
    """ Create the main App instance. """
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        greeting = "Welcome to the Casting Database - Application Programming Interface (API) layer." 
        return greeting

    @app.route('/status')
    def status():
        return jsonify({
            "working": "true"
        })
    
    # GET All endpoints - All Films & All Actors

    @app.route('/films')
    def get_films():
      """Return the set of Films from the DB"""
      films = Film.query.all()
      fetched_films = []
      for film in films:
        fetched_films.append(film.format())
      return jsonify({
        "success": "True",
        "films": fetched_films
      })

    @app.route('/actors')
    def get_actors():
      """Return the set of Actors from the DB"""
      actors = Actor.query.all()
      fetched_actors = []
      for actor in actors:
        fetched_actors.append(actor.format())
      return jsonify({
        "success": "True",
        "actors": fetched_actors
      })

    # POST endpoints - Add a Film & Add an Actor

    @app.route('/film', methods=['POST'])
    def post_film():
        request_data = request.get_json()
        name = request_data['name'],
        date_of_release = request_data['date_of_release']
        new_film = Film(name, date_of_release);
        return jsonify({
            "success": True,
            "film": new_film.format()
        })

    @app.route('/actor', methods=['POST'])
    def post_actor():
        request_data = request.get_json()
        name = request_data['name'],
        gender = request_data['gender'],
        age = request_data['age']
        new_actor = Actor(name, gender, age);
        return jsonify({
            "success": True,
            "actor": new_actor.format()
        })


    return app

app = create_app()

if __name__ == '__main__':
    app.run()

@app.shell_context_processor
def make_shell_context():
    print ("Welcome to Interactive Mode.")
    print ("============================")
    print ("The following structures are available: db, app, Actor, Film, and film_actors.")
    return {
            'db': db,
            'app': app,
            'Actor': Actor,
            'Film': Film,
            'film_actors': film_actors
            }
