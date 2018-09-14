from flask import Flask, request, make_response, jsonify,abort
import json
import os
from smtplib import SMTPException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import random
from random import randint
import string 
import sys	
from getDataFromDialogflow import *
from getDataFromFirebase import *
from ConnectLineAPI import *
import config

app = Flask(__name__)
log = app.logger

def auth_role(req):
    role = getParamQueryResult(req,'role')
    print(role)
    if role == 'Students':
        return 'ขอรหัสนักศึกษาของคุณด้วยค่ะ'
    if role == 'Staffs':
        return 'ขอรหัสเจ้าหน้าที่ของคุณด้วยค่ะ'
    else:
        return 'ขอรหัสผู้ช่วยสอนของคุณด้วยค่ะ'

def authentications(req):
    ID = getParamOutputcontext(req,'id',1)  #studentID StaffID LFID --> id
    role = getParamOutputcontext(req,'role',1)
    status_auth = getDataFollowRole(role,ID,'status')
    print(role)
    print(ID)
    print(status_auth)
    if status_auth == 'no':
        email = getDataFollowRole(role,ID,'email')
        otp_no = random.randint(100000,999999)
        ref_no = random_refNO()
        print(email)
        statusSendMail = sendEmailAuth(email,otp_no,ref_no)

        if statusSendMail == 'Success':
            data = {"otpNO" : otp_no}
            updateFollowRole(role,ID,data)
            print('OTP : '+ str(otp_no))
            
            userId = getUserID(req)
            #userId_data = {str(userId) : str(userId)}
            updateNewMatchUser(userId,role,ID)
            msg = 'ระบบทำการส่งรหัส OTP ไปยัง \n E-mail: ' + str(email) +'\n โดยมี ref No. ' + ref_no + '\n กรุณาระบุรหัส OTP ที่ได้รับด้วยค่ะ'
        else:
            msg = 'ส่งไม่สำเร็จ' + statusSendMail
    else:
	    msg = 'คุณได้ทำการยืนยันตัวตนไปแล้วค่ะ'
    return msg


def random_refNO(length = 6, char = string.ascii_uppercase):
    return ''.join(random.choice( char) for x in range(length))


def sendEmailAuth (email,otpno,refno):
	to = email
	gmail_user = config.EMAIL_SENDER
	gmail_pwd = config.PW_SENDER
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)
	header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Authemtication with SIT Chatbot\n'
	

	msg = header + '\n OTP NO : ' + str(otpno) +'\n ref NO. : ' + refno
	message = msg.encode('ascii', 'ignore').decode('ascii')
	smtpserver.sendmail(gmail_user, to, message)
	print('Done')
	status = 'Success' 
	smtpserver.close()
	
	return status 

def checkOTP(req):
    role = getParamOutputcontext(req,'role',0)
    userId = getUserID(req)
    ID = getDataMatchUsers(str(userId),'id')
    otpDi = getParamOutputcontext(req,'otp',0)
    otpDB = getDataFollowRole(role,ID,'otp')


    if otpDB == otpDi:
        print('same')
        print(role)
        print(ID)
        data = {"userId" : str(userId)}
        updateFollowRole(role,ID,data)
        print('userId : '+ str(userId) )
        outputMs = 'การยืนยันตัวตนของคุณเสร็จเรียบร้อยแล้วค่ะ' 
        updateRichMenu(str(userId),role) #อย่าลืมแก้เมนูคนทั่วไปเอา ยืนยันตัวตนมาใส่
    else:
        print('not same')
        print("OTP usr: "+otpDi)
        print("OTP db: "+otpDB)
        print(role)
        print(ID)
        outputMs = 'รหัส OTP ของท่านไม่ถูกต้อง กรุณาระบุใหม่อีกครั้ง'
    return    str(outputMs)