import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "student", "student", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    new_question = {
        'question':'sheeg caasimadda somalia',
        'answer':'mogadishu',
        'category':'2',
        'difficulty':'1'
    }

    
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    
    """
    
    # def test_get_questions(self):
    #     res = self.client().get('/questions?page=1')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data.get('success'),True)


    # def test_404_questions(self):
    #     res = self.client().get('/questions?page=1000')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code,404)
    #     self.assertEqual(data.get('success'),False)
    #     self.assertEqual(data.get('message'),'not found')




    #delete questions

    # def test_delete_questions(self):
    #     res = self.client().delete('questions/3')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data.get('success'),True)
    #     self.assertEqual(data.get('message'),'not found')


    # def test_404_questions(self) :
    #     res = self.client().delete('/questions/')
    #     data = json.loads(res.data)
    #     self.assertEqual(data.get('success'),False)
    #     self.assertEqual(data.get('message'),'unprrocesible')   



#create questions


    # def test_create_questions(self):
    #     res = self.client().post('/questions',json=self.new_question)
    #     data = json.loads(res.data)
    #     self.assertEqual(data.get('success'),True)
       

    # def test_400_questions(self):
    #     res = self.client().post('/questions')
    #     print(res)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(data.get('success'),False)


#search questions


    # def test_404_search_questions(self):
       
    #     response = self.client().post('/questions/search', json={
    #         'searchTerm': 'somalia'})
    #     data = json.loads(response.data)


      
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], " not found")

    
    def test_post_quizes(self):
        res = self.client().post(
            "/api/quizzes", json={"previous_questions": None, "quiz_category": "2"}
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data.get("question")))






















if __name__ == "__main__":
    unittest.main()