from __future__ import print_function
import streamlit as st
import streamlit.components.v1 as components
from readMailUtilities import readmail
import pyttsx3
from Utilities import getLastTenMails, getMessageFromMessageID, decodeMailBody, isResponse1, isResponse2, isResponse3, isResponseRead, isResponseSend, isResponseStarred, isResponseUnread, isResponseFullInbox, listen, isResponseNext, isResponseSearchByName, markEmailAsRead
from test import speakText, listen, transcribe_speech
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
from AttachmentUtilites import handleAttachments
st.title(f"Welcome to VABES: Voice Based Emailing")
start_app = st.button("Start Application", key='start_app')

hide_streamlit_style = """
            <style>
            *{white-space:initial !important;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .css-14xtw13{opacity: 0 !important;}
            *{margin:0;padding:0;box-sizing:border-box}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


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
    # st.write(val)
    speakText(val)


if start_app:
    while (1):
        try:
            st.text("What do you want to do\n1. Read Emails \n2. Send Email")
            speakText("What do you want to do")
            speakText(" Read Emails ")
            speakText(" Send  Email ")

            try:

                readOrSend = transcribe_speech()
            except Exception as e:
                print(e)
            if (isResponseRead(readOrSend)):
                st.text("Okay so you want to read your emails \nPlease specify what mails do you want to read? \n1. Unread mails \n2. Starred mails \n3. Full Inbox \n4. Search mails by name")
                speakAndWrite("Okay so you want to read your emails")
                speakAndWrite("Please specify what mails do you want to read?")
                speakAndWrite("Unread mails")
                speakAndWrite("Starred mails")
                speakAndWrite("Full inbox")
                speakAndWrite("Search mails by name")
                readMailType = transcribe_speech()
                if (isResponseUnread(readMailType)):
                    st.text("Reading out latest unread mails: ")
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

                            st.text(senderName + " says " + subject +
                                    "\n1. Read Emails \n2. Next Emails \n3.Go back")
                            speakAndWrite(senderName + " says " + subject)
                            speakAndWrite("Read email")
                            speakAndWrite("Next mail")
                            speakAndWrite("Go back")
                            shouldReadNext = transcribe_speech()
                            if (isResponseRead(shouldReadNext)):
                                speakAndWrite("Here is the mail: ")
                                mailBody = readmail(dictionary)
                                st.text("Here is the mail: \n"+mailBody)
                                speakAndWrite(mailBody)
                                speakAndWrite("                       ")
                                speakAndWrite("Over")
                                markEmailAsRead(service, inbox[i]["id"])
                                handleAttachments(
                                    dictionary, service, inbox[i]["id"])
                                continue
                            if (isResponseNext(shouldReadNext)):
                                continue
                            else:
                                break
                        except Exception as e:
                            print(e)
                elif (isResponseStarred(readMailType)):
                    st.text("Reading out latest Starred mails: ")
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
                            st.text(senderName + " says " + subject)
                            speakAndWrite(senderName + " says " + subject)
                            st.text("1. Read email \n2. Next mail \n3. Go back")
                            speakAndWrite("Read email")
                            speakAndWrite("Next mail")
                            speakAndWrite("Go back")
                            shouldReadNext = transcribe_speech()
                            if (isResponseRead(shouldReadNext)):
                                speakAndWrite("Here is the mail: ")
                                mailBody = readmail(dictionary)
                                st.text("Here is the mail: \n"+mailBody)
                                speakAndWrite(mailBody)
                                speakAndWrite("                       ")
                                speakAndWrite("Over")
                                handleAttachments(
                                    dictionary, service, inbox[i]["id"])
                                continue
                            if (isResponseNext(shouldReadNext)):
                                continue
                            else:
                                break
                        except Exception as e:
                            print(e)
                elif (isResponseFullInbox(readMailType)):
                    st.text("Reading out latest mails: ")
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
                            st.text(senderName + " says " + subject +
                                    "\n1. Read Email \n2. Next Email \n3.Go back")
                            speakAndWrite(senderName + " says " + subject)
                            speakAndWrite("Read email")
                            speakAndWrite("Next mail")
                            speakAndWrite("Go back")
                            shouldReadNext = transcribe_speech()
                            if (isResponseRead(shouldReadNext)):
                                speakAndWrite("Here is the mail: ")
                                mailBody = readmail(dictionary)
                                st.text("Here is the mail: \n"+mailBody)
                                speakAndWrite(mailBody)
                                speakAndWrite("                       ")
                                speakAndWrite("Over")
                                handleAttachments(
                                    dictionary, service, inbox[i]["id"])
                                continue
                            if (isResponseNext(shouldReadNext)):
                                continue
                            else:
                                break
                        except Exception as e:
                            print(e)

                elif (isResponseSearchByName(readMailType)):
                    st.text("What name should I search for?")
                    speakAndWrite("What name should I search for?")
                    searchName = transcribe_speech()
                    st.text("Reading out latest mails by: "+searchName)
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
                            st.text(senderName + " says " + subject +
                                    "\n1. Read Email \n2. Next Email \n3.Go back")
                            speakAndWrite(senderName + " says " + subject)
                            speakAndWrite("Read email")
                            speakAndWrite("Next mail")
                            speakAndWrite("Go back")
                            shouldReadNext = transcribe_speech()
                            if (isResponseRead(shouldReadNext)):
                                speakAndWrite("Here is the mail: ")
                                mailBody = readmail(dictionary)
                                st.text("Here is the mail: \n"+mailBody)
                                speakAndWrite(mailBody)
                                speakAndWrite("                       ")
                                speakAndWrite("Over")
                                handleAttachments(
                                    dictionary, service, inbox[i]["id"])
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
                st.markdown("**:blue[What is the subject of the mail?]**")
                speakAndWrite("What is the subject of the mail?")
                subject = transcribe_speech()
                st.markdown("**:blue[What is the body of the email?]**")
                speakAndWrite("What is the body of the email")
                body = transcribe_speech()
                st.markdown("**:blue[What is receivers's mail id?]**")
                speakAndWrite("What is receivers's  mail id")
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
                    st.text("Mail Sent!!")
                    speakAndWrite("Mail Sent!!")
                except HttpError as error:
                    print(F'An error occurred: {error}')
                    st.text("Receiver's Email Id Incorrect!")
                    speakAndWrite("Receiver's Email Id Incorrect!")
                    send_message = None
            else:
                # speakAndWrite("Sorry can you repeat yourself?")
                st.text("Sorry can you repeat yourself?")
                print("Sorry can you repeat yourself?")
                continue

        except Exception as e:
            print(e)
            st.text("Something went wrong !")
            print("Something went wrong !")
            break
