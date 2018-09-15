from flask import Flask, request, make_response, jsonify,abort
import json
import os

import config
from getDataFromDialogflow import *
from getDataFromFirebase import *
from ConnectLineAPI import *
from collections import OrderedDict

app = Flask(__name__)
log = app.logger

def request_announcementLF(req):
    userId = getUserID(req) #def from getDataFromDialogflow
    role = getRoleFromMatchUser(userId) # request argument userid and parameters that you want to get

    if str(role) == 'LF':
        announceType = getParamQueryResult(req,'type')
        print(announceType)
        if announceType == 'cancelclass':
            return 'ต้องการแจ้งงดการเรียนการสอนวิชาอะไรคะ'
        if announceType == 'compensatory':
            return 'ต้องการแจ้งชดเชยการเรียนการสอนวิชาอะไรคะ'
        if announceType == 'score':
            return 'ต้องการแจ้งคะแนนวิชาอะไรคะ'
        else:
            return 'ต้องการประกาศหัวข้ออะไรคะ'
    else:
        return 'ผู้ช่วยสอนเท่านั้นที่สามารถใช้งานฟังก์ชันนี้ได้ค่ะ'

def pushMsg_cancelclass(req):
    sub = getParamOutputcontext(req,'subject',0) #request parameters name 
    userId = getUserID(req)
    ID = getIDFromMatchUser(userId)
    IDcheck = getLFId(str(sub))
    print(sub,ID,IDcheck)
    if ID == IDcheck:
        sec = getParamOutputcontext(req,'section',0)
        date = getParamOutputcontext(req,'date',0)
        date = str(date).replace("T12:00:00+00:00","")
        print(sec)
        message = 'แจ้งเตือนนักศึกษา '+str(sec)+'\nงดการเรียนการสอนวิชา '+str(sub) +'\nวันที่ '+str(date)
        if sec == 'sec A':
            stdArr= getstudentSecA(str(sub))
            pushmultiMessage(stdArr,message)
        if sec == 'sec B':
            stdArr= getstudentSecB(str(sub))
            pushmultiMessage(stdArr,message)
        else:
            stdArrA= getstudentSecA(str(sub))
            pushmultiMessage(stdArrA,message)
            stdArrB= getstudentSecB(str(sub))
            pushmultiMessage(stdArrB,message)
    else:
        return 'ต้องเป็นผู้ช่วยสอนประจำวิชาเท่านั้นค่ะ ถึงจะสามารถเเจ้งเตือนได้'
    
    return 'ส่งเเจ้งเตือนไปยังนักศึกษาเรียบร้อยเเล้วค่ะ'

def  pushMsg_compensatory(req):
    sub = getParamOutputcontext(req,'subject',0) #request parameters name 
    userId = getUserID(req)
    ID = getIDFromMatchUser(userId)
    IDcheck = getLFId(str(sub))
    if ID == IDcheck:
        sec = getParamOutputcontext(req,'section',0)
        date = getParamOutputcontext(req,'date',0)
        date = str(date).replace("T12:00:00+00:00","")
        stdArr= getDataCourse(str(sub),'student')
        del stdArr[0]
        print(stdArr)
        message = 'แจ้งเตือนนักศึกษา '+str(sec)+'\nชดเชยเวลาเรียนวิชา '+str(sub) +'\nวันที่ '+str(date)
        pushmultiMessage(stdArr,message)
    else:
        return 'ต้องเป็นผู้ช่วยสอนประจำวิชาเท่านั้นค่ะ ถึงจะสามารถเเจ้งเตือนได้'
    
    return 'ส่งเเจ้งเตือนไปยังนักศึกษาเรียบร้อยเเล้วค่ะ'
    
def  pushMsg_score(req):
    sub = getParamOutputcontext(req,'subject',0) #request parameters name 
    userId = getUserID(req)
    ID = getDataMatchUsers(userId,'id')
    IDcheck = getDataCourse(str(sub),'lfid')
    if ID == IDcheck:
        sec = getParamOutputcontext(req,'section',0)
        scoreType = getParamOutputcontext(req,'scoretype',0)
        channel = getParamOutputcontext(req,'channel',0)
        stdArr= getDataCourse(str(sub),'student')
        del stdArr[0]
        print(stdArr)
        message = 'แจ้งเตือนนักศึกษา '+str(sec)+'\nคะแนนสอบ'+str(scoreType)+'วิชา '+str(sub) +'ประกาศแล้วค่ะ\nสามารถดูได้ที่'+str(channel)
        pushmultiMessage(stdArr,message)
    else:
        return 'ต้องเป็นผู้ช่วยสอนประจำวิชาเท่านั้นค่ะ ถึงจะสามารถเเจ้งเตือนได้'
    
    return 'ส่งเเจ้งเตือนไปยังนักศึกษาเรียบร้อยเเล้วค่ะ'

