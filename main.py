from flask import Flask
from init import db, ma
import os
from marshmallow import ValidationError
from blueprints.db_bp import db_bp
from blueprints.students_bp import students_bp
from blueprints.teachers_bp import teachers_bp
from blueprints.courses_bp import courses_bp


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
    

    db.init_app(app)
    ma.init_app(app)


    @app.errorhandler(ValidationError)
    def validation_error(err):
        return{"error": str(err)}, 400

    app.register_blueprint(db_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(courses_bp)

    return app


