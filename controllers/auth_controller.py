from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, user_schema, users_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

auth_bp = Blueprint('auth', __name__, url_prefix='/auth') # any route we create will now have prefix of auth

@auth_bp.route('/register', methods=['POST']) # register is post method
def auth_register():
    try:
        body_data = request.get_json()

        user = User() # user model instance for our user class
        user.name = body_data.get('name')
        user.email = body_data.get('email')
        user.address = body_data.get('address')
        if body_data.get('password'):
            user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')

        db.session.add(user)
        db.session.commit()

        return user_schema.dump(user), 201 # 201 message = created
    except IntegrityError as err: # handling the possible errors in registering a user
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error': 'Email address is already in use'}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} must be entered'}, 409 # the f string allows us to dynamically change the error message depending on the column name
