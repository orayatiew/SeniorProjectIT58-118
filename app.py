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
	
    else:
        log.error('Unexpected action.')

    print('Action: ' + action)
    print('Response: ' + res)

    return make_response(jsonify({'fulfillmentText': res}))

def authentication_student(req):
	parameters = req.get('queryResult').get('parameters')
	studentId =parameters.get('studentId')
	email = db.child("Students").child(studentId).child("email").get()

	#sender = 'seniorproject.5818@gmail.com'
	#receivers = ['thehunny.oraya@gmail.com']
	#message = "OTP"
	#try:
	#	smtpObj = smtplib.SMTP('smtp.gmail.com', 465)
	#	smtpObj.sendmail(sender, receivers, message)         
	#	print ("Successfully sent email")
	#except SMTPException:
	#	print ("Error: unable to send email")

	return str(email.val())



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT','5000')))