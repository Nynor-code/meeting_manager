from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Example config — replace with your actual DB URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/yourdbname'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from . import models  # Ensure models are loaded
        db.create_all()       # Optional: auto-create tables on app start

    return app