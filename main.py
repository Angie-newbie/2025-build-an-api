from flask import Flask
from init import db, ma
import os
from blueprints.db_bp import db_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')


    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_bp)

    return app