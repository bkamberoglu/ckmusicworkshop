import os
basedir = os.path.abspath(os.path.dirname(__file__))

#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
 
from app.models import Student, Address, Payment, MusicalNote, StudentAttendHistory, User, StudentMusicalNoteLink
 
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'musiccourse.db')

from app import app, db

#engine = create_engine(SQLALCHEMY_DATABASE_URI)
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


db.drop_all()

'''
StudentMusicalNoteLink.__table__.drop()
User.__table__.drop()
MusicalNote.__table__.drop()
Address.__table__.drop()
StudentAttendHistory.__table__.drop()
Payment.__table__.drop()
Student.__table__.drop()
'''

#db.drop_all()


print ("All tables are droped!")

