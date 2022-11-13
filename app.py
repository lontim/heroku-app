import os

from flask import Flask, jsonify
from flask_cors import CORS

from auth import AuthError, RequiresAuth
from common_handles import db, migrate
from models import Actor, Film, setup_db


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!!"
        return greeting

    @app.route('/status')
    def be_cool():
        status = ""
        status = 'The value of __name__ is {}'.format(__name__) + "\n"
        status += "<br>\n"
        return status + "Connection string: " + os.environ['DATABASE_URL']


    @app.route('/films')
    def get_films():
      films = Film.query.all()
      fetched_films = []
      for film in films:
        fetched_films.append(film.format())
      return jsonify({
        "success": "True",
        "films": fetched_films
      })

    return app

app = create_app()

if __name__ == '__main__':
    app.run()

@app.shell_context_processor
def make_shell_context():
    return {
            'db': db,
            'app': app,
            'Actor': Actor,
            'Film': Film
            }
