from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_user, logout_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash,check_password_hash
import re
from app.extensions import db
from app.models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/register', methods=["GET", "POST"])
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
                    
                    flash("Account created successfully!, Please login", "success")
                    return redirect(url_for('auth.login'))
                except IntegrityError:
                    db.session.rollback()
                    errors.append("that username or email already exist")


                
                return f"valid input recieved - {email}"    

        return render_template("register.html", errors = errors)
    
@auth_bp.route('/login',  methods=["GET", "POST"])
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
                    remember_flag = request.form.get("remember") == "1"
                    login_user(user, remember=remember_flag)
                    flash(f"Welcome back, {user.username}", "success")

                    #urlparse("https://example.com/page")
                    # scheme="https", metloc='example.com', pah='/page'



                    return redirect(url_for('dashboard'))

            
        
        return render_template("login.html", errors=errors)
    
@auth_bp.route('/logout')
def logout():
        logout_user()
        flash("You have been logged out", "success")
        return redirect(url_for('index'))
    
@auth_bp.route('/change-password', methods=["GET","POST"])
def change_password():
        #to be completed
        errors = []
        
        if request.methods == "POST":
            current_pw = request.forms.get("current_password")
            new_pw = request.forms.get("new_password")
            confirm_pw = request.forms.get("confirm_password")

            return render_template(url_for("auth.change_password.html", errors=errors))

    