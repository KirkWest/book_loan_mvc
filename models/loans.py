from init import db, ma
from datetime import datetime


class Loans(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', back_populates='loans')
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    book = db.relationship('Books', back_populates='loans')
    loan_date = db.Column(db.Date, default=datetime.now, nullable=False)
    returned = db.Column(db.Boolean, default=False)

class LoansSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'book_id', 'loan_date', 'returned')