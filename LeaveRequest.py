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
    leavetype = getParamQueryResult(req,'leavetype')
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
    leavetype = getParamOutputcontext(req,'leavetype',1)
    subject = getParamOutputcontext(req,'subjects',0)
    section = getParamOutputcontext(req,'section',0)
    date = getParamOutputcontext(req,'date',0)
    date = str(date).replace("T12:00:00+00:00","")
    print(subject,section,date,userId)
    pushMgsReqToLF(subject,date,userId,section,leavetype)
    return 'คำขอของนักศึกษาได้ถูกส่งไปยัง LF ประจำวิชาแล้ว เมื่อLF รับทราบแล้วระบบจะส่งแจ้งเตือนมายังนักศึกษาอีกครั้งค่ะ'

def approveReq(req):
    studentId = getParamQueryResult(req,'ID')
    role = getParamQueryResult(req,'role')
    userId = getUserId(role,studentId)
    print (userId,studentId)
    message = 'คำขอของคุณได้รับการอนุมัติแล้วค่ะ'
    pushMessage(str(userId),message)
    return 'แจ้งการอนุมัติไปยังนักศึกษาเรียบร้อยแล้วค่ะ'

def rejectReq(req):
    cuase = getQueryRult(req)
    studentId = getParamOutputcontext(req,"ID",0)
    role = getParamOutputcontext(req,"role",0)
    userId = getUserId(role,studentId)
    print (userId,studentId)
    message1 = 'คำขอของคุณไม่ได้รับการอนุมัติค่ะ'
    pushMessage(str(userId),message1)
    message2 = 'เพราะ '+str(cuase)
    pushMessage(str(userId),message2)
    return 'แจ้งการอนุมัติไปยังนักศึกษาเรียบร้อยแล้วค่ะ'  
