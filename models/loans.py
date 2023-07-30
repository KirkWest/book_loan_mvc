from init import db, ma
from datetime import datetime

# Creates Loans model for loans in db
class Loans(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False, unique=True)
    loan_date = db.Column(db.Date, default=datetime.now, nullable=False)
    returned = db.Column(db.Boolean, default=False)

    # relationships between User-loans and Books-loan(books-loan is a one to one relationship)
    user = db.relationship('User', back_populates='loans')
    book = db.relationship('Books', back_populates='loan', uselist=False)

class LoansSchema(ma.Schema):
    class Meta: # serilised output for loans fields
        fields = ('id', 'user_id', 'book_id', 'loan_date', 'returned')