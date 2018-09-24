from flask import Flask, request, make_response, jsonify,abort
import json
import os

import config
from getDataFromDialogflow import *
from getDataFromFirebase import *
from ConnectLineAPI import *


app = Flask(__name__)
log = app.logger

def leaveRequest(req):
    userId = getUserID(req)
    leavetype = getParamQueryResultLeaveType(req)
    ID = getIDFromMatchUser(str(userId))
    role = getRoleFromMatchUser(str(userId))
    name = getName(str(role),str(ID))
    print(ID,role,name)
    if leavetype == 'Business':
        return 'คุณ '+str(name) +' ต้องการลากิจวิชาอะไรคะ'
    else:
        return 'คุณ '+str(name) +' ต้องการลาป่วยวิชาอะไรคะ'

def pushReqToLf(req):
    userId = getUserID(req)
    leavetype = getParamOutputcontextLeavetypeIndexOne(req)
    subject = getParamOutputcontextSubjects(req)
    section = getParamOutputcontextSection(req)
    date = getParamOutputcontextDate(req)
    print(subject,section,date,userId)
    pushMgsReqToLF(subject,date,userId,section,leavetype)
    return 'คำขอของนักศึกษาได้ถูกส่งไปยัง LF ประจำวิชาแล้ว เมื่อLF รับทราบแล้วระบบจะส่งแจ้งเตือนมายังนักศึกษาอีกครั้งค่ะ'

def approveReq(req):
    studentId = getParamQueryResultID(req)
    role = getParamQueryResultRole(req)
    userId = getUserId(role,studentId)
    print (userId,studentId)
    message = 'คำขอของคุณได้รับการอนุมัติแล้วค่ะ'
    pushMessage(str(userId),message)
    return 'แจ้งการอนุมัติไปยังนักศึกษาเรียบร้อยแล้วค่ะ'

def rejectReq(req):
    cuase = getQueryRult(req)
    studentId = getParamOutputcontextID(req)
    role = getParamOutputcontextRole(req)
    userId = getUserId(role,studentId)
    print (userId,studentId)
    message1 = 'คำขอของคุณไม่ได้รับการอนุมัติค่ะ'
    pushMessage(str(userId),message1)
    message2 = 'เพราะ '+str(cuase)
    pushMessage(str(userId),message2)
    return 'แจ้งการอนุมัติไปยังนักศึกษาเรียบร้อยแล้วค่ะ'  
