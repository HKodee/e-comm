from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
lm = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] =  'legit-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///memory.db:"
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

    db.init_app(app)
    lm.init_app(app)
    lm.login_view = "login"
    
    @app.route('/')
    def index():
        return render_template("index.html")
    
    @app.route('/')
    def register():
        return render_template("register.html")
    
    @app.route('/')
    def login():
        return render_template("login.html")
    
    @lm.user_loader
    def login_user(user_id):
        return
    
    return app




if __name__ == "__main__":
    app = create_app()
    app.run()
