from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.students import Student, many_students, one_student, student_without_id

students_bp = Blueprint('students', __name__)

# Read all - GET /students
@students_bp.route('/students')
def get_all_students():
    stmt = db.select(Student).order_by(Student.name.desc())
    students = db.session.scalars(stmt)
    return many_students.dump(students)


# Read one - GET / students/ <int:id>
@students_bp.route('/students/<int:student_id>')
def get_one_student(student_id):
    stmt = db.select(Student).filter_by(id = student_id)
    student = db.session.scalar(stmt)
    if student:
        return one_student.dump(student)
    else:
        return {'error': f'student with id {student_id} does not exits'}, 404

# Create - POST / students
@students_bp.route('/students', methods = ['POST'])
def create_student():
    try:
        # Get incoming request body(json)
        data = student_without_id.load(request.json)
        # Create a new instance of student modelc
        new_student = Student(
            name = data.get('name'),
            email = data.get('email'),
            address = data.get('address')
        )
        # Add the instance to the db session
        db.session.add(new_student)
        # Commit the session
        db.session.commit()
        # Return the new student instance 
        return one_student.dump(new_student), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: 
            # unique violation
            return {"error": "email address already in use"}, 409
        elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return{"error": "Field is required"}, 400
        else:
            return{"error": err._message()}, 400


    

# Update - PUT / students / <int:id>
@students_bp.route('/students/<int:student_id>', methods = ['PUT', 'PATCH'])
def update_student(student_id):
    try:
        
        # Fetch student by id
        stmt = db.select(Student).filter_by(id = student_id)
        student = db.session.scalar(stmt)
        if student:
            # Get incoming request body
            data = student_without_id.load(request.json)
            # update the attribute of the student with the incoming data
            student.name = data.get('name') or student.name
            student.email = data.get('email') or student.email
            student.address = data.get('address') or student.address

            db.session.commit()
            return one_student.dump(student)
        else:
            return {'error': f'Student with id {student_id} does not exist'}, 404 
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return{"error": "email address already in use"}, 409
        else:
            return{"error": err._message()}, 400

# Delete - DELETE/ students / <int:id>
@students_bp.route('/students/<int:student_id>', methods = ['DELETE'])
def delete_student(student_id):
    stmt = db.select(Student).filter_by(id = student_id)
    student = db.session.scalar(stmt)
    if student:
        db.session.delete(student)
        db.session.commit()
        return {}, 204
    else:
        return {'error': f'Student with id {student_id} does not exist'}, 404

# possible extra route
# Enrol - Post / students/ <int:student_id>/ <int:course_id>
# Unenrol - DELETE/ students/ <int:student_id>/ <int:course_id>



