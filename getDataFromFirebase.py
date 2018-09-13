from flask import Flask, request, make_response, jsonify,abort
import json
import os
import pyrebase
import config

firebase = pyrebase.initialize_app(config.FIREBASE_CONFIG)
db = firebase.database()

app = Flask(__name__)
log = app.logger

def changePar(par):
    if par == 'id':
        param = 'ID'
        return str(param)
    if par == 'lfid':
        param = 'lf_id'
        return str(param)
    if par == 'student':
        param = 'students'
        return str(param)
    if par == 'status':
        param = 'status_auth'
        return str(param)
    if par == 'otp':
        param = 'otpNO'
        return str(param)
    else:
        return str(par)

def getDataMatchUsers(userid,par):
    data = db.child("MatchUsers").child(str(userid)).child(changePar(par)).get()
    return str(data.val())

def getDataCourse(sub,par):
    data = db.child("Course").child(str(sub)).child(changePar(par)).get()
    return data.val()

def getDataFollowRole(role,ID,par):
    data = db.child(role).child(ID).child(changePar(par)).get() 
    return str(data.val())

def updateFollowRole(role,ID,data):
    db.child(role).child(ID).update(data)
    return 'update success'

def updateNewMatchUser(userId,role,ID):
     matchUserdata = {
               "MatchUsers/"+str(userId): {
                     "role": role,
					 "ID":ID
            }}
     db.update(matchUserdata)
     return 'update success'