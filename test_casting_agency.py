import os, unittest, json
from flask_sqlalchemy import SQLAlchemy
from common_handles import db, migrate


from app import create_app
from models import setup_db, Actor, Film, film_actors

CASTING_ASSISTANT_TOKEN = os.environ['CASTING_ASSISTANT_TOKEN'] # token used by Casting Assistant role
CASTING_DIRECTOR_TOKEN = os.environ['CASTING_DIRECTOR_TOKEN'] # token used by Casting Director role
EXEC_PRODUCER_TOKEN = os.environ['EXEC_PRODUCER_TOKEN'] # token used by Exec Producer role
ERROR_TOKEN = os.environ['ERROR_TOKEN'] # an invalid token used for testing the authentication & authorisation

def bearer_token(token):
    return {
        'Authorization: Bearer ' + token
    }

class AgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define the casting agency test variables, go ahead and initialize the app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)

        self.test_film_valid = {
            "name": "Udacity Documentary",
            "date_of_release": "13-Nov-2022"
        }

        self.test_film_invalid = {
            "name": "John Wick 5"
        }

        self.test_actor_valid = {
            "name": "Keanu Reeves",
            "gender": "Male",
            "age": "58"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after each test"""
        pass

    def test_add_film_fail(self):
        """ Attempt to add a film, without the relevant token being present - should generate a 401. """
        res = self.client().post("/film",  json=self.test_film_valid)
        self.assertEqual(res.status_code,401)

    def test_add_film_succeed(self):
        res = self.client().post("/film", headers=bearer_token(EXEC_PRODUCER_TOKEN), json=self.test_film_valid)
        self.assertEqual(res.status_code,200)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()