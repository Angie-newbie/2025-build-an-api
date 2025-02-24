from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.teachers import Teacher, many_teachers, one_teacher, teacher_without_id

teachers_bp = Blueprint('teachers', __name__)

# Read all - GET /teachers
@teachers_bp.route('/teachers')
def get_all_teachers():
    stmt = db.select(Teacher).order_by(Teacher.name.desc())
    teachers = db.session.scalars(stmt)
    return many_teachers.dump(teachers)


# Read one - GET / teachers/ <int:id>
@teachers_bp.route('/teachers/<int:teacher_id>')
def get_one_teacher(teacher_id):
    stmt = db.select(Teacher).filter_by(id = teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        return one_teacher.dump(teacher)
    else:
        return {'error': f'teacher with id {teacher_id} does not exits'}, 404

# Create - POST / teachers
@teachers_bp.route('/teachers', methods = ['POST'])
def create_teacher():
    try:
        # Get incoming request body(json)
        data = teacher_without_id.load(request.json)
        # Create a new instance of teacher modelc
        new_teacher = Teacher(
            name = data.get('name'),
            department = data.get('department'),
            address = data.get('address')
        )
        # Add the instance to the db session
        db.session.add(new_teacher)
        # Commit the session
        db.session.commit()
        # Return the new teacher instance 
        return one_teacher.dump(new_teacher), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: 
            # unique violation
            return {"error": "department address already in use"}, 409
        elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return{"error": "Field is required"}, 400
        else:
            return{"error": err._message()}, 400


    

# Update - PUT / teachers / <int:id>
@teachers_bp.route('/teachers/<int:teacher_id>', methods = ['PUT', 'PATCH'])
def update_teacher(teacher_id):
    try:
        
        # Fetch teacher by id
        stmt = db.select(Teacher).filter_by(id = teacher_id)
        teacher = db.session.scalar(stmt)
        if teacher:
            # Get incoming request body
            data = teacher_without_id.load(request.json)
            # update the attribute of the teacher with the incoming data
            teacher.name = data.get('name') or teacher.name
            teacher.department = data.get('department') or teacher.department
            teacher.address = data.get('address') or teacher.address

            db.session.commit()
            return one_teacher.dump(teacher)
        else:
            return {'error': f'Teacher with id {teacher_id} does not exist'}, 404 
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return{"error": "department address already in use"}, 409
        else:
            return{"error": err._message()}, 400

# Delete - DELETE/ teachers / <int:id>
@teachers_bp.route('/teachers/<int:teacher_id>', methods = ['DELETE'])
def delete_teacher(teacher_id):
    stmt = db.select(Teacher).filter_by(id = teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return {}, 204
    else:
        return {'error': f'Teacher with id {teacher_id} does not exist'}, 404

# possible extra route
# Enrol - Post / teachers/ <int:teacher_id>/ <int:course_id>
# Unenrol - DELETE/ teachers/ <int:teacher_id>/ <int:course_id>



