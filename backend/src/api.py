import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
drop all schemas and re-create them
'''
# db_drop_and_create_all()

@app.after_request
def after_request(response):

    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')

    return response

## ROUTES

'''
Endpoint: GET /drinks
'''

@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in drinks]
    }), 200


'''
Endpoint: GET /drinks-detail
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_details(payload):

    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    }), 200

'''
Endpoint: POST /drinks
'''

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(payload):

     body = request.get_json()

     if not body:
         abort(400)

     if not ('title' in body and 'recipe' in body):
         abort(422)

     title = body.get('title')
     recipe = body.get('recipe')

     drink_obj = Drink(title=title, recipe=json.dumps(recipe))

     drink_obj.insert()

     newly_added_drink = Drink.query.filter_by(id=drink_obj.id).first()

     print("newly added obj is ",newly_added_drink)

     return jsonify({
         'success': True,
         'drinks': [newly_added_drink.long()]
     }), 200

'''
Endpoint: PATCH /drinks/<drink_id>
'''

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):

    body = request.get_json()

    if not body:
        abort(400)

    if not ('title' in body or 'recipe' in body):
        abort(422)

    try:
        title = body.get('title')
        recipe = body.get('recipe')

        drink_obj = Drink.query.filter(Drink.id == drink_id).first()

        if not drink_obj:
            abort(404)

        if title:
            drink_obj.title = title
        if recipe:
            drink_obj.recipe = json.dumps(recipe)

        drink_obj.update()

        return jsonify({
            'success': True,
            'drinks': [Drink.long(drink_obj)]
        }), 200
    except:
        abort(422)

'''
Endpoint: DELETE /drinks/<drink_id>
'''

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(token, drink_id):

    try:
        drink_obj = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink_obj is None:
            abort(404)

        drink_obj.delete()

        return jsonify({
            'success': True,
            'deleted': drink_id
        }), 200
    except:
        abort(422)



## Error Handling

'''
Error: 422 (unprocessable entity)
'''

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable entity"
                    }), 422

'''
Error: 400 (bad request)
'''

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
    }), 400

'''
Error: 401 (unauthorized user)
'''

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'unauthorized'
    }), 401

'''
Error: 404 (resource not found)
'''

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404

'''
Error: 405 (method not implemented)
'''

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed on this resource'
    }), 405

'''
Error: 500 (internal server error)
'''

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500

'''
Error: 401 (Authentication Error)
'''

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    """
    ADD SOME MEANINGFUL COMMENT ABOUT THIS HANDLER
    """

    return jsonify({
        'success': False,
        'error': ex.status_code,
        'message': ex.error
    }), 401


## Main method implemented below

if __name__ == "__main__":
    app.run(debug=True)