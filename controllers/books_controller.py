from flask import Blueprint, request, jsonify
from init import db
from models.books import Books, BooksSchema

books_bp = Blueprint('books', __name__, url_prefix='/books')
books_schema = BooksSchema()
books_schemas = BooksSchema(many=True)

@books_bp.route('/', methods=['GET'])
def get_all_books():
    books = Books.query.all()
    return books_schemas.dump(books)

@books_bp.route('/', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Books(title=data['title'], author=data['author'], genre_id=data['genre+id'])
    db.session.add(new_book)
    db.session.commit()
    return books_schema.jsonfy(new_book), 201