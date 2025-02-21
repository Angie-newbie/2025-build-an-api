from flask import Blueprint
from init import db
from models.students import Student

db_bp = Blueprint('db', __name__)

@db_bp.cli.command('init')
def create_tables():
    db.drop_all()
    db.create_all()
    print('Tables Created')

@db_bp.cli.command('seed')
def seed_tables():
    students = [
        Student(
            name = 'Mary Jones',
            email = 'mary.jons@gmail.com',
            address = 'Sydney'
        ),
        Student( 
            name = 'John Smith',
            email = 'john.smith@outlook.com'
        )
    ]
    db.session.add_all(students)
    db.session.commit()
    print('table seeded')