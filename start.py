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
from quickStart import getLastTenUnreadMails, getMessageFromMessageID,decodeMailBody, isResponse1, isResponse2, isResponse3
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
    try:
        speakText("What do you want to do")
        speakText(" 1. Read Email ")
        speakText(" 2. Send  Email ")
        r = sr.Recognizer()
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            readOrSendAudio = r.listen(source2)
            readOrSend = r.recognize_google(readOrSendAudio, language='en-IN')
            if (isResponse1(readOrSend)):
                speakText("Okay so you want to read your emails")
                speakText("Please specify what mails do you want to read?")
                speakText("1 Unread mails")
                speakText("2 Starred mails")
                speakText("3 Full inbox")
                readMailTypeAudio = r.listen(source2)
                readMailType = r.recognize_google(readMailTypeAudio, language='en-IN')
                if (isResponse1(readMailType)):
                    speakText("Reading out latest unread mails: ")
                    service = build('gmail', 'v1', credentials=creds)
                    inbox = getLastTenUnreadMails(service)
                    for i in range(2):
                        dictionary=getMessageFromMessageID(service, inbox[i]["id"])
                        speakText(dictionary['snippet'])

                    # tempo = re.sub(
                    #     r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", messageContent)
                    # temp = re.sub('<.*?>', '', temp)
                    # print("sgswsbjhiwbasfihbw")
                    # mailBy = [sub['value'] for sub in dictionary['payload']['headers'] if sub['name'] == constant.REPLY_TO][0]
                    # Subject= [sub['value'] for sub in dictionary['payload']['headers'] if sub['name'] == constant.SUBJECT][0]
                    # senderDetails=[sub['value'] for sub in dictionary['payload']['headers'] if sub['name'] == constant.FROM][0]
                    # senderName = senderDetails.split('"')[1]
                    # encodedMailBody= [sub['body']['data'] for sub in dictionary['payload']['parts'] if sub['mimeType'] == constant.MIME_TYPE_TEXT_PLAIN][0]
                    # mailBody = decodeMailBody(encodedMailBody)
                    # print("chalja",mailBy,Subject, senderName, mailBody)

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

                elif (isResponse2(readMailType)):
                    print("starred")
                elif (isResponse3(readMailType)):
                    print("full inbox")
                else:
                    speakText("Can you repeat ?")
                    continue

            elif(isResponse2(readOrSend)):
                print("writing mail")
            else:
                speakText("Sorry can you repeat yourself?")
                continue

    except:
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