import os, unittest, json
from flask_sqlalchemy import SQLAlchemy
from common_handles import db, migrate


from app import create_app
from models import setup_db, Question, Category

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

        self.question_to_add = {
            "question": "How many stars in our galaxy, the Milky Way?",
            "answer": "100 thousand million stars",
            "difficulty": 3,
            "category": 1
        }

        self.question_incomplete = {
            "answer": "100 thousand million stars",
            "category": 1
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

    def test_add_film():
        res = self.client().post("/film", json=self.test_film_valid, headers=bearer_token(STUDIO_TOKEN))
        self.assertEqual(res.status_code,200)

    def test_category(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)        
        self.assertEqual(res.status_code,200)

    def test_category_fail(self):
        # try to use delete HTTP method - expect a 405 HTTP error
        res = self.client().delete("/categories")
        self.assertEqual(res.status_code,405)

    def test_question_happy(self):
        res = self.client().get("/questions?page=2")
        data = json.loads(res.data)        
        self.assertEqual(res.status_code,200)
        # tries to load page 2 of questions - should succeed with 200

    def test_question_fail_high_pagination(self):
        res = self.client().get("/questions/7")
        self.assertEqual(res.status_code,405)
        # this tries to load a non-existant page of questions - expect 405

    def test_question_create(self):
        res = self.client().post("/questions", json=self.question_to_add)
        self.assertEqual(res.status_code,200)

    def test_question_create_fail(self):
        res = self.client().post("/questions", json=self.question_incomplete)
        self.assertEqual(res.status_code,200)

    def test_question_delete(self):
        res = self.client().post("/questions", json=self.question_to_add)
        data = json.loads(res.data)
        added_id = data["created"]
        res = self.client().delete("/questions/{}".format(added_id))
        self.assertEqual(res.status_code, 200)

    def test_question_delete_fail(self):
        # try to delete an invalid question ID
        res = self.client().delete("/questions/7766")
        # expect to see a 404 Not Found
        self.assertEqual(res.status_code, 404)

    def test_question_search(self):
        # try searching for something we know is in a question
        search_payload = {"searchTerm": "graph"}
        res = self.client().post("/questions/search", json=search_payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["questions"]), 2)

    def test_question_search_failure(self):
        # try searching for something that isn't in any questions
        search_payload = {"searchTerm": "null"}
        res = self.client().post("/questions/search", json=search_payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["questions"]), 0)

    def test_simulate_quiz_happy(self):
        self.get_next_question = {
            "previous_questions": [13, 14],
            "quiz_category": {"type": "Geography", "id": "3"},
        }
        # We assume that the user has chosen Geography topic;
        # last two questions are specified. Check correct question
        # that was not yet asked, is returned.
        res = self.client().post("/quizzes", json=self.get_next_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["question"].get("id"), 15)

    def test_simulate_quiz_unhappy(self):
        self.get_next_question = {
            "previous_questions": [13, 14, 15],
            "quiz_category": {"type": "Geography", "id": "3"},
        }
        # We assume that the user has chosen Geography topic;
        # last three questions are specified. 
        # Check that quiz ends.
        res = self.client().post("/quizzes", json=self.get_next_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["forceEnd"], "true")
        
    def test_question_search_unhappy(self):
        search_payload = {"searchTerm": "xyzxyz"}
        res = self.client().post("/questions/search", json=search_payload)
        data = json.loads(res.data)

        # confirm that no questions are returned, when incorrect search term provided:
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["questions"]), 0)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()