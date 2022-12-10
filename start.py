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
from quickStart import getLastTenUnreadMails, getMessageFromMessageID, decodeMailBody, isResponse1, isResponse2, isResponse3
import pyttsx3
from readmail import readmail
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
        # speakText("What do you want to do")
        # speakText(" 1. Read Email ")
        # speakText(" 2. Send  Email ")
        print("What do you want to do")
        print(" 1. Read Email ")
        print(" 2. Send  Email ")

        r = sr.Recognizer()
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            # readOrSendAudio = r.listen(source2)
            # readOrSend = r.recognize_google(readOrSendAudio, language='en-IN')
            readOrSend = input()
            if (isResponse1(readOrSend)):
                print("Okay so you want to read your emails")
                print("Please specify what mails do you want to read?")
                print("1 Unread mails")
                print("2 Starred mails")
                print("3 Full inbox")
                # speakText("Okay so you want to read your emails")
                # speakText("Please specify what mails do you want to read?")
                # speakText("1 Unread mails")
                # speakText("2 Starred mails")
                # speakText("3 Full inbox")
                # readMailTypeAudio = r.listen(source2)
                # readMailType = r.recognize_google(readMailTypeAudio, language='en-IN')
                readMailType = input()
                if (isResponse1(readMailType)):
                    # speakText("Reading out latest unread mails: ")
                    print("Reading out latest unread mails: ")
                    service = build('gmail', 'v1', credentials=creds)
                    inbox = getLastTenUnreadMails(service)
                    for i in range(10):
                        dictionary = getMessageFromMessageID(
                            service, inbox[i]["id"])
                        print(dictionary['snippet'])
                        print("                                      ")
                        # print("This was your "+(i+1)+" mail")
                        print("Now next mail is        ")
                        # speakText(dictionary['snippet'])
                        # speakText("                                      ")
                        print("This was your "+str(i+1)+" mail")
                        # speakText("Now next mail is        ")

                        # mailBy = [sub['value'] for sub in dictionary['payload']
                        #           ['headers'] if sub['name'] == constant.REPLY_TO][0]
                        # Subject = [sub['value'] for sub in dictionary['payload']
                        #            ['headers'] if sub['name'] == constant.SUBJECT][0]
                        # senderDetails = [sub['value'] for sub in dictionary['payload']
                        #                  ['headers'] if sub['name'] == constant.FROM][0]
                        # senderName = senderDetails.split('"')[1]
                        # print(dictionary)
                        try:
                            mailBody = readmail(dictionary)
                            print(mailBody)
                            speakText(mailBody)
                        except Exception as e:
                            print(e)

                elif (isResponse2(readMailType)):
                    print("starred")
                elif (isResponse3(readMailType)):
                    print("full inbox")
                else:
                    speakText("Can you repeat ?")
                    continue

            elif (isResponse2(readOrSend)):
                print("writing mail")
            else:
                # speakText("Sorry can you repeat yourself?")
                print("Sorry can you repeat yourself?")
                break

    except:
        print("Something went wrong !!")
        break
