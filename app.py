from flask import Flask, request, make_response, jsonify,abort
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
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)




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


line_bot_api = LineBotApi('3Qg6VvA4B3r0t1QIp2eK+8ofPyhv0s+SieA4KV5YXyk4R2BDXyXhmmTgyV0jzN5JjxeJTBnMh7/FTJmHDNkaFmQ7bUhPIzvcWloXgk+hn301hRgT6uABPXXVumtkvlfLhO97NJ90ftB6/Vs5P+Bd2AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('22026c4321303e7bc5a36ae01728b77e')



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
            
            userId = req.get('originalDetectIntentRequest').get('payload').get('data').get('source').get('userId')
            userId_data = {str(userId) : str(userId)}

            matchUserdata = {
               "MatchUsers/"+str(userId): {
                     "role": role,
					 "ID":ID
            }}
            db.update(matchUserdata)
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
    role = outputContexts[1].get('parameters').get('role')

    userId = req.get('originalDetectIntentRequest').get('payload').get('data').get('source').get('userId')
    ID = db.child("MatchUsers").child(str(userId)).child("ID").get()
    std_ID = str(ID.val())
   
    

    otpPar =outputContexts[0].get('parameters').get('number.original')
    otpDB =db.child(role).child(std_ID).child("otpNO").get()
	
    otp = str(otpPar)
    checkNo = str(otpDB.val())

    if checkNo == otp:
        print('same')
        print(role)
        print(std_ID)
        

        userId_data = {"userId" : str(userId)}
        db.child(role).child(std_ID).update(userId_data)

        print('userId : '+ str(userId) )
        outputMs = 'การยืนยันตัวตนของคุณเสร็จเรียบร้อยแล้วค่ะ'
        data = {"status_auth" : "yes"}
        db.child(role).child(std_ID).update(data)

        updateRichMenu(str(userId),req)
    else:
        print('not same')
        print("OTP usr: "+otp)
        print("OTP db: "+checkNo)
        print(role)
        print(std_ID)
        outputMs = 'รหัส OTP ของท่านไม่ถูกต้อง กรุณาระบุใหม่อีกครั้ง'
    return    str(outputMs)

def updateRichMenu (userId,req):
    print('updateRichMenu')
    print(userId)
    rich_menu_id = 'richmenu-522899ebf0a6d1fd004f83bbc51cfbba'
    #line_bot_api.link_rich_menu_to_user(userId, rich_menu_id)

    ine_bot_api.unlink_rich_menu_from_user(user_id)
    return 'menu changed'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT','5000')))