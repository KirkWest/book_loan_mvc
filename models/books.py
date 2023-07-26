from init import db, ma

# using a similar format to user.py
class Books(db.Model): 
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False)

    # added relationship to access genre name
    genre = db.relationship('Genres', back_populates='books')

class BooksSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author', 'author', 'genre_id')