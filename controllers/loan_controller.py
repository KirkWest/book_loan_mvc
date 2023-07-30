from flask import Blueprint, request, jsonify
from init import db
from models.loans import Loans, LoansSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

loan_bp = Blueprint('loan', __name__, url_prefix='/loans')
loan_schema = LoansSchema()
loans_schema = LoansSchema(many=True)

# get all loans and dumps them in JSON format
@loan_bp.route('/', methods=['GET'])
def get_all_loans():
    loans = Loans.query.all()
    return jsonify(loans_schema.dump(loans))

# gets one loan and dumps in JSON format
@loan_bp.route('/<int:id>', methods=['GET'])
def get_one_loan(id):
    loan = Loans.query.get(id)
    if loan:
        return loan_schema.jsonify(loan)
    else:
        return {'error': 'Loan does not exist'}, 404

# creates new loan
@loan_bp.route('/', methods=['POST'])
def create_loan():
    data = request.get_json()

    # added validation check that will alert the user of what fields are missing
    required_fields = ['user_id', 'book_id']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        missing_fields_str = ', '.join(missing_fields)
        return {'error': f'You are missing these fields: {missing_fields_str}'}, 400
    
    #creates loan date automatically using datetime
    loan_date = datetime.now()
    
    # creates new loan
    new_loan = Loans(
        user_id=data['user_id'],
        book_id=data['book_id'],
        loan_date=loan_date,
        returned=False
    )

    db.session.add(new_loan)
    db.session.commit()

    return loan_schema.jsonify(new_loan), 201

    
@loan_bp.route('/<int:id>', methods=['PATCH']) # lets us update a loan using JWT by setting the boolean to True or False depending on loan status
@jwt_required()
def update_loan(id):
    body_data = request.get_json()
    stmt = db.select(Loans).filter_by(id=id)
    loan = db.session.scalar(stmt)
    if loan:
        if str(loan.user_id) != get_jwt_identity():
            return {'error': 'You are not authorized to update this loan'}, 403

        if 'returned' in body_data:
            loan.returned = body_data['returned']

        db.session.commit()
        return loan_schema.dump(loan)
    else:
        return {'error': f'Loan not found with id {id}'}, 404
    
@loan_bp.route('/<int:id>', methods=['DELETE']) # Lets us delete a loan if we wish to clean up the system from old loans, JWT required
@jwt_required()
def delete_loan(id):
    loan = Loans.query.get(id)
    if loan:
        user_id = get_jwt_identity()
        if loan.user != user_id:
            return {'error': 'You do not have permission to delete'}, 403
        
        db.session.delete(loan)
        db.session.commit()
        return {'message': 'Loan deleted'}
    else:
        return {'error': 'Loan does not exist'}, 404