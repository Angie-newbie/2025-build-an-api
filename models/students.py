from init import db, ma

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Interger, primary_key = True)

    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(200), nullable = False)
    address = db.Column(db.String(250))
                        
class Student(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'address')

one_student = StudentSchema()
many_students = StudentSchema(many = True)