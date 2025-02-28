from init import db, ma
from marshmallow_sqlalchemy import fields


class Course(db.Model):
    __tablename__ = 'courses'
    __table_args__ = {'schema': 'academy'}  # Specify the schema


    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(200), nullable = False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    teacher_id = db.Column(db.Integer, db.ForeignKey('academy.teachers.id'))
    teacher_info = db.relationship('Teacher', back_populates = 'teacher_courses')
                        
class CourseSchema(ma.Schema):
    teacher_info = fields.Nested('TeacherSchema')

    class Meta:
        fields = ('id', 'name', 'start_date', 'end_date', 'teacher_id', 'teacher_info')

one_course = CourseSchema()
many_courses = CourseSchema(many = True, exclude=['teacher_info'])

course_without_id = CourseSchema(exclude=['id'])



