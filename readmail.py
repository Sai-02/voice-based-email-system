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
from quickStart import getLastTenUnreadMails, getMessageFromMessageID, decodeMailBody, isResponse1, isResponse2, isResponse3, message_full_recursion, message_full_recursion_html
import pyttsx3
from bs4 import BeautifulSoup
for i in range(10):
    isHtml = False
    f = open('data' + str(i+1) + '.json')
    data = json.load(f)
    tempo = message_full_recursion(data["payload"]["parts"])
    if (tempo == ""):
        tempo = message_full_recursion_html(data['payload']["parts"])
        isHtml = True
    tempo = decodeMailBody(tempo)
    tempo = tempo.replace('\r', '')
    tempo = tempo.replace('\n', '')
    tempo = tempo.replace('\"', '\"')
    tempo = re.sub("\[.*?\]"," ",tempo)
    tempo = re.sub("\<.*?\>"," ",tempo)
    tempo = re.sub(' +', ' ', tempo)
    # tempo = re.sub('[^A-Za-z0-9]+', ' ', tempo)
    with open("hehehe"+str(i+1)+".json", 'w') as f:
        json.dump(tempo, f, indent=4)
    # if (isHtml):
    #     soup = BeautifulSoup(tempo, features="html.parser")

    #     # kill all script and style elements
    #     for script in soup(["script", "style"]):
    #         script.extract()    # rip it out

    #     # get text
    #     text = soup.get_text()

    #     # break into lines and remove leading and trailing space on each
    #     lines = (line.strip() for line in text.splitlines())
    #     # break multi-headlines into a line each
    #     chunks = (phrase.strip()
    #               for line in lines for phrase in line.split("  "))
    #     # drop blank lines
    #     text = '\n'.join(chunk for chunk in chunks if chunk)
    #     tempo = text

    # f=open("text"+())
    # tempo = re.sub('[^n]+', ' ', tempo)
    # tempo = re.sub('[^r]+', ' ', tempo)
    # with open("text"+str(i+1)+".txt", 'w') as f:
    #     f.write(tempo)

    # print(tempo)
    # print("\n\n\n\n\n")
