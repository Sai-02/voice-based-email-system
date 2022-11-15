from __future__ import print_function
import json
import constant
import base64
import os.path
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from test import speakText, listen
import speech_recognition as sr
from quickStart import getLastTenUnreadMails, getMessageFromMessageID,decodeMailBody
import pyttsx3
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
while (1):
    # speakText("What do you want to do")
    # speakText(" 1. Read Email ")
    # speakText(" 2. Send  Email ")
    # r = sr.Recognizer()
    # with sr.Microphone() as source2:
    #     r.adjust_for_ambient_noise(source2, duration=0.2)
    #     audio2 = r.listen(source2)
    #     MyText = r.recognize_google(audio2, language='en-IN')
    #     print(MyText)
    # print(listen())
    resp = input()
    if (resp == "1"):
        # speakText("Okay so you want to read your emails")
        # speakText("Please specify what mails do you want to read?")
        # speakText("1 Unread mails")
        # speakText("2 Starred mails")
        # speakText("3 Full inbox")
        resp = input()
        if (resp == "2"):
            print("Unread")
            # speakText("Do you want me to read latest 10 unread mails?")
            resp = input()
            if (resp == "3"):
                # speakText("Fine so here are you latest 10 unread mails")
                # speakText("sbjhiwbasfihbw")
                service = build('gmail', 'v1', credentials=creds)
                inbox = getLastTenUnreadMails(service)
                dictionary=getMessageFromMessageID(service, inbox[0]["id"])
                print("sbsgsjhiwbasfihbw")
                # tempo = re.sub(
                #     r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", messageContent)
                # temp = re.sub('<.*?>', '', temp)

                print("sgswsbjhiwbasfihbw")
                
                mailBy = [sub['value'] for sub in dictionary['payload']['headers'] if sub['name'] == constant.REPLY_TO][0]
                Subject= [sub['value'] for sub in dictionary['payload']['headers'] if sub['name'] == constant.SUBJECT][0]
                senderDetails=[sub['value'] for sub in dictionary['payload']['headers'] if sub['name'] == constant.FROM][0]
                senderName = senderDetails.split('"')[1]
                encodedMailBody= [sub['body']['data'] for sub in dictionary['payload']['parts'] if sub['mimeType'] == constant.MIME_TYPE_TEXT_PLAIN][0]
                mailBody = decodeMailBody(encodedMailBody)
                print("chalja",mailBy,Subject, senderName, mailBody)
                # for i in range(10):
                #     speakText(str(i+1)+" Email is :")
                #     speakText("   ")
                #     messageContent = getMessageFromMessageID(
                #         service, inbox[i]["id"])
                #     # Removing Special characters and links from mail
                #     messageContent = re.sub(
                #         r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", messageContent)
                #     messageContent = re.sub('<.*?>', '', messageContent)
                #     print(messageContent)
                #     speakText(messageContent)

        elif (resp == "Starred mails"):
            print("starred")
        elif (resp == "Full inbox"):
            print("inbox")
        else:
            speakText("Can you repeat ?")
            continue

    else:
        speakText("Sorry can you repeat yourself?")
        continue


# service = build('gmail', 'v1', credentials=creds)
# inbox = getLastTenUnreadMails(service)
# for i in range(2):
#     try:
#         print(str(i+1)+" Email is :")
#         messageContent = getMessageFromMessageID(
#             service, inbox[i]["id"])
#         # Removing Special characters and links from mail
#         messageContent = re.sub(
#             r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", messageContent)
#         messageContent = re.sub('<.*?>', '', messageContent)
#         print(messageContent)
#     except:
#         print("hehe fail")