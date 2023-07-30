from init import db, ma

# Creates a book model for books table in db
class Books(db.Model): 
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False)

    # defines relationships for genres-books and loans-book(one to one relationship for loans and book)
    genre = db.relationship('Genres', back_populates='books')
    loans = db.relationship('Loans', back_populates='book', nullable=False)

class BooksSchema(ma.Schema):
    class Meta: # specifies fields for serilised output
        fields = ('id', 'title', 'author', 'author', 'genre_id')