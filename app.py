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
    if action == 'auth.confirm': 
        res = authentication_student(req) 
 	if action == 'input.otp': #error
  		res = checkOTP(req) 
    else: 
        log.error('Unexpected action.') 

    print('Action: ' + action) 
    print('Response: ' + res)
    return make_response(jsonify({'fulfillmentText': res}))

def authentication_student(req):
	parameters = req.get('queryResult').get('parameters')
	studentId =parameters.get('studentId')
	email = db.child("Students").child(studentId).child("email").get()
	role = 'Students'
	otp_no = random.randint(100000,999999)
	ref_no = random_refNO()
	to = str(email.val())

	statusSendMail = sendEmailAuth(to,otp_no,ref_no,studentId,role)

	if statusSendMail == 'Success':
		data = {"otpNO" : otp_no}
		db.child("Students").child(studentId).update(data)
		msg = 'ระบบทำการส่งรหัส OTP ไปยัง \n E-mail: ' + str(email.val()) +'\n โดยมี ref No. ' + ref_no + '\n กรุณาระบุรหัส OTP ที่ได้รับด้วยค่ะ'
	else:
		msg = 'ส่งไม่สำเร็จ' + statusSendMail

	return msg

def checkOTP(req):
	parameters = req.get('queryResult').get('parameters')
	studentId = parameters.get('id')
	otpPar =parameters.get('number')
	otpDB =db.child("Students").child(studentId).child("otp").get()
	
	otp = str(otpPar)
	checkNo = str(otpDB.val())

	if checkNo == otp:
		print('same')
		return 'otp match'

def random_refNO(length = 6, char = string.ascii_uppercase):
    return ''.join(random.choice( char) for x in range(length))

def sendEmailAuth (email,otpno,refno,id_user,role):
	to = email
	gmail_user = 'seniorproject.5818@gmail.com'
	gmail_pwd = 'project5818'
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)
	header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Authemtication with SIT Chatbot\n'
	
	nameVar = db.child(role).child(id_user).child("name").get()
	lnameVar = db.child(role).child(id_user).child("lname").get()

	name = str(nameVar.val())
	lname = str(lnameVar.val())

	msg = header + '\n OTP NO : ' + str(otpno) +'\n ref NO. : ' + refno
	message = msg.encode('ascii', 'ignore').decode('ascii')
	smtpserver.sendmail(gmail_user, to, message)
	print('Done')
	status = 'Success' 
	smtpserver.close()
	
	return status 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT','5000')))