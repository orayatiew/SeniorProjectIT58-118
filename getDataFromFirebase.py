from flask import Flask, request, make_response, jsonify,abort
import json
import os
import pyrebase
import random
from random import randint
import string 
import sys	
import config
from collections import OrderedDict
import secrets
from ConnectLineAPI import *
from getDataFromDialogflow import *
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

def getAllStaff():
    staffs = db.child("Staffs").get()
    item1 = dict(staffs.val())
    item2 = list(item1.keys())
    return item2
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

def getStatusFrommatchUser(userId):
    status =  db.child("MatchUsers").child(str(userId)).child("status").get()
    return status.val()
         #----------------Update Method----------------#
def updateNewMatchUser(userId,role,ID):
     if role == 'Staffs':
         matchUserdata = {
                   "MatchUsers/"+str(userId): {
                         "role": role,
					     "ID":ID,
                         "status": 'online'
                }}
         db.update(matchUserdata) 
     else:
         matchUserdata = {
                   "MatchUsers/"+str(userId): {
                         "role": role,
					     "ID":ID
                }}
         db.update(matchUserdata) 
     return 'update success'

def updateStatusStaff(userId,status):
    data = {"status": str(status)}
    db.child("MatchUsers").child(str(userId)).update(data)
    print('Update success')
    return 'Update success'    

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
#----------------------------status_staff---------------------------#
def updateStatusDefault(userId,staffid):
    data = {
               "status_Staff/online/"+str(staffid): {
                     "amount": 0,
					 "userId":str(userId)
            }}
    db.update(data) 
    print('updateStatusDefault success')
    return 'updateStatusDefault success'

def getAmount(staffid,status):
    amonut = db.child("status_Staff").child(str(status)).child(str(staffid)).child("amount").get()
    return amonut.val()


def deleteStaffOnline(staffid):
    db.child("status_Staff").child("online").child(str(staffid)).remove()
    print('Delete success')
    return 'Delete success' 

def deleteStaffBusy(staffid):
    db.child("status_Staff").child("busy").child(str(staffid)).remove()
    print('Delete success')
    return 'Delete success' 

def deleteStaffIgnore(staffid):
    db.child("status_Staff").child("ignore").child(str(staffid)).remove()
    print('Delete success')
    return 'Delete success'

def addStaffOnline(staffid,userId,amount):
    data = {
               "status_Staff/online/"+str(staffid): {
                     "amount": amount,
					 "userId":str(userId)
            }}
    db.update(data) 
    print('addStaffOnline success')
    return 'addStaffOnline success'

def addStaffBusy(staffid,userId,amount):
    data = {
               "status_Staff/busy/"+str(staffid): {
                     "amount": amount,
					 "userId":str(userId)
            }}
    db.update(data) 
    print('addStaffBusy success')
    return 'addStaffBusy success'

def addStaffIgnore(staffid,userId,amount):
    data = {
               "status_Staff/ignore/"+str(staffid): {
                     "amount": amount,
					 "userId":str(userId)
            }}
    db.update(data) 
    print('addStaffIgnore success')
    return 'addStaffIgnore success'

def getUserIdStaffAnswer():
    anwser = db.child("status_Staff").child("online").get()
    item1 = dict(anwser.val())
    item2 = list(item1.keys())
    length = len(item2)
    print(item2)
    userIds = []
    userId = ''
    amount = ''
    if length == 1:
        del item2[0]
        anwser = db.child("status_Staff").child("busy").get()
        item1 = dict(anwser.val())
        item2 = list(item1.keys()) 
        length = len(item2)
        if length == 1:
            return 'staff ignore'
        else:
            for index in range(len(item2)):
                amount = int((db.child("status_Staff").child("busy").child(item2[index]).child("amount").get()).val())
                if amount < 2:
                    userIds.append((db.child("status_Staff").child("busy").child(item2[index]).child("userId").get()).val())
                    print(userIds)
                    userId = random.choice(userIds)
    else:
        del item2[0]
        for index in range(len(item2)):
            amount = int((db.child("status_Staff").child("online").child(item2[index]).child("amount").get()).val())
            if amount < 2:
                userIds.append((db.child("status_Staff").child("online").child(item2[index]).child("userId").get()).val())
                print(userIds)
                userId = random.choice(userIds)
    return userId
#----------------------------Question---------------------------#
def updateQuestion(sender,question,refno):
    print(refno)
    data = {
               "Questions/"+str(refno): {
                     "sender": sender,
					 "question":question,
                     "state":'no'
            }}
    db.update(data) 
    return 'update success' 

def updateStateQuestion(state,refno):
    data = {"state":str(state)}
    db.child("Questions").child(str(refno)).update(data)
    return 'Update success'

def updateAns(refno,ans):
    data = {"ans": ans}
    db.child("Questions").child(str(refno)).update(data)
    print('Update success')
    return 'Update success'

def getQuestion(refno):
    question = db.child("Questions").child(str(refno)).child("question").get()
    return question.val()

def getsender(refno):
    sender = db.child("Questions").child(str(refno)).child("sender").get()
    return sender.val()

def getAns(refno):
    answer = db.child("Questions").child(str(refno)).child("ans").get()
    return answer.val()

def deleteQuestion(refno):
    db.child("Questions").child(str(refno)).remove()
    print('Delete success')
    return 'Delete success'    

def checkAmountQuestions():
    questions = db.child("Questions").get()
    item1 = dict(questions.val())
    item2 = list(item1.keys())
    length = len(item2)
    del item2[length-1]
    print(item2)
    amount = 0
    for index in range(len(item2)):
        state = (db.child("Questions").child(item2[index]).child("state").get()).val()
        if state == 'no':
            amount += 1
    print(amount)
    return amount

def getQuestionAll(amount,userId):
    questions = db.child("Questions").get()
    item1 = dict(questions.val())
    item2 = list(item1.keys())
    length = len(item2)
    del item2[length-1]
    print(item2)
    amount = 0
    for index in range(len(item2)):
        question = (db.child("Questions").child(item2[index]).child("question").get()).val()
        state = (db.child("Questions").child(item2[index]).child("state").get()).val()
        if state == 'no':
            pushQuestionToStaff(userId,question,item2[index])
            state = 'wait'
            updateStateQuestion(state,item2[index])
    print(amount)
    return ''

def getQuestionAmount(amount,userId):
    print(amount)
    questions = db.child("Questions").get()
    item1 = dict(questions.val())
    item2 = list(item1.keys())
    print('before ' + str(item2))
    length = len(item2)
    del item2[length-1]
    print('after'+ str(item2))
    arrRef = []
    for index in range(len(item2)):
        question = (db.child("Questions").child(item2[index]).child("question").get()).val()
        state = (db.child("Questions").child(item2[index]).child("state").get()).val()
        if state == 'no':
            arrRef.append((item2[index]))
    print('ref of state NO:'+str(arrRef))

    print(len(arrRef))
    number = int(amount)
    for index in range(number):
        print(arrRef[index])
        pushQuestionToStaff(userId,question,arrRef[index])
        state = 'wait'
        updateStateQuestion(state,item2[index])
    return ''

