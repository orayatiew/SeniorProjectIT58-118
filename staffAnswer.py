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
    updateQuestion(sender,question,refno)
    print('collect success')
    answer = getUserIdStaffAnswer()
    print('answer: '+ answer)
    pushQuestionToStaff(answer,question,refno)

    return ''

def staffAnswer(req):
    userId_staff = getUserID(req)
    ans = getQueryRult(req)
    refno = getParamOutputcontext(req,"code",0)
    updateAns(refno,ans)
    pushConfirmToStaff(ans,userId_staff,refno)
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
    return 'ส่งคำตอบไปยังผู้ถามเรียบร้อยแล้วค่ะ'


    
