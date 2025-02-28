from init import db, ma
from marshmallow_sqlalchemy import fields


class Teacher(db.Model):
    __tablename__ = 'teachers'
    __table_args__ = {'schema': 'academy'}  # Specify the schema


    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    department = db.Column(db.String(50), nullable = False)
    address = db.Column(db.String(250))

    
    teacher_courses = db.relationship('Course', back_populates= 'teacher_info')
                        
class TeacherSchema(ma.Schema):
    teacher_courses = fields.Nested('CourseSchema', many=True, exclude=['teacher_info'])
    
    class Meta:
        fields = ('id', 'name', 'department', 'address', 'teacher_courses')

one_teacher = TeacherSchema()
many_teachers = TeacherSchema(many = True)

teacher_without_id = TeacherSchema(exclude=['id'])



