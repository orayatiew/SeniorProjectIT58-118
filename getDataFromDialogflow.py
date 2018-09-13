from flask import Flask, request, make_response, jsonify,abort
import json
import os
app = Flask(__name__)
log = app.logger

def getUserID(req):
    userID = req.get('originalDetectIntentRequest').get('payload').get('data').get('source').get('userId')
    return str(userID)

def getAction(req):
    action = req.get('queryResult').get('action')
    return str(action)

def getParamOutputcontext(req,par,index):
    def changePar(par):
        if par == 'id':
            param = 'ID.original'
            return str(param)
        if par == 'subject':
            param = 'subjects'
            return str(param)
        if par == 'otp':
            param ='number.original'
            return str(param)
        else:
            return str(par)
    outputContexts = req.get('queryResult').get('outputContexts')
    parameter = outputContexts[index].get('parameters').get(changePar(par))

    
    return str(parameter)

def getParamQueryResult(req,par):
    parameter = req.get('queryResult').get('parameters').get(par)
    return str(parameter)
    