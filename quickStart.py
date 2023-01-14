from __future__ import print_function
import base64
import os.path
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from googleapiclient.errors import HttpError
import speech_recognition as sr

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          "https://mail.google.com/",
          "https://www.googleapis.com/auth/gmail.modify",
          "https://www.googleapis.com/auth/gmail.compose",
          "https://www.googleapis.com/auth/gmail.send"]

getStarred = 'is:starred'
getUnread = 'is:unread'


def getAllMails(service):
    inbox = service.users().messages().list(userId='me').execute()
    return inbox


def getLastTenMails(service, query):
    inbox = service.users().messages().list(userId='me', q=query).execute()
    return inbox["messages"]


def isResponse1(resp):
    return resp == "one" or resp == "on" or resp == "vun" or resp == "One" or resp == "On" or resp == "Vun" or resp == "1" or resp == "man" or resp == "Man" or resp == "wall" or resp == "Read Email" or resp == "Read mail" or resp == "Read nail" or resp == "Read E mail" or resp == "read e mail" or resp == "reed mail"


def isResponse2(resp):
    return resp == "two" or resp == "tu" or resp == "too" or resp == "Two" or resp == "Tu" or resp == "Too" or resp == "2"


def isResponse3(resp):
    return resp == "three" or resp == "thri" or resp == "tree" or resp == "Three" or resp == "Thri" or resp == "Tree" or resp == "3" or resp == "free" or resp == "Free"


def isResponseRead(resp):
    for x in ["reed", "read", "re ead"]:
        if (resp and resp.lower().find(x) != -1):
            return 1
    return 0


def isResponseSend(resp):
    for x in ["send", "sent", "sed", "sad", "sand"]:
        if (resp and resp.lower().find(x) != -1):
            return 1
    return 0


def isResponseUnread(resp):
    for x in ["unread", "un read", "un red", "umread", "100", "hundred"]:
        if (resp and resp.lower().find(x) != -1):
            return 1
    return 0


def isResponseStarred(resp):
    for x in ["star", "sitar"]:
        if (resp and resp.lower().find(x) != -1):
            return 1
    return 0


def isResponseFullInbox(resp):
    for x in ["full", "inbox", "in box", "fool", "box"]:
        if (resp and resp.find(x) != -1):
            return 1
    return 0


def isResponseNext(resp):
    for x in ["next", "ext", "text", "test", "axe", "ex", "nest"]:
        if (resp and resp.find(x) != -1):
            return 1
    return 0


def getMessageFromMessageID(service, messageID):
    mescontent = service.users().messages().get(userId='me', id=messageID).execute()
    # print(mescontent)
    # encodedMail = mescontent['payload']['parts'][0]['body']['data']
    # base64_message = encodedMail.replace("-", "+")
    # base64_message = base64_message.replace("_", "/")
    # message = base64.b64decode(base64_message)
    # print(message.decode())
    # return message.decode()
    return mescontent


def decodeMailBody(encodedMail):
    base64_message = encodedMail.replace("-", "+")
    base64_message = base64_message.replace("_", "/")
    message = base64.b64decode(base64_message)
    decodedMessage = message.decode()
    return decodedMessage


def message_full_recursion(m):
    try:
        for i in m:
            mimeType = (i['mimeType'])

            if (i['mimeType']) in ('text/plain'):
                return i['body']['data']
            elif 'parts' in i:
                return message_full_recursion(i['parts'])
        return ""
    except Exception as e:
        return ""


def message_full_recursion_html(m):
    try:
        for i in m:
            mimeType = (i['mimeType'])

            if (i['mimeType']) in ('text/html'):
                return i['body']['data']
            elif 'parts' in i:
                return message_full_recursion_html(i['parts'])
        return ""
    except:
        return ""


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        inbox = getAllMails(service)
        if (inbox):
            mes1 = inbox['messages'][0]['id']
            mescontent = service.users().messages().get(userId='me', id=mes1).execute()
            encodedMail = mescontent['payload']['parts'][0]['body']['data']
            base64_message = encodedMail.replace("-", "+")
            base64_message = base64_message.replace("_", "/")
            message = base64.b64decode(base64_message)
            print(message)

        else:
            print("F###")

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()


def listen():
    r = sr.Recognizer()
    # print(sr.Microphone.list_microphone_names())
    print("listening...")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.1)
        # r.energy_threshold()
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
            return text
        except:
            print("sorry, could not recognise")
            # listen()
