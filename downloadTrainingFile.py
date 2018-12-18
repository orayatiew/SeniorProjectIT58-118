import codecs
from flask import Flask, request, make_response, jsonify,abort
import json
import os
from smtplib import SMTPException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import string 
import sys	
from getAdditionalInfo import *
from getApplicationData import *
from ConnectExternalAPI import *
import config
from email.mime.text import MIMEText

app = Flask(__name__)
log = app.logger


def downloadTrainingFile(req):
    from getDataFromDialogflow import getTimestamp
    ownerReq = getUserID(req)
    message = 'กรุณารอสักครู่...'
    pushMessage(ownerReq,message)
    ID = getIDFromMatchUser(ownerReq)
    email = getEmail("Staffs",ID)
    statusQuestion = AmountQuestions()
    time =  getTimestamp(req)
    print(str(ID),str(email),str(statusQuestion))
    if statusQuestion > 0 :
        pushMsgLogTrainingFile(req,ownerReq,ID)
        sendFileQuestion(email)
        deleteAllQuestion()

        res = 'คุณสามารถ Download File (question.txt) \n ได้ที่ emai: '+email
        pushMessage(ownerReq,res)
        return 'Success'
    else:
        res = 'ยังไม่มีคำถามที่ยังไม่ถูก trainning...'
        pushMessage(ownerReq,res)
        return ''


def sendFileQuestion(email):
    questions=getAllQuestion()
    print(len(questions))
    questions1 = questions.replace("["," ")
    questions2 = questions1.replace("]"," ")
    questions3 = questions2.replace("'"," ")
    questions4 = questions3.replace(",","\n")
    print(questions4)
    f = codecs.open("questions.txt", "w", "utf-8")
    f.write(str(questions4))
    f.close()

    subject = 'Download Trainning File'
    to = email
    gmail_user = config.EMAIL_SENDER
    gmail_pwd = config.PW_SENDER
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject

    body = 'คุณสามารถ Download ไฟล์นี้เพื่อนำไป Upload ใน Dialogflow เพื่อทำการ trainning '
    msg.attach(MIMEText(body,'plain'))
    filename = 'questions.txt'
    attachment = open(filename,'rb')
    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment;  filename='+filename)           
    msg.attach(part)
    text = msg.as_string()
    smtpserver.sendmail(gmail_user, to, text)
    print('Done')
    status = 'Success' 
    smtpserver.close()
    return ''
    

