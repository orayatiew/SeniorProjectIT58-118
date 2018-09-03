from flask import Flask, request, make_response, jsonify
import json
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dateutil.parser import parse
from datetime import datetime

cred = credentials.Certificate('D:\SITChat\seniorproject-38db0-firebase-adminsdk-28jq8-adaff53e71.json')
default_app = firebase_admin.initialize_app(cred,
    {
        "project_id": "seniorproject-38db0",
    })

db = firestore.client()

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
    if action == 'Reservation.Reservation-yes':
        res = create_reservation(req)
	if action == 'auth.confirm':
		res = authentication_student(req)
    else:
        log.error('Unexpected action.')

    print('Action: ' + action)
    print('Response: ' + res)

    return make_response(jsonify({'fulfillmentText': res}))

def authentication_student(req):
	#parameters = req.get('queryResult').get('parameters')
	#studentId =parameters.get('studentId')
	return 'ระบุรหัสOTP ที่ได้รับจากอีเมลของคุณค่ะ'

def create_reservation(req):
    parameters = req.get('queryResult').get('parameters')
    name = parameters.get('name')
    seats = parameters.get('seats')
    time = parameters.get('time')
    date = parameters.get('date')
    # time = parse(Strtime)
    # date = parse(Strdate)

    date_ref = db.collection(u'date').document(str(date))
    date_ref.collection(u'reservations').add({
        u'name': name,
        u'seats': seats,
        u'time' : time,
        # u'time': date.replace(hour=time.hour-7, minute=time.minute)
    })
    return 'เรียบร้อยละค่า จอง ' + str(seats)+ time+  ' ดูเมนูต่อเลยมั้ยเอ่ย'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT','5000')))