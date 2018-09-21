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
        if announceType == 'cancelclass': #Done
            return 'ต้องการแจ้งงดการเรียนการสอนวิชาอะไรคะ'
        if announceType == 'compensatory': #Done
            return 'ต้องการแจ้งชดเชยการเรียนการสอนวิชาอะไรคะ'
        if announceType == 'score': #Done
            return 'ต้องการแจ้งช่องทางประกาศของคะแนนวิชาอะไรคะ'
        if announceType == 'quiz': #Done
            return 'ต้องการประกาศการสอบเก็บคะแนนวิชาอะไรคะ'
        if announceType == 'news': #Done
            message = 'ระบุหัวข้อในการแจ้งเตือน\nตัวอย่าง\n-แจ้งย้ายห้องเรียน\n-แจ้งให้นำงานมาส่งภายในคาบ'
            pushMessage(userId,message)
            return ''
        if announceType == 'Missedclass': #Done
            return 'แจ้งการขาดเรียนของนักศึกษารหัสอะไรคะ'
    else:
        return 'ผู้ช่วยสอนเท่านั้นที่สามารถใช้งานฟังก์ชันนี้ได้ค่ะ'

def comfirm_News(req):
    userId = getUserID(req)
    title = getParamOutputcontext(req,'title',0)
    subject = getParamOutputcontext(req,'subject',0)
    date = getParamOutputcontext(req,'date',0)
    date = str(date).replace("T12:00:00+00:00","")
    section = getParamOutputcontext(req,'section',0)
    content = getParamOutputcontext(req,'content',0)
    pushMsgConfirmNews(userId,subject,date,content,section,title)
    return ''

def pushMsg_News(req):
    print(pushMsg_News)
    title = getParamOutputcontext(req,'title',0)
    subject = getParamOutputcontext(req,'subject',0)
    date = getParamOutputcontext(req,'date',0)
    date = str(date).replace("T12:00:00+00:00","")
    section = getParamOutputcontext(req,'section',0)
    content = getParamOutputcontext(req,'content',0)  
    print(title,subject,date,section,content)
    message = 'หัวข้อ: '+str(title)+'\nวิชา '+str(subject)+'\nวันที่'+str(date)+'\n'+str(content)+'\nแจ้งนักศึกษา '+str(section)
    if section == 'sec A':
        stdArr= getstudentSecA(str(subject))
        pushmultiMessage(stdArr,message)
    if section == 'sec B':
        stdArr= getstudentSecB(str(subject))
        pushmultiMessage(stdArr,message)
    if section == 'All':
        stdArrA= getstudentSecA(str(subject))
        pushmultiMessage(stdArrA,message)
        stdArrB= getstudentSecB(str(subject))
        pushmultiMessage(stdArrB,message)
    return 'ส่งเเจ้งเตือนไปยังนักศึกษาเรียบร้อยเเล้วค่ะ'

def pushMsg_quiz(req):
    print("pushMsg_quiz")
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
        message = 'แจ้งเตือนนักศึกษา '+str(sec)+'\nวันที่ '+str(date)+'\nจะมีการสอบเก็บคะแนนวิชา '+str(sub)+'\nขอให้นักศึกษามาตรงเวลาด้วยค่ะ'
        if sec == 'sec A':
            stdArr= getstudentSecA(str(sub))
            pushmultiMessage(stdArr,message)
        if sec == 'sec B':
            stdArr= getstudentSecB(str(sub))
            pushmultiMessage(stdArr,message)
        if sec == 'All':
            stdArrA= getstudentSecA(str(sub))
            pushmultiMessage(stdArrA,message)
            stdArrB= getstudentSecB(str(sub))
            pushmultiMessage(stdArrB,message)
    else:
        return 'ต้องเป็นผู้ช่วยสอนประจำวิชาเท่านั้นค่ะ ถึงจะสามารถเเจ้งเตือนได้'
    
    return 'ส่งเเจ้งเตือนไปยังนักศึกษาเรียบร้อยเเล้วค่ะ'    

def comfirm_MissedClass(req):
    message = getQueryRult(req)
    userId = getUserID(req)
    ID = getParamOutputcontext(req,'id',1)
    subject = getParamOutputcontext(req,'subject',1)
    pushMsgConfirmMissedClass(userId,subject,ID,message)
    print ( ID , subject)
    return ''

def pushMsg_MissClass(req):
    userId = getUserID(req)
    ID = getParamOutputcontext(req,'id',1)
    subject = getParamOutputcontext(req,'subject',1)
    message = getParamOutputcontext(req,'message',1)
    role = 'Students'
    name = getName(role,ID)
    lname = getLname(role,ID)
    msg ='แจ้งเตือน นักศึกษา '+str(name)+' '+str(lname)+' '+'\nรหัส: '+str(ID)+' ขาดเรียน\nวิชา '+str(subject)+'\n'+str(message)
    pushMessage(userId,msg)
    return 'ส่งเเจ้งเตือนไปยังนักศึกษาเรียบร้อยเเล้วค่ะ'


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
        if sec == 'All':
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
        time = getParamOutputcontext(req,'time.original',0)
        message = 'แจ้งเตือนนักศึกษา '+str(sec)+'\nชดเชยเวลาเรียนวิชา '+str(sub) +'\nวันที่ '+str(date)+'\nเวลา '+str(time)
        if sec == 'sec A':
            stdArr= getstudentSecA(str(sub))
            pushmultiMessage(stdArr,message)
            print('if 1')
        if sec == 'sec B':
            stdArr= getstudentSecB(str(sub))
            pushmultiMessage(stdArr,message)
            print('if 2')
        if sec == 'All':
            stdArrA= getstudentSecA(str(sub))
            pushmultiMessage(stdArrA,message)
            stdArrB= getstudentSecB(str(sub))
            pushmultiMessage(stdArrB,message)
            print('if 3')
    else:
        return 'ต้องเป็นผู้ช่วยสอนประจำวิชาเท่านั้นค่ะ ถึงจะสามารถเเจ้งเตือนได้'
    
    return 'ส่งเเจ้งเตือนไปยังนักศึกษาเรียบร้อยเเล้วค่ะ'
    
def  pushMsg_score(req):
    sub = getParamOutputcontext(req,'subject',0) #request parameters name 
    userId = getUserID(req)
    ID = getIDFromMatchUser(userId)
    IDcheck = getLFId(str(sub))
    if ID == IDcheck:
        sec = getParamOutputcontext(req,'section',0)
        scoreType = getParamOutputcontext(req,'scoretype',0)
        channel = getParamOutputcontext(req,'channel',0)
        print(sec)
        message = 'แจ้งเตือนนักศึกษา '+str(sec)+'\nคะแนนสอบ'+str(scoreType)+'วิชา '+str(sub) +'ประกาศแล้วค่ะ\nสามารถดูได้ที่'+str(channel)
        if sec == 'sec A':
            stdArr= getstudentSecA(str(sub))
            pushmultiMessage(stdArr,message)
        if sec == 'sec B':
            stdArr= getstudentSecB(str(sub))
            pushmultiMessage(stdArr,message)
        if sec == 'All':
            stdArrA= getstudentSecA(str(sub))
            pushmultiMessage(stdArrA,message)
            stdArrB= getstudentSecB(str(sub))
            pushmultiMessage(stdArrB,message)
    else:
        return 'ต้องเป็นผู้ช่วยสอนประจำวิชาเท่านั้นค่ะ ถึงจะสามารถเเจ้งเตือนได้'
    
    return 'ส่งเเจ้งเตือนไปยังนักศึกษาเรียบร้อยเเล้วค่ะ'

def  announcementTopic(req):
    userId = getUserID(req)
    role = getRoleFromMatchUser(userId)
    ID = getIDFromMatchUser(userId)
    if role == 'LF':
	    pushMsgQuicReply(role,userId)
    return ' '
    
    