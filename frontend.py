from __future__ import print_function
import streamlit as st
import streamlit.components.v1 as components
from readMailUtilities import readmail, handleReadMail
import pyttsx3
from Utilities import getLastTenMails, getMessageFromMessageID, decodeMailBody, isResponse1, isResponse2, isResponse3, isResponseRead, isResponseSend, isResponseStarred, isResponseUnread, isResponseFullInbox, listen, isResponseNext, isResponseSearchByName, markEmailAsRead, isResponseGoBack
from sendMailUtilities import handleSendMail
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
                while(1):
                    st.text("Okay so you want to read your emails \nPlease specify what mails do you want to read? \n1. Unread mails \n2. Starred mails \n3. Full Inbox \n4. Search mails by name")
                    speakAndWrite("Okay so you want to read your emails")
                    speakAndWrite("Please specify what mails do you want to read?")
                    speakAndWrite("Unread mails")
                    speakAndWrite("Starred mails")
                    speakAndWrite("Full inbox")
                    speakAndWrite("Search mails by name")
                    speakAndWrite("Go back")
                    readMailType = transcribe_speech()
                    if (isResponseUnread(readMailType)):
                        st.text("Reading out latest unread mails: ")
                        speakAndWrite("Reading out latest unread mails: ")
                        handleReadMail(constant.GET_PRIMARY, creds)
                    elif (isResponseStarred(readMailType)):
                        st.text("Reading out latest Starred mails: ")
                        speakAndWrite("Reading out latest Starred mails: ")
                        handleReadMail(constant.GET_STARRED, creds)
                    elif (isResponseFullInbox(readMailType)):
                        st.text("Reading out latest mails: ")
                        speakAndWrite("Reading out latest mails: ")
                        handleReadMail(constant.GET_FULL_INBOX, creds)
                    elif (isResponseSearchByName(readMailType)):
                        st.text("What name should I search for?")
                        speakAndWrite("What name should I search for?")
                        searchName = transcribe_speech()
                        st.text("Reading out latest mails by: "+searchName)
                        speakAndWrite("Reading out latest mails by: "+searchName)
                        handleReadMail(
                            constant.SEARCH_MAIL_BY_NAME + searchName, creds)
                    elif (isResponseGoBack(readMailType)):
                        break
                    else:
                        speakAndWrite("Can you please repeat ?")
                        continue

                    break
            elif (isResponseSend(readOrSend)):
                handleSendMail(creds)
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
