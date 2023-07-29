from init import db, ma

# Creates Genres model for genres table in db
class Genres(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)

    # defines relationship between books and genre
    books = db.relationship('Books', back_populates='genre')

class GenresSchema(ma.Schema):
    class Meta: # specifies fields for serialised output
        fields = ('id', 'genre_name', 'description')