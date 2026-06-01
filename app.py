from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return render_template("index.html")
    
    return app




if __name__ == "__main__":
    app = create_app()
    app.run()
