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

def collectQuestion(req):
    def random_refNO(length = 6, char = string.ascii_uppercase):
        return ''.join(random.choice( char) for x in range(length))
    refno = random_refNO()
    sender = getUserID(req)
    question = getQueryRult(req)
    answer = getUserIdStaffAnswer()
    if answer == 'staff ignore':
        updateQuestion(sender,question,refno)
        print('collect success')
    else:
        print('answer: '+ answer)
        updateQuestion(sender,question,refno)
        print('collect success')
        status = pushQuestionToStaff(answer,question,refno)
        if status == 'success':
            state = 'wait'
            updateStateQuestion(state,refno)
    return ''

def staffAnswer(req):
    userId_staff = getUserID(req)
    ans = getQueryRult(req)
    refno = getParamOutputcontext(req,"code",0)
    print(refno)
    updateAns(refno,ans)
    question = getQuestion(str(refno))
    status = pushConfirmToStaff(ans,userId_staff,refno,question)
    if status == 'sendConfirmAlready':
        state = 'yes'
        updateStateQuestion(state,refno)
    return ''

def pushAnsToUser(req):
    refno = getParamOutputcontext(req,"code",0)
    userId = getsender(refno)
    question = getQuestion(refno)
    ans = getAns(refno)
    message_question = 'คำถาม: '+str(question)
    message_answer = 'คำตอบ: '+str(ans)
    pushMessage(userId,message_question)
    pushMessage(userId,message_answer)
    deleteQuestion(refno)
    return 'ส่งคำตอบไปยังผู้ถามเรียบร้อยแล้วค่ะ'

def changeStatus(req):
    status = getParamQueryResult(req,"status")
    userId = getUserID(req)
    staffid = getIDFromMatchUser(userId)
    nowStatus = getStatusFrommatchUser(userId)
    amount = getAmount(staffid,nowStatus)
    if status == 'online':
        if nowStatus == 'online':
            return 'สถานะของคุณคือ Online แล้วค่ะ'
        if nowStatus == 'busy':
            deleteStaffBusy(staffid)
            addStaffOnline(staffid,userId,amount)
            updateStatusStaff(userId,status)
            return 'สถานะของคุณเปลี่ยนเป็น Online เรียนร้อยเเล้วค่ะ'           
        if nowStatus == 'ignore':
            deleteStaffIgnore(staffid)
            addStaffOnline(staffid,userId,amount)
            updateStatusStaff(userId,status)
            return 'สถานะของคุณเปลี่ยนเป็น Online เรียนร้อยเเล้วค่ะ'
    if status == 'busy':
        if nowStatus == 'busy':
            return 'สถานะของคุณคือ Busy แล้วค่ะ'
        if nowStatus == 'online':
            deleteStaffOnline(staffid)
            addStaffBusy(staffid,userId,amount)
            updateStatusStaff(userId,status)
            return 'สถานะของคุณเปลี่ยนเป็น Busy เรียนร้อยเเล้วค่ะ'           
        if nowStatus == 'ignore':
            deleteStaffIgnore(staffid)
            addStaffBusy(staffid,userId,amount)
            updateStatusStaff(userId,status)
            return 'สถานะของคุณเปลี่ยนเป็น Busy เรียนร้อยเเล้วค่ะ'     
    if status == 'ignore':
        if nowStatus == 'ignore':
            return 'สถานะของคุณคือ Ignore แล้วค่ะ'
        if nowStatus == 'online':
            deleteStaffOnline(staffid)
            addStaffIgnore(staffid,userId,amount)
            updateStatusStaff(userId,status)
            return 'สถานะของคุณเปลี่ยนเป็น Ignore เรียนร้อยเเล้วค่ะ'           
        if nowStatus == 'busy':
            deleteStaffBusy(staffid)
            addStaffIgnore(staffid,userId,amount)
            updateStatusStaff(userId,status)
            return 'สถานะของคุณเปลี่ยนเป็น Ignore เรียนร้อยเเล้วค่ะ'     
 
 
def callQuestions(req):
    userId = getUserID(req)
    amount = int(checkAmountQuestions())
    if amount > 0:
        pushConfirmCallQuestion(userId,amount)
    else:
        return 'ไม่มีคำถามที่ยังไม่ถูกส่งไปยังเจ้าหน้าที่'
    return ''

def callquestionAll(req):
    userId = getUserID(req)
    amount = getParamOutputcontext(req,"number",0)
    getQuestionAll(amount,userId)
    return ''

def callquestionAmount(req):
    userId = getUserID(req)
    amount = getParamOutputcontext(req,"number.original",0)    
    getQuestionAmount(amount,userId)
    return '' 