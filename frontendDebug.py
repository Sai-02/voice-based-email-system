from __future__ import print_function
import streamlit as st
import streamlit.components.v1 as components
from readMailUtilities import readmail, handleReadMail
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
            st.text("Okay so you want to read your emails \nPlease specify what mails do you want to read? \n1. Unread mails \n2. Starred mails \n3. Full Inbox \n4. Search mails by name")
            speakAndWrite("Reading out latest unread mails: ")
            handleReadMail(constant.GET_FULL_INBOX, creds)

        except Exception as e:
            print(e)
            st.text("Something went wrong !")
            print("Something went wrong !")
            break
