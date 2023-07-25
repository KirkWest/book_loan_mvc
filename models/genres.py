from init import db, ma

class Genres(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)

class GenresSchema(ma.Schema):
    class Meta:
        fields = ('id', 'genre_name', 'description')