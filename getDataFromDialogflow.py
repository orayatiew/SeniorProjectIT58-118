from flask import Flask, request, make_response, jsonify,abort
import json
import os
app = Flask(__name__)
log = app.logger

def getUserID(req):
    userID = req.get('originalDetectIntentRequest').get('payload').get('data').get('source').get('userId')
    return str(userID)

