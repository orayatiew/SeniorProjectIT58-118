from flask import Flask, request, make_response, jsonify,abort
import json
import os

import config
from getDataFromDialogflow import *
from getDataFromFirebase import *
from ConnectLineAPI import *


app = Flask(__name__)
log = app.logger

def leaveRequest(req):
    userId = getUserID(req)
    leavetype = getParamQueryResult(req,'leavetype')
    ID = getDataMatchUsers(userId,'id')
    role = getDataMatchUsers(userId,'role')
    name =getDataFollowRole(str(role),str(ID),'name')
    if leavetype == 'Business':
        return 'คุณ '+name +' ต้องการลากิจวิชาอะไรคะ'
    else:
        return 'คุณ '+name +' ต้องการลาป่วยวิชาอะไรคะ'

def leavereqGetpar(req):
    
