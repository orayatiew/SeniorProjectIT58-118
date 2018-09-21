from flask import Flask, request, make_response, jsonify,abort
import json
import os
import pyrebase
import config
from collections import OrderedDict
#--------------------connect firebase----------------------#
firebase = pyrebase.initialize_app(config.FIREBASE_CONFIG)
db = firebase.database()
#----------------------------------------------------------#

app = Flask(__name__)
log = app.logger

#---------------------LF/Student/Staff----------------------#
          #--------------GET Method-----------------#
def getName(role,ID):
    name = db.child(str(role)).child(str(ID)).child("name").get()
    return name.val()

def getLname(role,ID):
    lname = db.child(str(role)).child(str(ID)).child("lname").get()
    return lname.val()

def getEmail(role,ID):
    email = db.child(str(role)).child(str(ID)).child("email").get()
    return email.val()

def getotpNo(role,ID):
    otpNo = db.child(str(role)).child(str(ID)).child("otpNO").get()
    return otpNo.val()

def getStatusAuth(role,ID):
    status = db.child(str(role)).child(str(ID)).child("status_auth").get()
    return status.val()

def getUserId(role,ID):
    userId = db.child(str(role)).child(str(ID)).child("userId").get()
    return userId.val()

def getSection(role,ID):
    section = db.child(str(role)).child(str(ID)).child("section").get()
    return section.val()

def getYear(role,ID):
    year = db.child(str(role)).child(str(ID)).child("year").get()
    return year.val()

def getSubjects(role,ID):
    subjects = db.child(str(role)).child(str(ID)).child("subjects").get()
    return subjects.val()

          #---------------Update Method------------------#
def updateOtpNo(role,ID,otp):
    data = {"otpNO": str(otp)}
    db.child(str(role)).child(str(ID)).update(data)
    print('Update success')
    return 'Update success'

def updateUserId(role,ID,userId):
    data = {"userId": str(userId)}
    db.child(str(role)).child(str(ID)).update(data)
    print('Update success')
    return 'Update success'

def updateStatusAuth(role,ID):
    data = {"status_auth": 'yes'}
    db.child(str(role)).child(str(ID)).update(data)
    print('Update success')
    return 'Update success'

        #----------------Delete Method---------------#
def deleteOtpNo(role,ID):
    db.child(str(role)).child(str(ID)).child("otpNO").remove()
    print('Delete success')
    return 'Delete success'

#--------------------------Course---------------------------#
         #---------------GET Method---------------#
def getnameSubject(sub):
    subjectName = db.child("Course").child(str(sub)).child("name").get()
    return subjectName.val()

def getLFId(sub):
    LFId = db.child("Course").child(str(sub)).child("lf_id").get()
    return LFId.val()

def getstudentSecA(sub):
    studentSecA = db.child("Course").child(str(sub)).child("sectionA").get()
    item1 = dict(studentSecA.val())
    item2 = list(item1.keys())
    userIds = []
    for data in item2:
        userIds.append((db.child("Course").child(str(sub)).child("sectionA").child(data).child("userId").get()).val())
    return userIds

def getstudentSecB(sub):
    studentSecB = db.child("Course").child(str(sub)).child("sectionB").get()
    print(studentSecB.val())
    item1 = dict(studentSecB.val())
    item2 = list(item1.keys())
    userIds = []
    for data in item2:
        userIds.append((db.child("Course").child(str(sub)).child("sectionB").child(data).child("userId").get()).val())
    return userIds
        
        #----------------Push Method------------------#
def pushUserIdIntoSubject(subject,section,userId):
    if section == 'A':
        data = {"userId": str(userId)}
        db.child("Course").child(str(subject)).child("sectionA").push(data)
        print('Push success')
    else:
        data = {"userId": str(userId)}
        db.child("Course").child(str(subject)).child("sectionB").push(data)
        print('Push success')
    return 'Push success'

#--------------------------MatchUsers------------------------#
         #----------------Get Method-------------------#
def getIDFromMatchUser(userId):
    ID = db.child("MatchUsers").child(str(userId)).child("ID").get()
    return ID.val()

def getRoleFromMatchUser(userId):
    role = db.child("MatchUsers").child(str(userId)).child("role").get()
    return role.val()
         #----------------Update Method----------------#
def updateNewMatchUser(userId,role,ID):
     matchUserdata = {
               "MatchUsers/"+str(userId): {
                     "role": role,
					 "ID":ID
            }}
     db.update(matchUserdata) 
     return 'update success' 

#----------------------------Years---------------------------#
             #------------Push Method---------------#
def pushUserIdIntoYear(year,userId):
    data = {"userId": str(userId)}
    db.child("Years").child(str(year)).push(data)
    print('Push success')
    return 'Push success'

	         #------------Get Method---------------#
def getUserIdFreshy():
    userIdFreshy = db.child("Years").child("Freshy").child("userId").get()
    return userIdFreshy.val()

def getUserIdSophomore():
    userIdFreshy = db.child("Years").child("Sophomore").child("userId").get()
    return userIdFreshy.val()

def getUserIdJunior():
    userIdFreshy = db.child("Years").child("Junior").child("userId").get()
    return userIdFreshy.val()

def getUserIdSenior():
    userIdFreshy = db.child("Years").child("Senior").child("userId").get()
    return userIdFreshy.val()
