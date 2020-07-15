import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json
from models import setup_db, db_drop_and_create_all, ServiceRequest, Hospital
from datetime import datetime, timedelta
from auth.auth import AuthError, requires_auth

SERVICEREQUESTS_PER_PAGE = 5

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
# CORS(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}}) # pylint: disable=unused-variable

  '''
  @TODO uncomment the following line to initialize the datbase
  !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
  !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
  '''
  # PST: Temporarily commented out for database migration
  # db_drop_and_create_all()
  # example_hospital_1 = Hospital(name='Klinikum Muenchen Grosshadern', longitude=11.4734353, latitude=48.112907)
  # example_hospital_1.insert()
  # example_hospital_2 = Hospital(name='Universitaetsklinik Innsbruck', longitude=11.3870319, latitude=47.2634384)
  # example_hospital_2.insert()
  
  '''
  
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response): # pylint: disable=unused-variable
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response
  
  
  '''
  Endpoint to GET servicerequests, 
  including pagination (every 5 servicerequests). 
  '''
  @app.route('/servicerequests', methods=['GET'])
  @requires_auth('get:servicerequests')
  def get_servicerequests(jwt): # pylint: disable=unused-variable
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * SERVICEREQUESTS_PER_PAGE
    end = start + SERVICEREQUESTS_PER_PAGE

    servicerequests = ServiceRequest.query.all()
    formatted_servicerequests = [req.format() for req in servicerequests]
    #datetime_string = datetime.now().strftime("%Y-%m-%d, %H:%M")
    #date_string = datetime.now().strftime("%Y-%m-%d")
    #time_string = datetime.now().strftime("%H:%M")
    #print('datetime: %s' %datetime_string)
    #print('date: %s' %date_string)
    #print('time: %s' %time_string)
    return jsonify({
      'success':True,
      'servicerequests': formatted_servicerequests[start:end],
      'total_servicerequests': len(formatted_servicerequests)})

  
  '''
  Endpoint to GET hospitals, 
  '''
  @app.route('/hospitals', methods=['GET'])
  @requires_auth('get:hospitals')
  def get_hospitals(jwt): # pylint: disable=unused-variable

    hospitals = Hospital.query.all()
    formatted_hospitals = [hospital.format() for hospital in hospitals]
    return jsonify({
      'success':True,
      'hospitals': formatted_hospitals,
      'total_hospitals': len(formatted_hospitals)})

  '''
  Endpoint to DELETE servicerequests
  using a servicerequest ID. 
  '''
  @app.route('/servicerequests/<int:servicerequest_id>', methods=['DELETE'])
  @requires_auth('delete:servicerequest')
  def delete_servicerequest(jwt, servicerequest_id): # pylint: disable=unused-variable
    try:
      selected_servicerequest = ServiceRequest.query.get(servicerequest_id)
      if selected_servicerequest is None:
        abort(404)
      selected_servicerequest.delete()

      servicerequests = ServiceRequest.query.all()
      formatted_servicerequests = [sr.format() for sr in servicerequests]

      return jsonify({
        'success': True,
        'deleted_servicerequest_id': servicerequest_id,
        'total_servicerequests': len(formatted_servicerequests)
      })
    except:
      abort(422)

  '''
  Endpoint to PATCH servicerequest status
  using a servicerequest ID.
  '''
  @app.route('/servicerequests/<int:servicerequest_id>', methods=['PATCH'])
  @requires_auth('patch:servicerequest')
  def update_servicerequest(jwt, servicerequest_id): # pylint: disable=unused-variable
    print(servicerequest_id)
    try:
      selected_servicerequest = ServiceRequest.query.get(servicerequest_id)
      if selected_servicerequest is None:
        abort(404)
      selected_servicerequest.status = 'Scheduled'
      selected_servicerequest.update()

      servicerequests = ServiceRequest.query.all()
      formatted_servicerequests = [sr.format() for sr in servicerequests] # pylint: disable=unused-variable

      return jsonify({
        'success': True,
        'updated_servicerequest_id': servicerequest_id,
        'status': 'Scheduled'
      })
    except:
      abort(422)

  '''
  Endpoint to POST a new servicerequest.
  '''
  @app.route('/servicerequests', methods=['POST'])
  @requires_auth('post:servicerequest')
  def create_servicerequest(jwt): # pylint: disable=unused-variable
    try:
      body = request.get_json()
      new_servicerequest = ServiceRequest(
        service_type='Organ transport',
        origin_airport=body.get('origin_airport', None),
        destination_airport=body.get('destination_airport', None),
        payload=body.get('payload', None),
        payload_weight=body.get('payload_weight', None),
        status='Requested',
        priority=body.get('priority', None),
        user_id=2,
        collection_datetime=body.get('collection_datetime', None),
        delivery_datetime=body.get('delivery_datetime', None),
        latest_delivery_datetime=body.get('latest_delivery_datetime', None)
      )
      new_servicerequest.insert()
      all_servicerequests = ServiceRequest.query.order_by(ServiceRequest.id).all()
      return jsonify({
        'success': True,
        'created': new_servicerequest.id,
        'total_servicerequests': len(all_servicerequests)
      })
    except:
      abort(422)

  # '''
  # @TODO: 
  # Create a GET endpoint to get questions based on category. 

  # TEST: In the "List" tab / main screen, clicking on one of the 
  # categories in the left column will cause only questions of that 
  # category to be shown. 
  # '''
  # @app.route('/categories/<int:categories_id>/questions', methods=['GET'])
  # def get_category_questions(categories_id):
  #   page = request.args.get('page', 1, type=int)
  #   start = (page - 1) * QUESTIONS_PER_PAGE
  #   end = start + QUESTIONS_PER_PAGE

  #   searched_questions = Question.query.filter_by(category=str(categories_id)).all()
  #   formatted_questions = [question.format() for question in searched_questions]
  #   print('length_formatted_questions %s' %len(formatted_questions))
  #   if len(formatted_questions) == 0:
  #     print('Hi')
  #     abort(404)

  #   try:
  #     #body = request.get_json()
  #     #search_term = body.get('searchTerm', '')
  #     #print(search_term)

  #     return jsonify ({
  #       'success' : True,
  #       'questions': formatted_questions[start:end],
  #       'total_questions': len(formatted_questions),
  #       'current_category': None
  #     })

  #   except:
  #     abort(422)

  '''
  Error handlers for all expected errors,
  including 400, 404, 422 and auth errors 401, 403
  '''

  @app.errorhandler(400)
  def bad_request(error): # pylint: disable=unused-variable
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "Bad request."
      }), 400

  @app.errorhandler(404)
  def not_found(error): # pylint: disable=unused-variable
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Resource not found."
      }), 404

  @app.errorhandler(422)
  def unprocessable(error): # pylint: disable=unused-variable
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "Unprocessable."
      }), 422
  
  '''
  Error handler for AuthError
  '''
  @app.errorhandler(AuthError)
  def auth_error(error): # pylint: disable=unused-variable
      return jsonify({
                      "success": False,
                      "error": error.status_code,
                      "message": error.error['description']
                      }), error.status_code
  
  return app

# PST: Temporarily added for database migration
app = create_app()
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(host='127.0.0.1', port=5000, debug=True)

# python -m venv venv
# venv\Scripts\activate
# set FLASK_APP=flaskr
# set FLASK_ENV=development
# flask run
# conda create -n flask_env python=3.7
# conda create -n flask_auth_env python=3.7
# conda activate flask_env
# conda install -n flask
# conda install -c anaconda sqlalchemy
# conda install -c conda-forge flask-migrate
# conda install -c anaconda flask-cors
# conda install -c conda-forge flask-restful
# conda install -c conda-forge python-jose
# conda install -c anaconda psycopg2
# conda install -c anaconda requests
# conda deactivate
# conda info -e
# conda list -e > requirements.txt
# conda create --name flask_auth_env --file requirements.txt
# conda remove -n venv --all
# set FLASK_APP=flaskr
# set FLASK_ENV=development
# flask run
# psql -h localhost -p 5432 -U postgres trivia < C:\Users\Public\trivia.psql
# INSERT INTO requests (orig_airport, destination_airport, organ, organ_mass, max_transp_time, max_transp_cost, priority) VALUES ('Universitaetsklinik Innsbruck', 'Klinikum Grosshadern', 'Kidney', 1, 1, 2000, 1)
# curl -X POST -d '{"origin_airport":"Universitaetsklinik Innsbruck", "destination_airport":"Klinikum Grosshadern", "payload":"Kidney", "payload_weight":"5", "priority":"High"}' -H 'Content-Type: application/json' localhost:5000/servicerequests
# localhost:5000/servicerequests
# curl -X DELETE localhost:5000/servicerequests/1
# curl -X PATCH localhost:5000/servicerequests/1
# conda create --name flask_plotly_env --file requirements.txt
# conda create --prefix=/Users/Public/servicebroker/venv flask
# conda activate C:\Users\Public\servicebroker\venv
# https://medium.com/@daniel.carlier/how-to-build-a-simple-flask-restful-api-with-docker-compose-2d849d738137
# https://levelup.gitconnected.com/dockerizing-a-flask-application-with-a-postgres-database-b5e5bfc24848

# Export (in C:\Program Files\PostgreSQL\12\bin):
# pg_dump –U postgres servicebroker > servicebroker.psql
# dropdb -U postgres servicebroker_test
# createdb -U postgres servicebroker_test
# Import:
# psql -h localhost -p 5432 -U postgres servicebroker_test < C:\Users\Public\servicebroker.psql
# psql -h localhost -p 5432 -U postgres servicebroker_test < C:\Users\phili\Python\Udacity\servicebroker\servicebroker.psql

# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade

# Heroku:
# pip freeze > requirements.txt

