import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random


from models import setup_db, Question, Category,db

QUESTIONS_PER_PAGE = 10

def pagination_question(request , choise):

  page = request.args.get("page", 1 , type=int)
  start = (page - 1)*QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [
    question.format() for question in choise]
  paginated_questions = questions[start:end]

  return paginated_questions





def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
   
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    CORS(app, resources={r"/*":{'origins':'*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
  
    """

    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods','GET,POST,DELETE,PUT,OPTIONS')
      response.headers.add('Access-Control-Allow-Credentials','true')
     
    
      return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.get('/categories')
    def all_categoris():
      try:
        list_category = Category.query.all()
        if list_category is None :
          abort(404)
        list_all = {}

        for category in list_category:
          list_all [category.id] = category.type  
        return  {
          "success":True,
          "categories" :list_all
        } 
      except:
        abort(404)
   
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.get('/questions')
    def get_all_questions():
      
      questions =  Question.query.all()
      totalQuestions= len(questions)
      pg=pagination_question(request,questions) # 1 [10]

      if len(pg)==0:
        abort(404)

      
   


      
      Lscategories = Category.query.all()
      listAll ={}
      for category in Lscategories:
        listAll[category.id] = category.type

        # abort(404)
        
     
      
      return jsonify({
        'success': True,
        'questions': pg,
        "total_questions":totalQuestions,
        'categories':listAll,
        'currentCategory':None
      })
    

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.delete('/questions/<int:q_id>')
 
    def delete_questions(q_id):
      question = db.session.query(Question).filter(Question.id == q_id).first()

      if question is None:
        abort(404)

      Question.delete(question)

      return{
        'success':True
      }
  

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.post('/questions')
    def new_questions():
      data = request.get_json()
      question = data.get('question',None)
      answer = data.get('answer',None)
      difficulty = data.get('difficulty',None)
      category = data.get('category',None)

      if question is None or answer is None or difficulty is None or category is None:
        abort(422)

      try: 
        
        question = Question(question=question , answer=answer , difficulty=difficulty,category=category)

        Question.insert(question)
        return {
        'success':True
        }

      except:
        abort(422)
      



     
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.post('/search')
    def search_item():
      body=request.get_json()
      search_key = body.get('searchTerm')
      question = db.session.query(Question).filter(Question.question.ilike(f"%{search_key}%")).all()
      if question:
        totalQuestion=len(question)
        pg_que=pagination_question(request,question)
        return {
          "success":True,
          "questions":pg_que,
          "total_questions":totalQuestion,
          "current_category":None
        }


      pass
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')

    def get_category(category_id):

      get_categ = db.session.query(Category).filter(Category.id==category_id).first()
      if get_categ:
        question = db.session.query(Question).filter(Question.category == get_categ.id).all()
         
        totalQuestion=len(question)
        pg_que=pagination_question(request,question)
        return {
          "success":True,
          "questions":pg_que,
          "total_questions":totalQuestion,
          "current_category":get_categ.type
        }



    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.post("/quizzes")
    def play_quizzes():
        data = request.get_json()
        previousQuestions = data.get("previous_questions")
        quiz_category = data.get("quiz_category")

        try:
            # find all qouestions with in that category
            questions_by_ctg = (
                db.session.query(Question).all()
                if quiz_category.get("id") == 0
                else db.session.query(Question)
                .filter(Question.category == quiz_category.get("id"))
                .all()
            )

            question = None
            random_index = random.randint(0, len(questions_by_ctg) - 1)
            if questions_by_ctg:
                question = questions_by_ctg[random_index]

            return {"question": question.format()}
        except:
            abort(400)  
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
      return jsonify({
        'success':False,
        'error':404,
        'message':'not found'

      }),404
    @app.errorhandler(422)
    def unprocesible(error):
      return jsonify({
        'success':False,
        'error':422,
        'message':'unprocesible'



      }),422 


    @app.errorhandler(400)
    def unprocesible(error):
       return jsonify({
          'success':False,
          'error':400,
          'message':'unprocesible'



      }),400 

    return app

