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
import pyttsx3
from readMailUtilities import readmail

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
            print(readOrSend)
    except:
        print("Something went wrong !!")
        break
