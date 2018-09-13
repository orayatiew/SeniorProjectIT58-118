from flask import Flask, request, make_response, jsonify,abort
import json
import os
import pyrebase
import config

firebase = pyrebase.initialize_app(config.FIREBASE_CONFIG)
db = firebase.database()

app = Flask(__name__)
log = app.logger

def getDataMatchUsers(userid,par):
    def changePar(par):
        if par == 'id':
            param = 'ID'
            return str(param)
        else:
            return str(par)
    data = db.child("MatchUsers").child(str(userId)).child(par).get()