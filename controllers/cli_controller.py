from flask import Blueprint
from init import db, bcrypt
from models.user import User # create user
from models.books import Books
from models.loans import Loans
from models.genres import Genres
from datetime import date

db_commands = Blueprint('db', __name__) # wrapped our cli controller in blueprint

@db_commands.cli.command('create') # creates tables
def create_all():
    db.create_all()
    print("Tables Created") # prints to client table created

@db_commands.cli.command('drop') # drops tables
def drop_all():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed') # seeds table with User books genre information
def seed_db():
    users = [
        User(
            name='Kirk West',
            email='kirkwestsooby@gmail.com',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            address='10 Branch st Shortland 2307',
            is_admin=True
        ),
        User(
            name='James Rigby',
            email='jamesrigby@gmail.com',
            password=bcrypt.generate_password_hash('user1JR').decode('utf-8')
        ),
        User(
            name='Steve West-Sooby',
            email='stevewestsooby@gmail.com',
            password=bcrypt.generate_password_hash('user2SWS').decode('utf-8')
        )
    ]
    db.session.add_all(users) # adds users

    genres = [
        Genres(
            genre_name='Fantasy',
            description='Typically features the use of magic or other supernatural phenomena in the plot, setting, or theme'
        ),
        Genres(
            genre_name='Autobigraphical',
            description='Biography of oneself narrated by oneself'
        ),
        Genres(
            genre_name='Thrillers',
            description='Action-packed, page-turners with moments full of tension, anxiety, and fear'
        )
    ]
    db.session.add_all(genres) # adds genres

    books = [
        Books(
            title='Book 1',
            author='Author 1',
            genre_id=1
        ),
        Books(
            title='Book 2',
            author='Author 2',
            genre_id=2
        ),
        Books(
            title='Book 3',
            author='Author 3',
            genre_id=3
        )
    ]
    db.session.add_all(books) # adds books

    loans = [
        Loans(
            user_id=1,
            book_id=1,
            loan_date=date.today(),
            returned=False
        ),
        Loans(
            user_id=2,
            book_id=2,
            loan_date=date.today(),
            returned=False
        )
    ]
    db.session.add_all(loans) # adds loans, note: the first 3 tables must be seeded then commented out to then seed loans for testing

    db.session.commit() # commits to db

    print("tables seeded")