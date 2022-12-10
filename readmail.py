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
from quickStart import getLastTenUnreadMails, getMessageFromMessageID, decodeMailBody, isResponse1, isResponse2, isResponse3, message_full_recursion, message_full_recursion_html, remove_tags
import pyttsx3
import demoji
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
    tempo = re.sub(' +', ' ', tempo)

    # tempo.replace_with_desc(tempo, sep: str = ":") -> str
    bus = demoji.findall(tempo)
    for item in bus.keys():
        tempo = tempo.replace(item, bus[item] + ' emoji')

    emojiremove = re.compile("["
                             u"\U0001F600-\U0001F64F"  # emoticons
                             u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                             u"\U0001F680-\U0001F6FF"  # transport & map symbols
                             u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                             u"\U00002500-\U00002BEF"  # chinese char
                             u"\U00002702-\U000027B0"
                             u"\U00002702-\U000027B0"
                             u"\U000024C2-\U0001F251"
                             u"\U0001f926-\U0001f937"
                             u"\U00010000-\U0010ffff"
                             u"\u2640-\u2642"
                             u"\u2600-\u2B55"
                             u"\u200d"
                             u"\u23cf"
                             u"\u23e9"
                             u"\u231a"
                             u"\ufe0f"  # dingbats
                             u"\u3030"
                             u"\u00a0"
                             "]+", flags=re.UNICODE)
    tempo = emojiremove.sub(r'', tempo)
    unicoderemove = tempo.encode("ascii", "ignore")
    tempo = unicoderemove.decode()
    # print(bus)

    tempo = remove_tags(tempo)
    tempo = re.sub("\[.*?\]", " ", tempo)
    tempo = re.sub("\<.*?\>", " ", tempo)
    tempo = re.sub("\{.*?\}", " ", tempo)
    tempo = re.sub('=+', '=', tempo)
    # tempo = re.sub('[^A-Za-z0-9]+', ' ', tempo)
    # print(tempo,'\n')
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
