from flask import Flask
import os
from init import db, ma, bcrypt, jwt # imports instances
from controllers.cli_controller import db_commands # imports blueprint from client controller
from controllers.auth_controller import auth_bp
from controllers.books_controller import books_bp
from controllers.loan_controller import loan_bp
from controllers.genre_controller import genre_bp

# define app
def create_app():
    app = Flask(__name__) # create flask app
    
    # data bases URI and JWT secret key      dbms       driver     user      pwd     uri    port  db_name
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")

    # initialise with application
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands) # registers blueprint to app
    app.register_blueprint(auth_bp) # registers our authorisation blueprint
    app.register_blueprint(books_bp) # registers our books blueprint
    app.register_blueprint(loan_bp) # registers our loan blueprint
    app.register_blueprint(genre_bp) # registers our genre blueprint

    # return that app from the create_app function
    return app

