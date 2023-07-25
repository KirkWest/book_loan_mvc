from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.books import Books, BooksSchema
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
    
@books_bp.route('/', methods=['POST'])
@jwt_required()
def add_book():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user.is_admin:
        return {'error': 'Only admins can add a book'}, 403

    data = request.get_json()
    new_book = Books(title=data['title'], author=data['author'], genre_id=data['genre_id'])
    db.session.add(new_book)
    db.session.commit()
    return books_schema.jsonify(new_book), 201

@books_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_book(id):
    book = Books.query.get(id)
    if not book:
        return {'error': f'Book not found with id {id}'}, 404

    data = request.get_json()

    if 'title' in data:
        book.title = data['title']

    if 'author' in data:
        book.author = data['author']

    if 'genre_id' in data:
        book.genre_id = data['genre_id']

    db.session.commit()
    return books_schema.jsonify(book)

@books_bp.route('/<int:id>', methods=['DELETE'])
def delete_one_book(id):
    book = Books.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return {'message': f'Book {book.title} deleted successfully'}
    else:
        return {'error': f'Book not found with id {id}'}, 404