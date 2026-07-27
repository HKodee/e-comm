from flask import Flask, render_template, url_for, request, redirect, flash
from app.extensions import db, lm
from sqlalchemy import text
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse
from datetime import timedelta
import re
from app.models import User,Employee

    


def create_app():
    app = Flask(
        __name__,
        template_folder="app/templates",
        static_folder="app/static"
    )

    app.config['SECRET_KEY'] =  'legit-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=15)

    db.init_app(app)
    lm.init_app(app)
    lm.login_view = "auth.login"
    
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)

    @app.route("/health/db")
    def health_db():
        try:
            db.session.execute(text("SELECT 1"))
            return {"db":"ok"},200
        except Exception as e:
            return {"db":"error", "detail":str(e)}, 500
        
    with app.app_context():
        db.create_all()


    def _is_safe_local_path(target: str)-> bool:
        if not target:
            return False
        parts = urlparse(target)
        return parts.scheme == "" and parts.netloc == "" and target.startswith("/")
    

    @app.route('/')
    def index():
        return render_template("index.html")
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template("dashboard.html")

    @app.route('/test')
    @login_required
    def test():
        return "TEST PAGE"
    
    @app.route("/make-admin/<email>")
    def make_admin(email):
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return "User not found"
        
        user.role = "admin"
        db.session.commit()
        
        return f"{user.username} is now an admin."
    
    @lm.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
