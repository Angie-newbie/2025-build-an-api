from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.courses import Course, many_courses, one_course, course_without_id

courses_bp = Blueprint('courses', __name__)

# Read all - GET /courses
@courses_bp.route('/courses')
def get_all_courses():
    stmt = db.select(Course).order_by(Course.name.desc())
    courses = db.session.scalars(stmt)
    return many_courses.dump(courses)


# Read one - GET / courses/ <int:id>
@courses_bp.route('/courses/<int:course_id>')
def get_one_course(course_id):
    stmt = db.select(Course).filter_by(id = course_id)
    course = db.session.scalar(stmt)
    if course:
        return one_course.dump(course)
    else:
        return {'error': f'course with id {course_id} does not exits'}, 404

# Create - POST / courses
@courses_bp.route('/courses', methods = ['POST'])
def create_course():
    try:
        # Get incoming request body(json)
        data = course_without_id.load(request.json)
        # Create a new instance of course modelc
        new_course = Course(
            name = data.get('name'),
            start_date = data.get('start_date'),
            end_date = data.get('end_date'),
            teacher_id = data.get('teacher_id')
        )
        # Add the instance to the db session
        db.session.add(new_course)
        # Commit the session
        db.session.commit()
        # Return the new course instance 
        return one_course.dump(new_course), 201
    except Exception as err:
            return{"error": err._message()}, 400


    

# Update - PUT / courses / <int:id>
@courses_bp.route('/courses/<int:course_id>', methods = ['PUT', 'PATCH'])
def update_course(course_id):
    try:
        
        # Fetch course by id
        stmt = db.select(Course).filter_by(id = course_id)
        course = db.session.scalar(stmt)
        if course:
            # Get incoming request body
            data = course_without_id.load(request.json)
            # update the attribute of the course with the incoming data
            course.name = data.get('name') or course.name
            course.start_date = data.get('start_date') or course.start_date
            course.end_date = data.get('end_date') or course.end_date
            course.teacher_id = data.get('teacher_id', course.teacher_id)

            db.session.commit()
            return one_course.dump(course)
        else:
            return {'error': f'Course with id {course_id} does not exist'}, 404 
    except Exception as err:
            return{"error": err._message()}, 400

# Delete - DELETE/ courses / <int:id>
@courses_bp.route('/courses/<int:course_id>', methods = ['DELETE'])
def delete_course(course_id):
    stmt = db.select(Course).filter_by(id = course_id)
    course = db.session.scalar(stmt)
    if course:
        db.session.delete(course)
        db.session.commit()
        return {}, 204
    else:
        return {'error': f'Course with id {course_id} does not exist'}, 404

# possible extra route
# Enrol - Post / courses/ <int:course_id>/ <int:course_id>
# Unenrol - DELETE/ courses/ <int:course_id>/ <int:course_id>



