from flask import Blueprint
from init import db, bcrypt
from models.user import User # create user

db_commands = Blueprint('db', __name__) # wrapped our cli controller in blueprint

@db_commands.cli.command('create') # creates tables
def create_all():
    db.create_all()
    print("Tables Created") # prints to client table created

@db_commands.cli.command('drop') # drops tables
def drop_all():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
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
    db.session.commit() # commits to db