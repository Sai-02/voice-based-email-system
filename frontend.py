from __future__ import print_function
import streamlit as st
from readMailUtilities import readmail
import pyttsx3
from Utilities import getLastTenMails, getMessageFromMessageID, decodeMailBody, isResponse1, isResponse2, isResponse3, isResponseRead, isResponseSend, isResponseStarred, isResponseUnread, isResponseFullInbox, listen, isResponseNext, isResponseSearchByName
from test import speakText, listen
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import re
import os.path
import base64
import constant
from email.message import EmailMessage
import speech_recognition as sr

st.title(f"Welcome to VABES: Voice Based Emailing")
start_app = st.button("Start Application", key='start_app')

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def transcribe_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        with st.spinner("Listening..."):
            audio = r.listen(source)
            st.write("Transcribing...")
            try:
                text = r.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                st.write("Could not understand audio")
            except sr.RequestError as e:
                st.write(
                    "Could not request results from Google Speech Recognition service; {0}".format(e))


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          "https://mail.google.com/",
          "https://www.googleapis.com/auth/gmail.modify",
          "https://www.googleapis.com/auth/gmail.compose",
          "https://www.googleapis.com/auth/gmail.send"]
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# else:

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


def speakAndWrite(val):
    st.write(val)
    speakText(val)


if start_app:
    while (1):
        try:
            speakAndWrite("What do you want to do")
            speakAndWrite(" Read Emails ")
            speakAndWrite(" Send  Email ")
            try:

                readOrSend = transcribe_speech()
            except Exception as e:
                print(e)
            if (isResponseRead(readOrSend)):
                speakAndWrite("Okay so you want to read your emails")
                speakAndWrite("Please specify what mails do you want to read?")
                speakAndWrite("Unread mails")
                speakAndWrite("Starred mails")
                speakAndWrite("Full inbox")
                speakAndWrite("Search mails by name")
                readMailType = transcribe_speech()
                if (isResponseUnread(readMailType)):
                    speakAndWrite("Reading out latest unread mails: ")
                    service = build('gmail', 'v1', credentials=creds)
                    inbox = getLastTenMails(service, constant.GET_PRIMARY)
                    for i in range(10):
                        dictionary = getMessageFromMessageID(
                            service, inbox[i]["id"])
                        # print("                                      ")
                        # print("This was your "+str(i+1)+" mail")
                        # speakAndWrite("Now next mail is        ")
                        try:
                            # जय श्री राम
                            senderDetails = [sub['value'] for sub in dictionary['payload']
                                             ['headers'] if sub['name'] == constant.FROM][0]
                            subject = [sub['value'] for sub in dictionary['payload']
                                       ['headers'] if sub['name'] == constant.SUBJECT][0]
                            senderarr = senderDetails.split(' ')
                            senderarrlen = len(senderarr)
                            senderEmail = senderarr[senderarrlen - 1]
                            # Removing "<" & ">" from email
                            senderEmail = re.sub("\<", " ", senderEmail)
                            senderEmail = re.sub("\>", " ", senderEmail)
                            senderName = " ".join(
                                senderarr[0: (senderarrlen - 1)])
                            speakAndWrite(senderName + " says " + subject)
                            speakAndWrite("Read email")
                            speakAndWrite("Next mail")
                            speakAndWrite("Go back")
                            shouldReadNext = transcribe_speech()
                            if (isResponseRead(shouldReadNext)):
                                speakAndWrite("Here is the mail: ")
                                mailBody = readmail(dictionary)
                                speakAndWrite(mailBody)
                                speakAndWrite("                       ")
                                speakAndWrite("Over")
                                continue
                            if (isResponseNext(shouldReadNext)):
                                continue
                            else:
                                break
                        except Exception as e:
                            print(e)
                elif (isResponseStarred(readMailType)):
                    speakAndWrite("Reading out latest Starred mails: ")
                    service = build('gmail', 'v1', credentials=creds)
                    inbox = getLastTenMails(
                        service, constant.GET_STARRED)
                    for i in range(10):
                        dictionary = getMessageFromMessageID(
                            service, inbox[i]["id"])
                        # print("                                      ")
                        # print("This was your "+str(i+1)+" mail")
                        # speakAndWrite("Now next mail is        ")
                        try:
                            senderDetails = [sub['value'] for sub in dictionary['payload']
                                             ['headers'] if sub['name'] == constant.FROM][0]
                            subject = [sub['value'] for sub in dictionary['payload']
                                       ['headers'] if sub['name'] == constant.SUBJECT][0]
                            senderarr = senderDetails.split(' ')
                            senderarrlen = len(senderarr)
                            senderEmail = senderarr[senderarrlen - 1]
                            # Removing "<" & ">" from email
                            senderEmail = re.sub("\<", " ", senderEmail)
                            senderEmail = re.sub("\>", " ", senderEmail)
                            senderName = " ".join(
                                senderarr[0: (senderarrlen - 1)])
                            speakAndWrite(senderName + " says " + subject)
                            speakAndWrite("Read email")
                            speakAndWrite("Next mail")
                            speakAndWrite("Go back")
                            shouldReadNext = transcribe_speech()
                            if (isResponseRead(shouldReadNext)):
                                speakAndWrite("Here is the mail: ")
                                mailBody = readmail(dictionary)
                                speakAndWrite(mailBody)
                                speakAndWrite("                       ")
                                speakAndWrite("Over")
                                continue
                            if (isResponseNext(shouldReadNext)):
                                continue
                            else:
                                break
                        except Exception as e:
                            print(e)
                elif (isResponseFullInbox(readMailType)):
                    speakAndWrite("Reading out latest mails: ")
                    service = build('gmail', 'v1', credentials=creds)
                    inbox = getLastTenMails(
                        service, constant.GET_FULL_INBOX)
                    for i in range(10):
                        dictionary = getMessageFromMessageID(
                            service, inbox[i]["id"])
                        # print("                                      ")
                        # print("This was your "+str(i+1)+" mail")
                        # speakAndWrite("Now next mail is        ")
                        try:
                            senderDetails = [sub['value'] for sub in dictionary['payload']
                                             ['headers'] if sub['name'] == constant.FROM][0]
                            subject = [sub['value'] for sub in dictionary['payload']
                                       ['headers'] if sub['name'] == constant.SUBJECT][0]
                            senderarr = senderDetails.split(' ')
                            senderarrlen = len(senderarr)
                            senderEmail = senderarr[senderarrlen - 1]
                            # Removing "<" & ">" from email
                            senderEmail = re.sub("\<", " ", senderEmail)
                            senderEmail = re.sub("\>", " ", senderEmail)
                            senderName = " ".join(
                                senderarr[0: (senderarrlen - 1)])
                            speakAndWrite(senderName + " says " + subject)
                            speakAndWrite("Read email")
                            speakAndWrite("Next mail")
                            speakAndWrite("Go back")
                            shouldReadNext = transcribe_speech()
                            if (isResponseRead(shouldReadNext)):
                                speakAndWrite("Here is the mail: ")
                                mailBody = readmail(dictionary)
                                speakAndWrite(mailBody)
                                speakAndWrite("                       ")
                                speakAndWrite("Over")
                                continue
                            if (isResponseNext(shouldReadNext)):
                                continue
                            else:
                                break
                        except Exception as e:
                            print(e)

                elif (isResponseSearchByName(readMailType)):
                    speakAndWrite("What name should I search for?")
                    searchName = transcribe_speech()
                    speakAndWrite("Reading out latest mails by: "+searchName)
                    service = build('gmail', 'v1', credentials=creds)
                    inbox = getLastTenMails(
                        service, constant.SEARCH_MAIL_BY_NAME + searchName)
                    for i in range(10):
                        dictionary = getMessageFromMessageID(
                            service, inbox[i]["id"])
                        # print("                                      ")
                        # print("This was your "+str(i+1)+" mail")
                        # speakAndWrite("Now next mail is        ")
                        try:
                            senderDetails = [sub['value'] for sub in dictionary['payload']
                                             ['headers'] if sub['name'] == constant.FROM][0]
                            subject = [sub['value'] for sub in dictionary['payload']
                                       ['headers'] if sub['name'] == constant.SUBJECT][0]
                            senderarr = senderDetails.split(' ')
                            senderarrlen = len(senderarr)
                            senderEmail = senderarr[senderarrlen - 1]
                            # Removing "<" & ">" from email
                            senderEmail = re.sub("\<", " ", senderEmail)
                            senderEmail = re.sub("\>", " ", senderEmail)
                            senderName = " ".join(
                                senderarr[0: (senderarrlen - 1)])
                            speakAndWrite(senderName + " says " + subject)
                            speakAndWrite("Read email")
                            speakAndWrite("Next mail")
                            speakAndWrite("Go back")
                            shouldReadNext = transcribe_speech()
                            if (isResponseRead(shouldReadNext)):
                                speakAndWrite("Here is the mail: ")
                                mailBody = readmail(dictionary)
                                speakAndWrite(mailBody)
                                speakAndWrite("                       ")
                                speakAndWrite("Over")
                                continue
                            if (isResponseNext(shouldReadNext)):
                                continue
                            else:
                                break
                        except Exception as e:
                            print(e)
                else:
                    speakAndWrite("Can you repeat ?")
                    continue
            elif (isResponseSend(readOrSend)):
                speakAndWrite("What is the subject of the mail?")
                subject = transcribe_speech()
                speakAndWrite("What is the body of the email")
                body = transcribe_speech()
                speakAndWrite("What is recievers's  mail id")
                mailID = transcribe_speech()
                try:
                    service = build('gmail', 'v1', credentials=creds)
                    message = EmailMessage()
                    message.set_content(body)
                    message['To'] = mailID.replace(" ", "").lower()
                    print(message['To'])
                    message['Subject'] = subject
                    # encoded message
                    encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
                        .decode()
                    create_message = {
                        'raw': encoded_message
                    }
                    send_message = (service.users().messages().send
                                    (userId="me", body=create_message).execute())
                    print(F'Message Id: {send_message["id"]}')
                    speakAndWrite("Mail Sent!!")
                except HttpError as error:
                    print(F'An error occurred: {error}')
                    speakAndWrite("Receiver's Email Id Incorrect!")
                    send_message = None
            else:
                # speakAndWrite("Sorry can you repeat yourself?")
                print("Sorry can you repeat yourself?")
                continue

        except Exception as e:
            print(e)
            print("Something went wrong !!")
            break
