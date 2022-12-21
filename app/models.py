from app import db
#from sqlalchemy import func
from datetime import datetime


class User(db.Model):
  __tablename__ = 'user'

  id =                    db.Column(db.Integer, primary_key=True)
  name =                  db.Column(db.String(64), nullable=False)
  email =                 db.Column(db.String(120), index=True, nullable=False)
  isAdmin =               db.Column(db.Boolean, nullable=False, default=False)
  provider =              db.Column(db.String(25))
  picture =               db.Column(db.String(250))
  lastSeen =              db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  numberOfTimesLoggedIn = db.Column(db.Integer, default=1)

  @property
  def is_authenticated(self):
      return True

  @property
  def is_active(self):
      return True

  @property
  def is_anonymous(self):
      return False

  def get_id(self):
      try:
          return unicode(self.id)  # python 2
      except NameError:
          return str(self.id)  # python 3

  def __repr__(self):
      return '<User id:%r , name:%r , email:%r>' % (self.id, self.name, self.email)



class Student(db.Model):
  __tablename__ = 'student'
   
  id =                    db.Column(db.Integer, primary_key=True)
  firstName =             db.Column(db.String(25), nullable=False)
  lastName =              db.Column(db.String(25), nullable=False)  
  middleName =            db.Column(db.String(25)) 
  title =                 db.Column(db.String(4))
  telephoneNumber =       db.Column(db.String(25))
  mobilePhoneNumber =     db.Column(db.String(25))
  faxNumber =             db.Column(db.String(25))
  otherNumber =           db.Column(db.String(25))
  emailAddress =          db.Column(db.String(25))
  alternateEmailAddress = db.Column(db.String(25))
  comment =               db.Column(db.Text())
  dateOfBirth =           db.Column(db.String(10))
  gender =                db.Column(db.String(1))
  isActive =              db.Column(db.Boolean, nullable=False, default=True)
  courseDay =             db.Column(db.String(3), nullable=False)
  courseStartTime =       db.Column(db.String(10), nullable=False)
  courseEndTime =         db.Column(db.String(10), nullable=False)
  level =                 db.Column(db.Integer, nullable=False)
  createdDate =           db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  lastUpdate =            db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  address = db.relationship("Address", uselist=False, back_populates="student")
  musicalNotes = db.relationship('MusicalNote', secondary='studentMusicalNoteLink')
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  user = db.relationship(User)

  def __repr__(self):
      return '<Student id:%r, firstName:%r, lastName:%r>' % (self.id, self.firstName, self.lastName)



class StudentMusicalNoteLink(db.Model):
  __tablename__ =   'studentMusicalNoteLink'

  #id =              db.Column(db.Integer, primary_key = True)
  student_id =      db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
  musicalNote_id =  db.Column(db.Integer, db.ForeignKey('musicalNote.id'), primary_key=True)
  givenDate =       db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  student =         db.relationship("Student", backref=db.backref("musicalNote_assoc"))
  musicalNote =     db.relationship("MusicalNote", backref=db.backref("student_assoc"))



 
class Address(db.Model):
  __tablename__ = 'address'

  id =              db.Column(db.Integer, primary_key = True)
  addressType =     db.Column(db.String(1), nullable=False)
  streetAddress1 =  db.Column(db.String(150)) 
  streetAddress2 =  db.Column(db.String(150)) 
  city =            db.Column(db.String(50), nullable=False) 
  postalCode =      db.Column(db.String(10)) 
  province =        db.Column(db.String(50)) 
  country =         db.Column(db.String(50)) 
  pobox =           db.Column(db.String(20))
  createdDate =     db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  lastUpdate =      db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
  student = db.relationship("Student", back_populates="address")




class Payment(db.Model):
  __tablename__ = 'payment'

  id =          db.Column(db.Integer, primary_key = True)
  amount =      db.Column(db.String(8), nullable=False)
  paidMonth =   db.Column(db.String(7), nullable=False)
  paymentDate = db.Column(db.String(10))
  paymentType = db.Column(db.String(15))
  createdDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  student_id =  db.Column(db.Integer, db.ForeignKey('student.id'))
  student =     db.relationship(Student)


 

class MusicalNote(db.Model):
  __tablename__ = 'musicalNote'

  id =          db.Column(db.Integer, primary_key = True)
  name =        db.Column(db.String(50))
  compiler =    db.Column(db.String(100))
  source =      db.Column(db.String(100))
  region =      db.Column(db.String(50))
  noteType =    db.Column(db.String(50))
  level =       db.Column(db.Integer, nullable=False)
  isActive =    db.Column(db.Boolean, nullable=False, default=True)
  isPublic =    db.Column(db.Boolean, nullable=False, default=False)
  createdDate = db.Column(db.DateTime, nullable=False)
  lastUpdate =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  students = db.relationship('Student', secondary='studentMusicalNoteLink')

  def __repr__(self):
    return '<MusicalNote id:%r>' % (self.id)

    

class StudentAttendHistory(db.Model):
  __tablename__ = 'studentAttendHistory'

  id =          db.Column(db.Integer, primary_key = True)
  startDate =   db.Column(db.Date, index=True, default=datetime.utcnow)
  endDate =     db.Column(db.String(10))
  student_id =  db.Column(db.Integer, db.ForeignKey('student.id'))
  student =     db.relationship(Student)

    

