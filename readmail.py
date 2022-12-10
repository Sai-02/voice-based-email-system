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
from quickStart import getLastTenUnreadMails, getMessageFromMessageID, decodeMailBody, isResponse1, isResponse2, isResponse3, message_full_recursion,message_full_recursion_html
import pyttsx3

for i in range(10):
    f = open('data' + str(i+1) + '.json')
    data = json.load(f)
    tempo = message_full_recursion(data["payload"]["parts"])
    if(tempo == ""):
        tempo = message_full_recursion_html(data['payload']["parts"])
    
    tempo = decodeMailBody(tempo)
    # f=open("text"+())
    with open("dataop"+str(i+1)+".json", 'x') as f:
        json.dump(tempo, f, indent=4)
    # print(tempo)
    print("\n\n\n\n\n")
    