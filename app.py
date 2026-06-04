from flask import Flask, render_template, url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_login import LoginManager,UserMixin,login_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash,check_password_hash
import re

db = SQLAlchemy()
lm = LoginManager()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User{self.usename}>"
    


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] =  'legit-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
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
        return render_template("index.html")
    
    @app.route('/dashboard')
    def dashboard():
        return render_template("dashboard.html")
    
    @app.route('/register', methods=["GET", "POST"])
    def register():
        errors = []

        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            email = (request.form.get("email") or "").strip()
            password = request.form.get("password") or ""
            confirm = request.form.get("confirm_password") or ""

            if not (6 <= len(username) <= 20):
                errors.append("Username must be between 6 and 20 characters")

            if not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+$", email):
                errors.append("Please enter a valid email address")

            if len(password) < 6:
                errors.append("password need to be at least 6 characters")

            if password != confirm:
                errors.append("password does not match")

            if not errors:

                try:
                    pw_hash = generate_password_hash(password)
                    user = User(username=username, email=email, password_hash=pw_hash)
                    db.session.add(user)
                    db.session.commit()
                    
                    return redirect(url_for('login'))
                except IntegrityError:
                    db.session.rollback()
                    errors.append("that username or email already exist")


                
                return f"valid input recieved - {email}"    

        return render_template("register.html", errors = errors)
    
    @app.route('/login',  methods=["GET", "POST"])
    def login():
        errors = []

        if request.method == "POST":
            email = (request.form.get("email") or "").strip()
            password = request.form.get("password") or ""

            if not email:
                errors.append("email is required")

            if not password:
                errors.append("password is required")

            if not errors:
                user = User.query.filter_by(email=email).first()

            if not user or not check_password_hash(user.password_hash, password):
                errors.append("Invalid email or password")
            else:
                login_user(user)
                return redirect(url_for('dashboard'))

            
        
        return render_template("login.html", errors=errors)
    
    @lm.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app




if __name__ == "__main__":
    app = create_app()
    app.run()
