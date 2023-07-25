from flask import Blueprint, request
from init import db
from models.loans import Loans, LoansSchema

loan_bp = Blueprint('loan', __name__, url_prefix='/loans')
loan_schema = LoansSchema()
loans_schema = LoansSchema(many=True)

@loan_bp.route('/', methods=['GET'])
def get_all_loans():
    loans = Loans.query.all()
    return loans_schema.dump(loans)

@loan_bp.route('/', methods=['POST'])
def create_loan():
    data = request.get_json()
    new_loan = Loans(
        user_id=data['user_id'],
        book_id=data['book_id'],
        loan_date=data['loan_date'],
        returned=False
    )
    db.session.add(new_loan)
    db.session.commit()
    return loan_schema.jsonify(new_loan), 201

# need to add more routes as needed for updating loans, marking loans as returned, etc.
