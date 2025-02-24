from flask import Blueprint
from init import db
from models.students import Student
from models.teachers import Teacher

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

    teachers = [
        Teacher(
            name = 'Mr. Robot',
            department = 'Training and Development',
            address = 'Brisbane'
        ),
        Teacher(
            name = 'Alex',
            department = 'Training and Development',
            address = 'Sydney'
        )
    ]

    db.session.add_all(students)
    db.session.add_all(teachers)
    db.session.commit()
    print('table seeded')