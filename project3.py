from flask import Flask, render_template, request, redirect,jsonify, url_for, flash, abort
from flask import session as login_session
from flask import make_response


from sqlalchemy import create_engine, asc, desc, func
from sqlalchemy.sql import and_, or_
from sqlalchemy.sql.expression import true
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Student, Address, Payment, MusicalNote, StudentAttendHistory, User, StudentMusicalNoteLink

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib
import datetime
import random
import string
import httplib2
import json
import requests

app = Flask(__name__)




#Connect to Database and create database session
engine = create_engine('sqlite:///musiccourse.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Location of the client secrets.
CLIENT_SECRETS = 'client_secrets.json'

CLIENT_ID = json.loads(
    open(CLIENT_SECRETS, 'r').read())['web']['client_id']
APPLICATION_NAME = "Music Course App"

ADMIN_SECRETS = 'admin_secrets.json'
ADMIN_EMAILS = json.loads(open(ADMIN_SECRETS, 'r').read())['admin_emails']




#Show all active students
@app.route('/')
@app.route('/student/')
def showActiveStudents():
  
  users = db.session.query(User).all()
  '''
  print("len(users)====?????? ", len(users))
 
  for user in users:
    print("Name : ", user.name, " email: ", user.email, " picture: ", user.picture, " admin: ", user.isAdmin, 
      " provider: ", user.provider)
  '''
  students = []
  currentUser = None
  if 'username' in login_session:
    currentUser = getUserByEmail(login_session['email'])
    if login_session['email'] in ADMIN_EMAILS:
      students = db.session.query(Student).filter_by(isActive = True).order_by(asc(Student.firstName)).all()
    else:
      students = db.session.query(Student).filter(and_(Student.isActive == True, or_(Student.emailAddress == login_session['email'], Student.alternateEmailAddress == login_session['email']))).order_by(asc(Student.firstName)).all()
    return render_template('activeStudents.html', students = students, currentUser = currentUser)
  else:
    return redirect(url_for('showNotes'))  
  



#Show all inactive students
@app.route('/inactivestudent/')
def showInactiveStudents():
  if 'username' in login_session:
    currentUser = getUserByEmail(login_session['email'])
    if login_session['email'] in ADMIN_EMAILS:
      students = db.session.query(Student).filter_by(isActive = False).order_by(asc(Student.firstName)).all()
    else:
      students = db.session.query(Student).filter(and_(Student.isActive == False, or_(Student.emailAddress == login_session['email'], Student.alternateEmailAddress == login_session['email']))).order_by(asc(Student.firstName)).all()

    return render_template('inactiveStudents.html', students = students, currentUser = currentUser)
  else:
    return redirect(url_for('showNotes')) 




#Show all logged in users 
@app.route('/allusers/')
def showAllUsers():
  if 'username' in login_session:
    currentUser = getUserByEmail(login_session['email'])
    if login_session['email'] in ADMIN_EMAILS:
      users = db.session.query(User).order_by(asc(User.numberOfTimesLoggedIn)).all()
      return render_template('userInfo.html', users = users, currentUser = currentUser)
  return redirect(url_for('showActiveStudents')) 


#Create a new student
@app.route('/student/new/', methods=['GET','POST'])
def newStudent():
  if 'username' in login_session:
    currentUser = getUserByEmail(login_session['email'])
  else:
    return redirect(url_for('showNotes'))

  if request.method == 'POST':
      print("New Student Create button is clicked ======> ")
      # TODO add rollback
   
      newStudent = Student(title =                request.form['title'],
                          firstName =             request.form['firstName'],
                          lastName =              request.form['lastName'],          
                          middleName =            request.form['middleName'],
                          telephoneNumber =       request.form['telephoneNumber'],
                          mobilePhoneNumber =     request.form['mobilePhoneNumber'],
                          faxNumber =             request.form['faxNumber'],
                          otherNumber =           request.form['otherNumber'],
                          emailAddress =          request.form['emailAddress'],
                          alternateEmailAddress = request.form['alternateEmailAddress'],
                          comment =               request.form['comment'],
                          dateOfBirth =           request.form['dateOfBirth'],
                          gender =                request.form['gender'],
                          courseDay =             request.form['courseDay'],
                          courseStartTime =       request.form['courseStartTime'],
                          courseEndTime =         request.form['courseEndTime'],
                          level =                 request.form['level'],
                          user =                  getUserByEmail(login_session['email']),
                          createdDate =           datetime.date.today()
                          )
      db.session.add(newStudent)
      db.session.commit()

      newAddress = Address(addressType =    request.form['addressType'],
                          streetAddress1 =  request.form['streetAddress1'],
                          streetAddress2 =  request.form['streetAddress2'],
                          city =            request.form['city'],
                          postalCode =      request.form['postalCode'],
                          province =        request.form['province'],
                          country =         request.form['country'],
                          pobox =           request.form['pobox'],
                          student_id =      newStudent.id,
                          createdDate =     datetime.date.today()
                          )
      db.session.add(newAddress)
      db.session.commit()

      mewStudentAttendHistory = StudentAttendHistory(student_id = newStudent.id)

      db.session.add(mewStudentAttendHistory)
      db.session.commit()

      flash('New Student %s Successfully Created' % newStudent.firstName)
            
      return redirect(url_for('showActiveStudents'))
  else:
      return render_template('newStudent.html', currentUser = currentUser)


#Show a student information
@app.route('/student/<int:student_id>/edit/', methods = ['GET', 'POST'])
def editStudent(student_id):
    # TODO add session rollback 
    editStudent = db.session.query(Student).filter_by(id = student_id).one()
    editAddress = editStudent.address
    if 'username' in login_session:
      currentUser = getUserByEmail(login_session['email'])
    else:
      return redirect(url_for('showNotes'))

    print("I am in editStudent $$$$$$$$")

    studentAttendHistories = db.session.query(StudentAttendHistory).filter_by(student_id = student_id).all()
    if request.method == 'POST':  
      try:    
        if request.form['title'] != editStudent.title:
          editStudent.title = request.form['title']
        if request.form['firstName'] != editStudent.firstName:
          editStudent.firstName = request.form['firstName']
        if request.form['lastName'] != editStudent.lastName:
          editStudent.lastName = request.form['lastName']
        if request.form['middleName'] != editStudent.middleName:
          editStudent.middleName = request.form['middleName']
        if request.form['telephoneNumber'] != editStudent.telephoneNumber:
          editStudent.telephoneNumber = request.form['telephoneNumber']
        if request.form['mobilePhoneNumber'] != editStudent.mobilePhoneNumber:
          editStudent.mobilePhoneNumber = request.form['mobilePhoneNumber']
        if request.form['faxNumber'] != editStudent.faxNumber:
          editStudent.faxNumber = request.form['faxNumber']
        if request.form['otherNumber'] != editStudent.otherNumber:
          editStudent.otherNumber = request.form['otherNumber']
        if request.form['emailAddress'] != editStudent.emailAddress:
          editStudent.emailAddress = request.form['emailAddress']
        if request.form['alternateEmailAddress'] != editStudent.alternateEmailAddress:
          editStudent.alternateEmailAddress = request.form['alternateEmailAddress']
        if request.form['comment'] != editStudent.comment:
          editStudent.comment = request.form['comment']
        if request.form['dateOfBirth'] != editStudent.dateOfBirth:
          editStudent.dateOfBirth = request.form['dateOfBirth']
        if request.form['gender'] != editStudent.gender:
          editStudent.gender = request.form['gender']
        
        if currentUser.isAdmin:
          if request.form['courseDay'] != editStudent.courseDay:
            editStudent.courseDay = request.form['courseDay']
          if request.form['courseStartTime'] != editStudent.courseStartTime:
            editStudent.courseStartTime = request.form['courseStartTime']
          if request.form['courseEndTime'] != editStudent.courseEndTime:
            editStudent.courseEndTime = request.form['courseEndTime']
          if request.form['level'] != editStudent.level:
            editStudent.level = request.form['level']
        

        currentUser = getUserByEmail(login_session['email'])
        print("currentUser email=====> ", currentUser.email)
        if editStudent.user == None or editStudent.user.id != currentUser.id:
          editStudent.user = currentUser

        editStudent.lastUpdate = datetime.utcnow()
        db.session.add(editStudent)
        db.session.commit() 

        # Edit address information
        if request.form['addressType'] != editAddress.addressType:
          editAddress.addressType = request.form['addressType']
        if request.form['streetAddress1'] != editAddress.streetAddress1:
          editAddress.streetAddress1 = request.form['streetAddress1']
        if request.form['streetAddress2'] != editAddress.streetAddress2:
          editAddress.streetAddress2 = request.form['streetAddress2']
        if request.form['city'] != editAddress.city:
          editAddress.city = request.form['city']
        if request.form['province'] != editAddress.province:
          editAddress.province = request.form['province']
        if request.form['postalCode'] != editAddress.postalCode:
          editAddress.postalCode = request.form['postalCode']
        if request.form['country'] != editAddress.country:
          editAddress.country = request.form['country']
        if request.form['pobox'] != editAddress.pobox:
          editAddress.pobox = request.form['pobox']

        db.session.add(editAddress)
        db.session.commit()
        
        if currentUser.isAdmin:
          if editStudent.isActive == True and request.form.get('isActive') == None:
            editStudent.isActive = False
            StudentAttendHistory = db.session.query(StudentAttendHistory).filter_by( student_id = student_id, endDate = "Hello").one()
            StudentAttendHistory.endDate = datetime.date.today().strftime("%Y-%m-%d")
            db.session.add(StudentAttendHistory)
            db.session.commit() 
          if editStudent.isActive == False and bool(request.form.get('isActive')) == True:
            editStudent.isActive = True
            mewStudentAttendHistory = StudentAttendHistory(student_id = editStudent.id)
            db.session.add(mewStudentAttendHistory)
            db.session.commit()
       
        flash('Student Successfully Edited %s' % editStudent.firstName)
        return redirect(url_for('showActiveStudents'))
      except:
            abort(500)
    else:
      return render_template('editStudent.html', student = editStudent, studentAttendHistories = studentAttendHistories, currentUser = currentUser)


#Show a student information
@app.route('/student/payment/<int:student_id>/', methods = ['GET', 'POST'])
def addPayment(student_id):
    if 'username' in login_session:    
      student = db.session.query(Student).filter_by(id = student_id).one()
      payments = db.session.query(Payment).filter_by(student_id = student_id).order_by(desc(Payment.paidMonth)).all()
      currentUser = getUserByEmail(login_session['email'])

      print("I am in Payment $$$$$$$$")
      print(student.id)
      if request.method == 'POST':
        newPayment = Payment(amount =   request.form['amount'],
                            paidMonth =   request.form['paidMonth'],
                            paymentDate = request.form['paymentDate'],
                            paymentType = request.form['paymentType'],
                            student_id =  student.id
                          )
        db.session.add(newPayment)
        db.session.commit()

        flash('New Payment for %s Added ' % newPayment.paidMonth)

        return redirect(url_for('addPayment', student_id = student_id))
      else:
        return render_template('payment.html', student = student, payments = payments, currentUser = currentUser)
    else:
      return redirect(url_for('showNotes'))


@app.route('/mynotes/<int:student_id>/displayAll/<int:displayAll>')
def showMyNotes(student_id, displayAll):
  if 'username' in login_session:
    student = db.session.query(Student).filter_by(id = student_id).one()
    myMusicalNotes = db.session.query(StudentMusicalNoteLink).join(Student).filter(Student.id == student_id).all()
    currentUser = getUserByEmail(login_session['email'])

    selectedMusicalNotes = []
    for myMusicalNote in myMusicalNotes:
      selectedMusicalNotes.append(myMusicalNote.MusicalNote)

    print("len(selectedMusicalNotes)====", len(selectedMusicalNotes))
    print("len(myMusicalNotes)====", len(myMusicalNotes))
    allMusicalNotes = []
    if currentUser.isAdmin and displayAll == 1:
      allMusicalNotes = db.session.query(MusicalNote).filter().order_by(asc(MusicalNote.level)).all()
    else:
      allMusicalNotes = db.session.query(MusicalNote).filter(MusicalNote.level <= student.level).order_by(asc(MusicalNote.level)).all()

    print("len(allMusicalNotes)" , len(allMusicalNotes))
    notSelectedMusicalNotes = []
    for MusicalNote in allMusicalNotes:
      if MusicalNote not in selectedMusicalNotes:
        notSelectedMusicalNotes.append(MusicalNote)

    for notSelectedMusicalNote in notSelectedMusicalNotes:
      print("notSelectedMusicalNote Musical Note Id: %s, level: %s " % (notSelectedMusicalNote.id, notSelectedMusicalNote.level))

    print("len(notSelectedMusicalNotes)" , len(notSelectedMusicalNotes))
    
    return render_template('myNotes.html', student = student, myMusicalNotes = myMusicalNotes, notSelectedMusicalNotes = notSelectedMusicalNotes, currentUser = currentUser)
  else:
    return redirect(url_for('showNotes'))






@app.route('/addMyNotes', methods = ['POST'])
def addMyNotes():
  print("I am in addMyNotes $$$$$$$$")

  student_id = request.args.get('student_id')
  print("student_id is ========> ", student_id)
  student = db.session.query(Student).filter_by(id = student_id).one()
  ids = request.args.get('data')
  print("ids ==========> &&&&& ", ids)

  dataIds = request.data
  print("dataIds =============> ", dataIds)

  MusicalNoteIds = ids.split(",")
  for MusicalNoteId in MusicalNoteIds:
    print("each MusicalNoteId: ======> ", MusicalNoteId)
    MusicalNote = db.session.query(MusicalNote).filter_by(id = MusicalNoteId).one()
    newStudentMusicalNoteLink = StudentMusicalNoteLink(student = student, MusicalNote = MusicalNote)
    db.session.add(newStudentMusicalNoteLink)
    db.session.commit()

  flash('New Musical Note(s) is/are Added')

  return "Done"
  



#Delete one of my note
@app.route('/mynotes/<int:student_id>/<int:MusicalNote_id>/', methods = ['POST'])
def deleteMyNote(student_id, MusicalNote_id):
  print("I am in deleteMyNote $$$$$$$$")
  student = db.session.query(Student).filter_by(id = student_id).one()

  StudentMusicalNoteLink = db.session.query(StudentMusicalNoteLink).join(Student, MusicalNote).filter(Student.id == student_id, MusicalNote.id == MusicalNote_id).one()
  session.delete(StudentMusicalNoteLink)
  flash('%s Successfully Deleted' % StudentMusicalNoteLink.MusicalNote.id)
  db.session.commit()
  
  return redirect(url_for('showMyNotes', student_id = student_id, displayAll = 0))


  
#Delete one of my note
@app.route('/notes/<int:MusicalNote_id>/', methods = ['POST'])
def deleteNote(MusicalNote_id):
  print("I am in deleteNote $$$$$$$$")

  MusicalNote = db.session.query(MusicalNote).filter_by(id = MusicalNote_id).one()
  MusicalNote.isActive = False
  db.session.add(MusicalNote)
  db.session.commit()
  flash('%s Successfully Deleted' % MusicalNote.id)
  return redirect(url_for('showNotes'))




#Show all notes 
@app.route('/notes/', methods = ['GET', 'POST'])
def showNotes():
    MusicalNotes = db.session.query(MusicalNote).filter_by(isActive = True).order_by(asc(MusicalNote.noteType)).all()
    currentUser = None
    if 'username' in login_session:
      currentUser = getUserByEmail(login_session['email'])


    print("I am in showNotes $$$$$$$$")
    if request.method == 'POST':
      newMusicalNote = MusicalNote(compiler =   request.form['compiler'],
                                name =        request.form['name'],
                                source =      request.form['source'],
                                region =      request.form['region'],
                                noteType =    request.form['noteType'],
                                level =       request.form['level'],
                                createdDate = datetime.date.today()
                                )
      db.session.add(newMusicalNote)
      db.session.commit()

      flash('New Musical Note is Added')

      return redirect(url_for('showNotes'))
    else:
      return render_template('notes.html', MusicalNotes = MusicalNotes, currentUser = currentUser)


#Show all inactive notes
@app.route('/inactivenotes/')
def showInactiveNotes():
  if 'username' in login_session:
    currentUser = getUserByEmail(login_session['email'])
    MusicalNotes = db.session.query(MusicalNote).filter_by(isActive = False).order_by(asc(MusicalNote.noteType)).all()
    return render_template('inactivenotes.html', MusicalNotes = MusicalNotes, currentUser = currentUser)
  else:
    return redirect(url_for('showNotes'))


@app.route('/contactus/', methods = ['GET', 'POST'])
def contactUs():
    currentUser = None
    if 'username' in login_session:
      currentUser = getUserByEmail(login_session['email'])
    if request.method == 'POST':
      email_secrets = json.loads(open('email_secrets.json', 'r').read())['email']
      smtp_server = email_secrets['smtp_server'] 
      smtp_port = email_secrets['smtp_port'] 
      smtp_login_email = email_secrets['smtp_login_email'] 
      smtp_login_password = email_secrets['smtp_login_password'] 
      email_from = email_secrets['email_from'] 
      email_to = email_secrets['email_to']

      firstName = request.form['firstName']
      lastName = request.form['lastName']
      email = request.form['emailAddress']
      message = request.form['message']
      phone = request.form['phone']


    
      msg = MIMEMultipart()
      msg['From'] = "%s %s <%s>" % (firstName, lastName, email)
      msg['To'] = email_to
      msg['Subject'] = "Message from %s %s"  % (firstName, lastName)

      header = "Sender name: %s %s \nEmail:  %s" % (firstName, lastName, email)
      if phone:
        header = header + "\nPhone: %s" % (phone)
 
      body = header + "\n\n\n" + message
      msg.attach(MIMEText(body, 'plain'))
 
      server = smtplib.SMTP(smtp_server, smtp_port)
      server.starttls()
      server.login(smtp_login_email, smtp_login_password)
      text = msg.as_string()
      try:  
        server.sendmail(email_from, email_to, text)
        flash ('Contact form successfully submitted. Thank you, I will get back to you soon!')
      except:
        flash ('There was an error while submitting the form. Please try again later')
      server.quit()

      return redirect(url_for('contactUs'))
    else:
      return render_template('contactForm.html', currentUser = currentUser)




#Activated one of note
@app.route('/inactivenotes/<int:MusicalNote_id>/', methods = ['POST'])
def activedNote(MusicalNote_id):
  print("I am in activedNote $$$$$$$$")

  MusicalNote = db.session.query(MusicalNote).filter_by(id = MusicalNote_id).one()
  MusicalNote.isActive = True
  db.session.add(MusicalNote)
  db.session.commit()
  flash('%s Successfully Activated' % MusicalNote.id)
  return redirect(url_for('showInactiveNotes'))


# JSON APIs to view Student Information
@app.route('/student/<int:student_id>/edit/JSON')
def StudentAttendHistoryJSON(student_id):
    student = db.session.query(serialize).filter_by(id=student_id).one()
    studentAttendHistories = db.session.query(StudentAttendHistory).filter_by(
        student_id=student_id).all()
    return jsonify(StudentAttendHistories=[i.serialize for i in studentAttendHistories])


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf8'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    print("login_session['username']  ======> " , login_session['username'] )
    print("login_session['picture'] =======> ", login_session['picture'])
    print("login_session['email'] ========> ", login_session['email'])

    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user = getUserByEmail(data["email"])
    if not user:
        user = createUser(login_session)
    else:
        user.numberOfTimesLoggedIn = user.numberOfTimesLoggedIn + 1
        db.session.add(user)
        db.session.commit()
    login_session['user_id'] = user.id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("Done!")
    return output



def deleteUser(login_session):
    print("deleteUser is CALLED !!!!!!!!")
    try:
        user = db.session.query(User).filter_by(email=login_session['email']).one()
        print("USER DELETED!!!!")
        session.delete(user)
        db.session.commit()
    except:
        print("NOT DELETED!!!!")


# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'], provider = login_session['provider'])
    if login_session['email'] in ADMIN_EMAILS:
      newUser.isAdmin = True
    db.session.add(newUser)
    db.session.commit()
    return db.session.query(User).filter_by(email=login_session['email']).one()


def getUserByEmail(email):
  try:
    return db.session.query(User).filter_by(email=email).one()
  except:
      return None

'''
def getUserID(email):
    try:
        user = getUserByEmail(email)
        return user.id
    except:
        return None
'''
        
# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    print("I am in gdisconnect() $$$$$$$$$$$$$")
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    
    print("result['status'] ======> ", result['status'])

    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
        

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            # del login_session['credentials']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        #flash("You have successfully been logged out.")
        return redirect(url_for('showLogin'))         
    else:
        flash("You were not logged in")
        return redirect(url_for('showActiveStudents'))
        # TODO check the redirecting


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
      response = make_response(json.dumps('Invalid state parameter.'), 401)
      response.headers['Content-Type'] = 'application/json'
      return response
    
    #access_token = request.data
    #request.data
    #request.args.get('accessToken')
    access_token = request.args.get('accessToken')
    print("accessToken data is 1111 ============================ ***************** +++++ ", access_token)
    '''
    data = json.loads(request.form.get('data'))
    accessToken = data['accessToken']

    accessToken = request.data()
    print("accessToken data is ============================ ***************** +++++ ", str(accessToken))
    
   # request.data
    print ("Access token received ======> $$$$$$$$$$$$$$$$$$$$$$$$ ")
    print(access_token)
    
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    '''
    client_secrets = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']
    app_id = client_secrets['app_id']
    app_secret = client_secrets['app_secret']

    print("Facebook APP_ID: %s " % app_id)
    print("Facebook app_secret: %s  " % app_secret)
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)

    h = httplib2.Http()
    result = h.request(url, 'GET')[1].decode('utf8')

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.7/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.7/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1].decode('utf8')

    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.7/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    #result = h.request(url, 'GET')[1]
    # data = requests.get(result).json()
    data = json.loads(h.request(url, 'GET')[1].decode('utf8'))

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user = getUserByEmail(login_session['email'])
    if not user:
        user = createUser(login_session)
    else:
        user.numberOfTimesLoggedIn = user.numberOfTimesLoggedIn + 1
        db.session.add(user)
        db.session.commit()

    login_session['user_id'] = user.id

    # numberOfTimesLoggedIn

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output

@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return redirect(url_for('showLogin')) 
    #return "You have been logged out"



@app.route('/student/JSON')
def studentsJSON():
    students = db.session.query(Student).all()
    return jsonify(students=[r.serialize for r in students])


@app.errorhandler(404)
def not_found_error(error):
    print("I am in errorhandler(404)")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    print("I am in errorhandler(500)")
    session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)

####################

