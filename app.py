import os

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
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
            "Success": "True"
        })
    
    # GET All endpoints - All Films & All Actors

    @app.route('/films')
    def get_films():
      """Return the serialised set of Films from the DB"""
      films = Film.query.all()
      fetched_films = []
      for film in films:
        fetched_films.append(film.format())
      return jsonify({
        "Success": "True",
        "films": fetched_films
      })

    @app.route('/actors')
    def get_actors():
      """Return the serialised set of Actors from the DB"""
      actors = Actor.query.all()
      fetched_actors = []
      for actor in actors:
        fetched_actors.append(actor.format())
      return jsonify({
        "Success": "True",
        "actors": fetched_actors
      })

    # POST endpoints - Add a Film & Add an Actor

    @app.route('/film', methods=['POST'])
    def post_film():
        """ Endpoint to add a film. """
        request_data = request.get_json()
        name = request_data['name']
        date_of_release = request_data['date_of_release']
        film = Film(name, date_of_release)
        film.insert()
        return jsonify({
            "Success": "True",
            "film": film.format()
        })

    @app.route('/actor', methods=['POST'])
    def post_actor():
        """ Endpoint to add an actor. """
        request_data = request.get_json()
        name = request_data['name']
        gender = request_data['gender']
        age = request_data['age']
        actor = Actor(name, gender, age)
        actor.insert()
        return jsonify({
            "Success": "True",
            "actor": actor.format()
        })

    """ Error Handlers. """

    @app.errorhandler(500)
    def handle_ISE(error):
        """ Handler for Internal Server Error 500. """
        return jsonify({"Success": "False",
        "Error": 500,
        "Message": error.error['description']}), 500

    # @app.errorhandler(507)
    # def handle_storage(error):
    #    """ Handler for Insufficient Storage Space 507. """
    #    return jsonify({"Success": "False",
    #    "Error": 507,
    #    "Message": error.error['description']}), 507

    @app.errorhandler(AuthError)
    def handle_auth(error):
        """ Handler for an Auth Error. """
        return jsonify({"Success": "False",
        "Error": error.status_code,
        "Message": error.error['description']}), error.status_code

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # Based on docs: https://flask.palletsprojects.com/en/2.2.x/errorhandling/
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    """ end of create_app() """

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
