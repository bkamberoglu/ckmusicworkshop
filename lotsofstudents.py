#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#from sqlalchemy import func
from datetime import datetime


 
from app.models import Student, Address, Payment, MusicalNote, StudentAttendHistory, StudentMusicalNoteLink

from app import app, db
 
#engine = create_engine('sqlite:///musiccourse.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
#Base.metadata.bind = engine
 
#DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# db.session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()

#session = DBSession()



musicalNote1 = MusicalNote(name = "Yol Ver Daglar", compiler = "Arif Sag", source = "Anonim", region = "Erzurum", noteType = "Huseyni", level = "2", createdDate = datetime.utcnow()) 
db.session.add(musicalNote1)
db.session.commit()

musicalNote2 = MusicalNote(name = "Keklik Gibi", compiler = "Erdal Erzincan", source = "Anonim", region = "Erzincan", noteType = "Hicaz", level = "3", createdDate = datetime.utcnow()) 
db.session.add(musicalNote2)
db.session.commit()

musicalNote3 = MusicalNote(name = "Semmame", compiler = "Ibrahim Tatlises", source = "Anonim", region = "Urfa", noteType = "Rast", level = "4", createdDate = datetime.utcnow()) 
db.session.add(musicalNote3)
db.session.commit()

musicalNote4 = MusicalNote(name = "Basi Pare Pare Dumanli Daglar", compiler = "Turan Engin", source = "Anonim", region = "Erzincan", noteType = "Hicaz", level = "4", createdDate = datetime.utcnow()) 
db.session.add(musicalNote4)
db.session.commit()

musicalNote5 = MusicalNote(name = "Sarisin", compiler = "Sezen Aksu", source = "Sezen Aksu", region = "Istanbul", noteType = "Saba", level = "5", createdDate = datetime.utcnow()) 
db.session.add(musicalNote5)
db.session.commit()


musicalNote6 = MusicalNote(name = "Erenler Cemi", compiler = "Tolga Sag", source = "Anonim", region = "Erzurum", noteType = "Kurdi", level = "3", createdDate = datetime.utcnow()) 
db.session.add(musicalNote6)
db.session.commit()

musicalNote7 = MusicalNote(name = "Topal Oyun Havasi", source = "Anonim", region = "Ankara", noteType = "Huseyni", level = "5", createdDate = datetime.utcnow()) 
db.session.add(musicalNote7)
db.session.commit()


musicalNote8 = MusicalNote(name = "Misket", source = "Anonim", region = "Ankara", noteType = "Huseyni", level = "4", createdDate = datetime.utcnow()) 
db.session.add(musicalNote8)
db.session.commit()

musicalNote9 = MusicalNote(name = "Guzelim Bir Derde Dustum", source = "Serpil Sarı", region = "Sivas", noteType = "Huseyni", level = "3", createdDate = datetime.utcnow()) 
db.session.add(musicalNote9)
db.session.commit()

musicalNote10 = MusicalNote(name = "Uzun ince Bir Yoldayim", compiler = "Asik Veysel", region = "Sivas", noteType = "Kurdi", level = "4", createdDate = datetime.utcnow()) 
db.session.add(musicalNote10)
db.session.commit()

musicalNote11 = MusicalNote(name = "Gardas", source = "Arif Kurt", region = "Erzincan", noteType = "Huseyni", level = "3", createdDate = datetime.utcnow()) 
db.session.add(musicalNote11)
db.session.commit()

musicalNote12 = MusicalNote(name = "Aldım Sazı Elime", source = "Sabahat Akkiraz", region = "Sivas", noteType = "Huseyni", level = "4", createdDate = datetime.utcnow()) 
db.session.add(musicalNote12)
db.session.commit()


#
student1 = Student(title = "Mr", firstName = "Bulent", lastName = "Kamberoglu", mobilePhoneNumber = "0-538-971-5753", gender = "M", dateOfBirth = "1975-10-15",
	emailAddress = "bkamberoglu@gmail.com", alternateEmailAddress = "b_kamberoglu@yahoo.com", courseDay = "Thu", courseStartTime = "11.30 AM", courseEndTime = "01.30 PM", 
	level = "4")
db.session.add(student1)
db.session.commit()

student2 = Student(title = "Mr", firstName = "Merdan", lastName = "Sahin", mobilePhoneNumber = "778-714-1545", gender = "M", dateOfBirth = "2008-06-17",
	emailAddress = "merdansahin@gmail.com", courseDay = "Thu", courseStartTime = "09.45 AM", courseEndTime = "11.45 AM", level = "3")
db.session.add(student2)
db.session.commit()


#
address1 = Address(addressType = "M", streetAddress1 = "Ataturk Cad. No:63", city = "Ankara", student = student1)
db.session.add(address1)
db.session.commit()

address2 = Address(addressType = "P", streetAddress1 = "A. Taner Kislali Cad", city = "Ankara", student = student2)
db.session.add(address2)
db.session.commit()


#
studentAttendHistory1 = StudentAttendHistory(student = student1)
db.session.add(studentAttendHistory1)
db.session.commit()

studentAttendHistory2 = StudentAttendHistory(student = student2)
db.session.add(studentAttendHistory2)
db.session.commit()



# 
studentMusicalNoteLink1 = StudentMusicalNoteLink(student = student1, musicalNote = musicalNote1)
db.session.add(studentMusicalNoteLink1)
db.session.commit()

studentMusicalNoteLink2 = StudentMusicalNoteLink(student = student1, musicalNote = musicalNote2)
db.session.add(studentMusicalNoteLink2)
db.session.commit()

studentMusicalNoteLink3 = StudentMusicalNoteLink(student = student1, musicalNote = musicalNote3)
db.session.add(studentMusicalNoteLink3)
db.session.commit()

studentMusicalNoteLink4 = StudentMusicalNoteLink(student = student1, musicalNote = musicalNote4)
db.session.add(studentMusicalNoteLink4)
db.session.commit()

studentMusicalNoteLink5 = StudentMusicalNoteLink(student = student1, musicalNote = musicalNote5)
db.session.add(studentMusicalNoteLink5)
db.session.commit()

studentMusicalNoteLink6 = StudentMusicalNoteLink(student = student2, musicalNote = musicalNote6)
db.session.add(studentMusicalNoteLink6)
db.session.commit()






print ("Student is added!")



