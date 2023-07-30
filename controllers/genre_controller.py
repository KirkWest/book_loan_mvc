from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.genres import Genres, GenresSchema

genre_bp = Blueprint('genre', __name__, url_prefix='/genres')
genre_schema = GenresSchema()
genres_schema = GenresSchema(many=True)

@genre_bp.route('/', methods=['GET']) # retrieves all genres and dumps them in JSON form
def get_all_genres():
    genres = Genres.query.all()
    return genres_schema.dump(genres)

@genre_bp.route('/', methods=['POST']) # creates new genres
def create_genre():
    data = request.get_json()
    genre_name = data.get('genre_name')

    if not genre_name or not genre_name.strip():
        return {'error': 'Genre name is required and cannot be empty'}, 400
    
    new_genre = Genres(
        genre_name=data['genre_name'],
        description=data.get('description')
    )
    try:
        db.session.add(new_genre)
        db.session.commit()
        return genre_schema.jsonify(new_genre), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error': 'Genre name already exists'}, 409
        return {'error': 'An error occurred while attempting to create the genre'}, 500 # catch all error for anything unforseen comes up