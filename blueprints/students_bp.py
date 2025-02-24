from flask import Blueprint
from init import db
from models.students import Student, many_students, one_student

students_bp = Blueprint('students', __name__)

# Read all - GET /students
@students_bp.route('/students')
def get_all_students():
    stmt = db.select(Student)
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
# Update - PUT / students / <int:id>
# Delete - DELETE/ students / <int:id>

# possible extra route
# Enrol - Post / students/ <int:student_id>/ <int:course_id>
# Unenrol - DELETE/ students/ <int:student_id>/ <int:course_id>


#  update
# @student_dp.route('/studentd/<int:student_id>', method = ['PUT', 'PATCH'])
# def update_student(student_id):
#     try:
        
#         # Fetch student by id
#         stmt = db.select(Student).filter_by(id = student_id)
#         student = db.session.scalar(stmt)
#         if student:
#             # Get incoming request body
#             data = student_without_id.load(request.json)
#             # update the attribute of the student with the incoming data
#             student.name = data.get('name') or student.name
#             email = data.get('email') or student.email
#             address = data.get('address') or student.address

#             db.session.commit()
#             return one_student.dump(student)
#     except IntegrityError as err:
#         if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
#             return{'error': f''}



# delete
# @students_bp.route('/students/<int:student_id>', method = ['DELETE'])
# def delete_student(id):
#     stmt = db.select(Student).filter_by(id = student_id)
#     student = db.session.scalar(stmt)
#     if student:
#         db.session.delete(student)
#         db.session.commit()
#         return {}, 204
#     else:
#         return {'error': f'Student with id {student_id} does not exist'}, 404