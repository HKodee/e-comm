from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_login import LoginManager,UserMixin
import re

db = SQLAlchemy()
lm = LoginManager()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usename = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User{self.usename}>"
    


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] =  'legit-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

    db.init_app(app)
    lm.init_app(app)
    lm.login_view = "login"

    @app.route("/health/db")
    def health_db():
        try:
            db.session.execute(text("SELECT 1"))
            return {"db":"ok"},200
        except Exception as e:
            return {"db":"error", "detail":str(e)}, 500
        
    with app.app_context():
        db.create_all()


    
    @app.route('/')
    def index():
        return render_template("home.html")
    
    @app.route('/register', methods=["GET", "POST"])
    def register():
        errors = []

        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            email = (request.form.get("email") or "").strip()
            password = request.form.get("password") or ""
            confirm = request.form.get("confirm_password") or ""

        if not (6 <= len(username) <= 20):
            errors.append("Username must be between 3 and 80")

        if not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            errors.append("Please enter a valid email address")

        if len(password) < 6:
            errors.append("password need to be at least 6 characters")

        if password != confirm:
            errors.append("password does not match")

        if not errors:
            return f"valid input recieved - {email}"        


        return render_template("register.html", errors = errors)
    
    @app.route('/login')
    def login():
        return render_template("login.html")
    
    @lm.user_loader
    def login_user(user_id):
        return
    
    return app




if __name__ == "__main__":
    app = create_app()
    app.run()
