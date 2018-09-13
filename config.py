from linebot import (
    LineBotApi, WebhookHandler
)

FIREBASE_CONFIG ={
    "apiKey": "AIzaSyDxX-2fA7eF24CKtisuPYQ0_3Ye_r2suW0",
    "authDomain": "seniorproject-38db0.firebaseapp.com",
    "databaseURL": "https://seniorproject-38db0.firebaseio.com",
    "projectId": "seniorproject-38db0",
    "storageBucket": "seniorproject-38db0.appspot.com",
    "messagingSenderId": "792126926339"
}

LINEBOTAPI_ACCESSTOKEN = LineBotApi('3Qg6VvA4B3r0t1QIp2eK+8ofPyhv0s+SieA4KV5YXyk4R2BDXyXhmmTgyV0jzN5JjxeJTBnMh7/FTJmHDNkaFmQ7bUhPIzvcWloXgk+hn301hRgT6uABPXXVumtkvlfLhO97NJ90ftB6/Vs5P+Bd2AdB04t89/1O/w1cDnyilFU=')

LINEBOTAPI_SECRETTOKEN = WebhookHandler('22026c4321303e7bc5a36ae01728b77e')
	