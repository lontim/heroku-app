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

    AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
    API_AUDIENCE = os.environ['API_AUDIENCE']
    AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
    AUTH0_CALLBACK_URL = os.environ['AUTH0_CALLBACK_URL']

    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE')
      return response

    @app.route('/')
    def get_greeting():
        """ Friendly welcome message advising that this is an API service. """
        greeting = "Welcome to the Casting Database - API (Application Programming Interface) layer." 
        return greeting

    @app.route('/status')
    def status():
        return jsonify({
            "Success": "True"
        })
    
    # GET All endpoints - All Films & All Actors

    @app.route('/films')
    @RequiresAuth('get:film')
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
    @RequiresAuth('get:actor')
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
    @RequiresAuth('post:film')
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
    @RequiresAuth('post:actor')
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
        "Message": "Internal Server Error."}), 500

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
