from flask import Blueprint
from init import db
from datetime import date
from models.students import Student
from models.teachers import Teacher
from models.courses import Course

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

    db.session.add_all(teachers)
    db.session.commit()

    courses = [
        Course(
            name = 'Diploma of Web Development',
            start_date = date(2025, 10, 1),
            end_date = date(2026, 4, 20),
            teacher_id = teachers[1].id
        ), 
        Course(
            name = 'Diploma of Cybersecurity',
            start_date = date(2026, 1, 26),
            end_date = date(2026, 7, 10),
            teacher_id = teachers[0].id
        )
    ]

    db.session.add_all(students)
    db.session.add_all(courses)
    db.session.commit()
    print('table seeded')