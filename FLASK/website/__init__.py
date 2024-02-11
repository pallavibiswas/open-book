from flask import Flask, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

DB_NAME = "database.db"
db = SQLAlchemy()

def create_app():

    app = Flask(__name__) #name of app 
    app.config['SECRET_KEY'] = 'hsgdhsjhdgd jagshjkshh' #to save sessions
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) #connects database and app

    from .models import User, Note
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/') #register within flask application

    return app