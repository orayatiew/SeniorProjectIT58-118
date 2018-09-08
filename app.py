from flask import Flask, request, make_response, jsonify
import json
import os
import pyrebase
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

config = {
	"apiKey": "AIzaSyDxX-2fA7eF24CKtisuPYQ0_3Ye_r2suW0",
    "authDomain": "seniorproject-38db0.firebaseapp.com",
    "databaseURL": "https://seniorproject-38db0.firebaseio.com",
    "projectId": "seniorproject-38db0",
    "storageBucket": "seniorproject-38db0.appspot.com",
    "messagingSenderId": "792126926339"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

app = Flask(__name__)
log = app.logger

@app.route("/", methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

    # Action Switcher
    if action == 'auth.request':
        res = auth_role(req)
    if action == 'auth.confirm':
        res = authentications(req)
    if action == 'input.otp':
        res = checkOTP(req)
    else: 
        log.error('Unexpected action.') 

    print('Action: ' + action) 
    print('Response: ' + res)
    return make_response(jsonify({'fulfillmentText': res}))

def auth_role(req):
    parameters = req.get('queryResult').get('parameters')
    role = parameters.get('role')
	
    if role == 'Students':
        return 'ขอรหัสนักศึกษาของคุณด้วยค่ะ'
    if role == 'Staffs':
        return 'ขอรหัสเจ้าหน้าที่ของคุณด้วยค่ะ'
    else:
        return 'ขอรหัสผู้ช่วยสอนของคุณด้วยค่ะ'

def authentications(req):
    parameters = req.get('queryResult').get('parameters')
    outputContexts = req.get('queryResult').get('outputContexts')

    ID = outputContexts[1].get('parameters').get('ID.original')
    role = outputContexts[1].get('parameters').get('role')

    status_auth = db.child(role).child(ID).child("status_auth").get()
    checkStatus = str(status_auth.val())

    if checkStatus == 'no':

        email = db.child(role).child(ID).child("email").get()
        to = str(email.val())

        otp_no = random.randint(100000,999999)
        ref_no = random_refNO()
	
        statusSendMail = sendEmailAuth(to,otp_no,ref_no)

        if statusSendMail == 'Success':
            data = {"otpNO" : otp_no}
            db.child(role).child(ID).update(data)
            print('OTP : '+ str(otp_no))
            msg = 'ระบบทำการส่งรหัส OTP ไปยัง \n E-mail: ' + str(email.val()) +'\n โดยมี ref No. ' + ref_no + '\n กรุณาระบุรหัส OTP ที่ได้รับด้วยค่ะ'
        else:
            msg = 'ส่งไม่สำเร็จ' + statusSendMail
    else:
	    msg = 'คุณได้ทำการยืนยันตัวตนไปแล้วค่ะ'
    return msg


def random_refNO(length = 6, char = string.ascii_uppercase):
    return ''.join(random.choice( char) for x in range(length))


def sendEmailAuth (email,otpno,refno):
	to = email
	gmail_user = 'seniorproject.5818@gmail.com'
	gmail_pwd = 'project5818'
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
    parameters = req.get('queryResult').get('parameters')
    outputContexts = req.get('queryResult').get('outputContexts')
    
    ID = outputContexts[1].get('parameters').get('ID.original')
    role = outputContexts[1].get('parameters').get('role')

    otpPar =parameters.get('number.original')
    otpDB =db.child(role).child(ID).child("otpNO").get()
	
    otp = str(otpPar)
    checkNo = str(otpDB.val())

    if checkNo == otp:
        print('same')
        data = {"status_auth" : "yes"}
        db.child(role).child(ID).update(data)
		
        userId = req.get('originalDetectIntentRequest').get('payload').get('data').get('source').get('userId')
        userId_data = {"userId" : str(userId)}
        db.child(role).child(ID).update(userId_data)

        db.child(role).child(ID).child("otpNO").remove()
        print('userId : '+ str(userId) )
        outputMs = 'การยืนยันตัวตนของคุณเสร็จเรียบร้อยแล้วค่ะ'
    else:
        print('not same')
        outputMs = 'รหัส OTP ของท่านไม่ถูกต้อง กรุณาระบุใหม่อีกครั้ง'
    return    str(outputMs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT','5000')))