from flask import Flask, request, make_response, jsonify,abort
import json
import os
app = Flask(__name__)
log = app.logger


def getQueryRultText(req):
    cuase = req.get('queryResult').get('queryText')
    return str(cuase) 

def getUserID(req):
    userID = req.get('originalDetectIntentRequest').get('payload').get('data').get('source').get('userId')
    return str(userID)

def getAction(req):
    action = req.get('queryResult').get('action')
    return str(action)


def getParamQueryResultLeaveType(req):
    leavetype = req.get('queryResult').get('parameters').get('leavetype')
    return str(leavetype)

def getParamQueryResultRole(req):
    role = req.get('queryResult').get('parameters').get('role')
    return str(role)

def getParamQueryResultID(req):
    ID = req.get('queryResult').get('parameters').get('ID.original')
    return str(ID)

def getParamOutputcontextLeavetypeIndexOne(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    leavetype = outputContexts[1].get('parameters').get('leavetype')
    return str(leavetype)

def getParamOutputcontextIDIndexOne(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    ID = outputContexts[1].get('parameters').get('ID.original')
    return str(ID)

def getParamOutputcontextRoleIndexOne(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    role = outputContexts[1].get('parameters').get('role')
    return str(role)

def getParamOutputcontextMessageIndexOne(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    message = outputContexts[1].get('parameters').get('message')
    return str(message)

def getParamOutputcontextSubjectIndexOne(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    subjects = outputContexts[1].get('parameters').get('subjects')
    return str(subjects)

def getParamOutputcontextSubjects(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    subjects = outputContexts[0].get('parameters').get('subjects')
    return str(subjects)

def getParamOutputcontextSection(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    section = outputContexts[0].get('parameters').get('section')
    return str(section)

def getParamOutputcontextDate(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    date = outputContexts[0].get('parameters').get('date')
    return str(date).replace("T12:00:00+00:00","")

def getParamOutputcontextID(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    ID = outputContexts[0].get('parameters').get('ID.original')
    return str(ID)

def getParamOutputcontextRole(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    role = outputContexts[0].get('parameters').get('role')
    return str(role)

def getParamOutputcontextOTP(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    otp = outputContexts[0].get('parameters').get('number.original')
    return str(otp)

def getParamOutputcontextYear(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    years = outputContexts[0].get('parameters').get('years')
    return str(years)

def getParamQueryResultannounceType(req):
    announceType = req.get('queryResult').get('parameters').get('announcementType')
    return str(announceType)

def getParamOutputcontextTitle(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    title = outputContexts[0].get('parameters').get('title')
    return str(title)
	
def getParamOutputcontextContent(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    content = outputContexts[0].get('parameters').get('content')
    return str(content)

def getParamOutputcontextTime(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    time = outputContexts[0].get('parameters').get('time.original')
    return str(time)

def getParamOutputcontextScoreType(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    scoretype = outputContexts[0].get('parameters').get('scoreType')
    return str(scoretype)

def getParamOutputcontextChannel(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    channel = outputContexts[0].get('parameters').get('channel')
    return str(channel)
    
def getParamOutputcontextCode(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    code = outputContexts[0].get('parameters').get('code')
    return str(code)

def getParamOutputcontextStatus(req):
    status = req.get('queryResult').get('parameters').get('status')
    return str(status)

def getParamOutputcontextAmount(req):
    outputContexts = req.get('queryResult').get('outputContexts')
    amount = outputContexts[0].get('parameters').get('number.original')
    return str(amount)