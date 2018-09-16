from flask import Flask, request, make_response, jsonify,abort
import json
import os
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,ConfirmTemplate,MessageAction,
    QuickReply,QuickReplyButton
)
import config
from getDataFromDialogflow import *
from getDataFromFirebase import *

app = Flask(__name__)
log = app.logger

line_bot_api = config.LINEBOTAPI_ACCESSTOKEN
handler = config.LINEBOTAPI_SECRETTOKEN

def pushMessage(to,message):

    line_bot_api.push_message(to, TextSendMessage(text = message))
    return 'send success'

def pushmultiMessage(to,message):
    line_bot_api.multicast(to, TextSendMessage(text = message))
    return 'send success'


def updateRichMenu(userid,role):
    if role == 'Students':
        line_bot_api.link_rich_menu_to_user(userid, config.RICHMENU_ID_STUDENT)
    else:
        line_bot_api.link_rich_menu_to_user(userid, config.RICHMENU_ID_STAFF_LF)
    return 'Menu changed'

def getMessageContent(message_id):
     message_content = line_bot_api.get_message_content(message_id)
     return str(message_content)

def pushMgsReqToLF(sub,date,userId,sec,leavetype):
    lfid = getLFId(sub)
    studentid = getIDFromMatchUser(userId)
    name = getName("Students",studentid)
    lname = getLname("Students",studentid)
    to = getUserId("LF",lfid)
    print(lfid)
    print(to)
    if leavetype == 'Business':
        line_bot_api.push_message(to, TemplateSendMessage(
        alt_text='Confirm template',
        template=ConfirmTemplate(
            text='นักศึกษา '+str(name)+' '+str(lname)+' '+str(sec)+'\nรหัส: '+str(studentid)+' ขอลากิจ\nวิชา '+str(sub)+'\nวันที่ '+str(date),
            actions=[
                MessageAction(
                    label='อนุมัติ',
                    text='อนุมัติคำขอลา ของนักศึกษารหัส:'+ str(studentid)
                ),
			    MessageAction(
                    label='ไม่อนุมัติ',
                    text='ไม่อนุมัติคำขอลา ของนักศึกษารหัส:' + str(studentid)
                )
            ]
        )
    ))
    else:
        lfid = getLFId(sub)
        studentid = getIDFromMatchUser(userId)
        name = getName("Students",studentid)
        lname = getLname("Students",studentid)
        to = getUserId("LF",lfid)
        print(lfid)
        print(to)
        if leavetype == 'Sick':
            line_bot_api.push_message(to, TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='นักศึกษา '+str(name)+' '+str(lname)+' '+str(sec)+'\nรหัส: '+str(studentid)+' ขอลาป่วย\nวิชา '+str(sub)+'\nวันที่ '+str(date),
                actions=[
                    MessageAction(
                        label='อนุมัติ',
                        text='อนุมัติคำขอลา ของนักศึกษารหัส:'+ str(studentid)
                    ),
			        MessageAction(
                        label='ไม่อนุมัติ',
                        text='ไม่อนุมัติคำขอลา ของนักศึกษารหัส:' + str(studentid)
                    )
                ]
            )
        ))
    return 'send success'

def pushMsgQuicReply(role,userId):
    if role == 'LF':
        line_bot_api.push_message(userId, TextSendMessage(text='เลือกหัวข้อที่จะประกาศค่ะ',
                               quick_reply=QuickReply(items=[
                                   QuickReplyButton(action=MessageAction(label="test", text="test")),
                                   QuickReplyButton(action=MessageAction(label="test1", text="test2"))
                               ])))
    return 'send quick reply'