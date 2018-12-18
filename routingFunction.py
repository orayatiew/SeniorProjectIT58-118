from flask import Flask, request, make_response, jsonify,abort
import json
import os
import linebot
import config
from getAdditionalInfo import *
from getApplicationData import *
from ConnectExternalAPI import *
from authentication import *
from announcementLF import *
from LeaveRequest import *
from staffAnswer import *
from announcementStaff import *
from downloadTrainingFile import *
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,ConfirmTemplate,MessageAction,
    QuickReply,QuickReplyButton,MessageEvent,DatetimePickerAction,PostbackAction,PostbackEvent
)

app = Flask(__name__)
log = app.logger
line_bot_api = config.LINEBOTAPI_ACCESSTOKEN
handler = config.LINEBOTAPI_SECRETTOKEN

@app.route("/", methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    try:
        action = getAction(req)

    except AttributeError:
        return 'json error'

    # Action Switcher
    if action == 'leavereq':
        res = leaveRequest(req)
    if action == 'auth.request':
        res = auth_role(req)
    if action == 'auth.confirm':
        res = authentications(req)
    if action == 'input.otp':
        res = checkOTP(req)
    if action =='event.announcementLF':
        res = request_announcementLF(req)
    if action =='cancelclass':
        res = pushMsg_cancelclass(req)
    if action == 'compensatory':
        res = pushMsg_compensatory(req)
    if action == 'score':
        res = pushMsg_score(req)
    if action == 'quiz':
        res = pushMsg_quiz(req)
    if action =='missedClass':
        res = comfirm_MissedClass(req)
    if action =='pushMissClass':
        res = pushMsg_MissClass(req)
    if action == 'confirmNews':
        res = comfirm_News(req) 
    if action == 'pushNews':
        res = pushMsg_News(req)
    if action == 'pushReqToLf':
        res = pushReqToLf(req)
    if action == 'approve':
        res = approveReq(req)
    if action == 'reject':
        res = rejectReq(req)
    if action == 'collectQuestion':
        res = collectQuestion(req)
    if action == 'staffAnswer':
        res = staffAnswer(req)
    if action == 'pushAnsToUser':
        res = pushAnsToUser(req)
    if action == 'changeStatus':
        res = changeStatus(req)
    if action == 'callquestion':
        res = callQuestions(req)
    if action == 'callquestionAll':
        res = callquestionAll(req)
    if action == 'callquestionAmount':
        res = callquestionAmount(req)
    if action == 'forwardTootherStaff':
        res = forwardToOtherStaff(req)
    if action == 'ForwardToStaff':
       res = ForwardToStaff(req)
    if action == 'staffCanceledClass':
       res = staffCanceledClass(req)
    if action == 'staffExamschedule':
       res = staffExamschedule(req)
    if action == 'downloadfile':
       res = downloadTrainingFile(req)


    else: 
        log.error('Unexpected action.') 



	
    print('Action: ' + action) 
    print('Response: ' + res)
    return make_response(jsonify({'fulfillmentText': res}))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT','5000')))
