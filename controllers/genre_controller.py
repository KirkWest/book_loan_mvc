from flask import Blueprint, request
from init import db
from models.genres import Genres, GenresSchema

genre_bp = Blueprint('genre', __name__, url_prefix='/genres')
genre_schema = GenresSchema()
genres_schema = GenresSchema(many=True)

@genre_bp.route('/', methods=['GET'])
def get_all_genres():
    genres = Genres.query.all()
    return genres_schema.dump(genres)

@genre_bp.route('/', methods=['POST'])
def create_genre():
    data = request.get_json()
    new_genre = Genres(
        genre_name=data['genre_name'],
        description=data.get('description')
    )
    db.session.add(new_genre)
    db.session.commit()
    return genre_schema.jsonify(new_genre), 201

# need to add extra routes for updating and deleting