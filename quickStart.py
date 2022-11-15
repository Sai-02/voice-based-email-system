from __future__ import print_function
import base64
import os.path
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

getStarred = 'is:starred'
getUnread = 'is:unread'


def getAllMails(service):
    inbox = service.users().messages().list(userId='me').execute()
    return inbox


def getLastTenUnreadMails(service):
    inbox = service.users().messages().list(userId='me').execute()
    return inbox["messages"]


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
    decodedMessage = re.sub(
        r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", decodedMessage)
    decodedMessage = re.sub('<.*?>', '', decodedMessage)
    return decodedMessage


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
