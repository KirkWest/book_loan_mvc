from flask import Blueprint, request, jsonify
from init import db, bcrypt
from models.user import User, user_schema, users_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth') # any route we create will now have prefix of auth

@auth_bp.route('/register', methods=['POST']) # register user route
def auth_register():
    try:
        body_data = request.get_json()

        # validate password length
        password = body_data.get('password')
        if not password or len(password) < 8:
            return {'error': 'Password must have 8 or more characters'}, 400

        user = User() # user model instance for our user class
        user.name = body_data.get('name')
        user.email = body_data.get('email')
        user.address = body_data.get('address')
        if body_data.get('password'): # generates a hashed password
            user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')

        db.session.add(user)
        db.session.commit()

        return user_schema.dump(user), 201 # 201 message = created
    except IntegrityError as err: # handling the possible errors in registering a user
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error': 'Email address is already in use'}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} must be entered'}, 409 # the f string allows us to dynamically change the error message depending on the column name

@auth_bp.route('/login', methods=['POST']) # login route for users with checks for existing user and correct password
def auth_login():
    body_data = request.get_json() # gets JSON data from body
    stmt = db.select(User).filter_by(email=body_data.get('email'))
    user = db.session.scalar(stmt)

    # if user exists it checks the password matches what is stored and returns the users email, token, and admin status
    if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=4)) # token expires in 4 hours
        return{'email': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        # error message if user doesn't exist
        return {'error': 'Invalid email or password'}, 401
    
# gets all users
@auth_bp.route('/get_all_users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return users_schema.jsonify(users), 200