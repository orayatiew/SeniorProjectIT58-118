import json


cred = credentials.Certificate('D:\SITChat\seniorproject-38db0-firebase-adminsdk-28jq8-adaff53e71.json')
default_app = firebase_admin.initialize_app(cred,
    {
        "project_id": "seniorproject-38db0",
    })

db = firestore.client()