from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.books import Books, BooksSchema
from models.genres import Genres, GenresSchema
from models.user import User

books_bp = Blueprint('books', __name__, url_prefix='/books')
books_schema = BooksSchema()
books_schemas = BooksSchema(many=True)

@books_bp.route('/', methods=['GET']) # retrieves all books
def get_all_books():
    books = Books.query.all()
    return books_schemas.dump(books)

@books_bp.route('/<int:id>', methods=['GET'])
def get_one_book(id):
    book = Books.query.get(id)
    if book:
        return books_schema.jsonify(book)
    else:
        return {'error': f'Book not found with id {id}'}, 404
    
@books_bp.route('/', methods=['POST']) # Adds new book to database
@jwt_required()
def add_book():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user.is_admin:
        return {'error': 'Only admin can add a book'}, 403

    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    genre_name = data.get('genre_name')

    # error code for missing fields
    if not title or not author or not genre_name:
        return {'error': 'title, author, and genre are required'}, 400

    # checks if genre with that name exists
    genre = Genres.query.filter_by(genre_name=genre_name).first()

    if not genre: # if genre doesn't aleady exist it will create the new genre
        genre = Genres(genre_name=genre_name)
        db.session.add(genre)
        db.session.commit()

    new_book = Books(title=data['title'], author=data['author'], genre=genre)
    db.session.add(new_book)
    db.session.commit()
    return books_schema.jsonify(new_book), 201

@books_bp.route('/<int:id>', methods=['PUT', 'PATCH']) # updates any information for a chosen book using the books ID
def update_book(id):
    book = Books.query.get(id)
    if not book:
        return {'error': f'Book not found with id {id}'}, 404

    data = request.get_json()
    genre_name = data.get('genre_name')

    genre = Genres.query.filter_by(genre_name=genre_name).first()

    if not genre:
        genre = Genres(genre_name=genre_name)
        db.session.add(genre)

    if 'title' in data:
        book.title = data['title']

    if 'author' in data:
        book.author = data['author']

    book.genre = genre
    db.session.commit()
    return books_schema.jsonify(book)

@books_bp.route('/<int:id>', methods=['DELETE']) # deltes a book if needed
def delete_one_book(id):
    book = Books.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return {'message': f'Book {book.title} deleted successfully'}
    else:
        return {'error': f'Book not found with id {id}'}, 404