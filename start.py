from __future__ import print_function
from email.message import EmailMessage
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
from Utilities import getLastTenMails,  getMessageFromMessageID, decodeMailBody, isResponse1, isResponse2, isResponse3, isResponseRead, isResponseSend, isResponseStarred, isResponseUnread, isResponseFullInbox, listen, isResponseNext, isResponseSearchByName
import pyttsx3
from tika import parser
from readMailUtilities import readmail
from AttachmentUtilites import handleAttachments
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

service = build('gmail', 'v1', credentials=creds)
inbox = getLastTenMails(service, constant.GET_STARRED)
dictionary = getMessageFromMessageID(
    service, inbox[0]["id"])
handleAttachments(dictionary, service,inbox[0]["id"])
with open("sample.json", "w") as outfile:
    outfile.write(str(dictionary))

# pdf = getAttachments(service, inbox[0]["id"], "")
# print(pdf)
# decode = base64.urlsafe_b64decode(pdf["data"])
# with open("sample.pdf", "wb") as file:
#     file.write(decode)
# raw = parser.from_file('sample.pdf')
# print(raw['content'])
# print(raw)

# with open("sample.json", "w") as outfile:
#     outfile.write(str(atc))
# atc = service.users().messages().attachments().get(
#     userId='me', messageId=messageID, id='').execute()
# while (1):
#     try:
#         speakText("What do you want to do")
#         speakText(" Read Emails ")
#         speakText(" Send  Email ")
#         # r.adjust_for_ambient_noise(source2, duration=0.2)
#         # readOrSendAudio = r.listen(source2)
#         # readOrSend = r.recognize_google(readOrSendAudio, language='en-IN')
#         readOrSend = listen()
#         if (isResponseRead(readOrSend)):
#             speakText("Okay so you want to read your emails")
#             speakText("Please specify what mails do you want to read?")
#             speakText("Unread mails")
#             speakText("Starred mails")
#             speakText("Full inbox")
#             speakText("Search mails by name")
#             readMailType = listen()
#             if (isResponseUnread(readMailType)):
#                 speakText("Reading out latest unread mails: ")
#                 service = build('gmail', 'v1', credentials=creds)
#                 inbox = getLastTenMails(service, constant.GET_PRIMARY)
#                 for i in range(10):
#                     dictionary = getMessageFromMessageID(
#                         service, inbox[i]["id"])
#                     # print("                                      ")
#                     # print("This was your "+str(i+1)+" mail")
#                     # speakText("Now next mail is        ")
#                     try:
#                         # जय श्री राम
#                         senderDetails = [sub['value'] for sub in dictionary['payload']
#                                          ['headers'] if sub['name'] == constant.FROM][0]
#                         subject = [sub['value'] for sub in dictionary['payload']
#                                    ['headers'] if sub['name'] == constant.SUBJECT][0]
#                         senderarr = senderDetails.split(' ')
#                         senderarrlen = len(senderarr)
#                         senderEmail = senderarr[senderarrlen - 1]
#                         # Removing "<" & ">" from email
#                         senderEmail = re.sub("\<", " ", senderEmail)
#                         senderEmail = re.sub("\>", " ", senderEmail)
#                         senderName = " ".join(
#                             senderarr[0: (senderarrlen - 1)])
#                         speakText(senderName + " says " + subject)
#                         speakText("Read email")
#                         speakText("Next mail")
#                         speakText("Go back")
#                         shouldReadNext = listen()
#                         if (isResponseRead(shouldReadNext)):
#                             speakText("Here is the mail: ")
#                             mailBody = readmail(dictionary)
#                             speakText(mailBody)
#                             speakText("                       ")
#                             speakText("Over")
#                             continue
#                         if (isResponseNext(shouldReadNext)):
#                             continue
#                         else:
#                             break
#                     except Exception as e:
#                         print(e)
#             elif (isResponseStarred(readMailType)):
#                 speakText("Reading out latest Starred mails: ")
#                 service = build('gmail', 'v1', credentials=creds)
#                 inbox = getLastTenMails(
#                     service, constant.GET_STARRED)
#                 for i in range(10):
#                     dictionary = getMessageFromMessageID(
#                         service, inbox[i]["id"])
#                     # print("                                      ")
#                     # print("This was your "+str(i+1)+" mail")
#                     # speakText("Now next mail is        ")
#                     try:
#                         senderDetails = [sub['value'] for sub in dictionary['payload']
#                                          ['headers'] if sub['name'] == constant.FROM][0]
#                         subject = [sub['value'] for sub in dictionary['payload']
#                                    ['headers'] if sub['name'] == constant.SUBJECT][0]
#                         senderarr = senderDetails.split(' ')
#                         senderarrlen = len(senderarr)
#                         senderEmail = senderarr[senderarrlen - 1]
#                         # Removing "<" & ">" from email
#                         senderEmail = re.sub("\<", " ", senderEmail)
#                         senderEmail = re.sub("\>", " ", senderEmail)
#                         senderName = " ".join(
#                             senderarr[0: (senderarrlen - 1)])
#                         speakText(senderName + " says " + subject)
#                         speakText("Read email")
#                         speakText("Next mail")
#                         speakText("Go back")
#                         shouldReadNext = listen()
#                         if (isResponseRead(shouldReadNext)):
#                             speakText("Here is the mail: ")
#                             mailBody = readmail(dictionary)
#                             speakText(mailBody)
#                             speakText("                       ")
#                             speakText("Over")
#                             continue
#                         if (isResponseNext(shouldReadNext)):
#                             continue
#                         else:
#                             break
#                     except Exception as e:
#                         print(e)
#             elif (isResponseFullInbox(readMailType)):
#                 speakText("Reading out latest mails: ")
#                 service = build('gmail', 'v1', credentials=creds)
#                 inbox = getLastTenMails(
#                     service, constant.GET_FULL_INBOX)
#                 for i in range(10):
#                     dictionary = getMessageFromMessageID(
#                         service, inbox[i]["id"])
#                     # print("                                      ")
#                     # print("This was your "+str(i+1)+" mail")
#                     # speakText("Now next mail is        ")
#                     try:
#                         senderDetails = [sub['value'] for sub in dictionary['payload']
#                                          ['headers'] if sub['name'] == constant.FROM][0]
#                         subject = [sub['value'] for sub in dictionary['payload']
#                                    ['headers'] if sub['name'] == constant.SUBJECT][0]
#                         senderarr = senderDetails.split(' ')
#                         senderarrlen = len(senderarr)
#                         senderEmail = senderarr[senderarrlen - 1]
#                         # Removing "<" & ">" from email
#                         senderEmail = re.sub("\<", " ", senderEmail)
#                         senderEmail = re.sub("\>", " ", senderEmail)
#                         senderName = " ".join(
#                             senderarr[0: (senderarrlen - 1)])
#                         speakText(senderName + " says " + subject)
#                         speakText("Read email")
#                         speakText("Next mail")
#                         speakText("Go back")
#                         shouldReadNext = listen()
#                         if (isResponseRead(shouldReadNext)):
#                             speakText("Here is the mail: ")
#                             mailBody = readmail(dictionary)
#                             speakText(mailBody)
#                             speakText("                       ")
#                             speakText("Over")
#                             continue
#                         if (isResponseNext(shouldReadNext)):
#                             continue
#                         else:
#                             break
#                     except Exception as e:
#                         print(e)

#             elif (isResponseSearchByName(readMailType)):
#                 speakText("What name should I search for?")
#                 searchName = listen()
#                 speakText("Reading out latest mails by: "+searchName)
#                 service = build('gmail', 'v1', credentials=creds)
#                 inbox = getLastTenMails(
#                     service, constant.SEARCH_MAIL_BY_NAME + searchName)
#                 for i in range(10):
#                     dictionary = getMessageFromMessageID(
#                         service, inbox[i]["id"])
#                     # print("                                      ")
#                     # print("This was your "+str(i+1)+" mail")
#                     # speakText("Now next mail is        ")
#                     try:
#                         senderDetails = [sub['value'] for sub in dictionary['payload']
#                                          ['headers'] if sub['name'] == constant.FROM][0]
#                         subject = [sub['value'] for sub in dictionary['payload']
#                                    ['headers'] if sub['name'] == constant.SUBJECT][0]
#                         senderarr = senderDetails.split(' ')
#                         senderarrlen = len(senderarr)
#                         senderEmail = senderarr[senderarrlen - 1]
#                         # Removing "<" & ">" from email
#                         senderEmail = re.sub("\<", " ", senderEmail)
#                         senderEmail = re.sub("\>", " ", senderEmail)
#                         senderName = " ".join(
#                             senderarr[0: (senderarrlen - 1)])
#                         speakText(senderName + " says " + subject)
#                         speakText("Read email")
#                         speakText("Next mail")
#                         speakText("Go back")
#                         shouldReadNext = listen()
#                         if (isResponseRead(shouldReadNext)):
#                             speakText("Here is the mail: ")
#                             mailBody = readmail(dictionary)
#                             speakText(mailBody)
#                             speakText("                       ")
#                             speakText("Over")
#                             continue
#                         if (isResponseNext(shouldReadNext)):
#                             continue
#                         else:
#                             break
#                     except Exception as e:
#                         print(e)
#             else:
#                 speakText("Can you repeat ?")
#                 continue
#         elif (isResponseSend(readOrSend)):
#             speakText("What is the subject of the mail?")
#             subject = listen()
#             speakText("What is the body of the email")
#             body = listen()
#             speakText("What is recievers's  mail id")
#             mailID = listen()
#             try:
#                 service = build('gmail', 'v1', credentials=creds)
#                 message = EmailMessage()
#                 message.set_content(body)
#                 message['To'] = mailID.replace(" ", "").lower()
#                 print(message['To'])
#                 message['Subject'] = subject
#                 # encoded message
#                 encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
#                     .decode()
#                 create_message = {
#                     'raw': encoded_message
#                 }
#                 send_message = (service.users().messages().send
#                                 (userId="me", body=create_message).execute())
#                 print(F'Message Id: {send_message["id"]}')
#                 speakText("Mail Sent!!")
#             except HttpError as error:
#                 print(F'An error occurred: {error}')
#                 speakText("Receiver's Email Id Incorrect!")
#                 send_message = None
#         else:
#             # speakText("Sorry can you repeat yourself?")
#             print("Sorry can you repeat yourself?")
#             continue

#     except Exception as e:
#         print(e)
#         print("Something went wrong !!")
#         break
