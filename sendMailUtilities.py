from __future__ import print_function
import streamlit as st
import base64
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from Utilities import isResponseYes,validateEmail
from test import speakText, transcribe_speech_with_repeat_for_send


def speakAndWrite(val):
    # st.write(val)
    speakText(val)


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          "https://mail.google.com/",
          "https://www.googleapis.com/auth/gmail.modify",
          "https://www.googleapis.com/auth/gmail.compose",
          "https://www.googleapis.com/auth/gmail.send"]


def gmail_send_message():
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content('This is automated draft mail')

        message['To'] = 'ayush2000mickey@gmail.com',
        message['From'] = 'saiprashant.saxena@gmail.com'
        message['Subject'] = 'Automated draft'

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message


if __name__ == '__main__':
    gmail_send_message()


def handleSendMail(creds):
    st.markdown("**:blue[What is the subject of the mail?]**")
    speakAndWrite("What is the subject of the mail?")
    subject = transcribe_speech_with_repeat_for_send()
    st.markdown("**:blue[What is the body of the email?]**")
    speakAndWrite("What is the body of the email")
    body = transcribe_speech_with_repeat_for_send()
    st.markdown("**:blue[What is receivers's mail id?]**")
    speakAndWrite("What is receivers's  mail id")
    mailID = transcribe_speech_with_repeat_for_send()
    mailID = mailID.replace(" ", "").replace("attherate", "@").lower()
    while (not validateEmail(mailID)):
        st.error("This Email is Invalid! Can you please repeat...", icon="💀")
        speakAndWrite("This Email is Invalid!")
        speakAndWrite("Can you please repeat?")
        mailID = transcribe_speech_with_repeat_for_send()
        mailID = mailID.replace(" ", "").replace("attherate", "@").lower()

    st.markdown("**:blue[Do you want to add cc to this mail?]**")
    speakAndWrite("Do you want to add cc to this mail?")
    shouldAddCc = transcribe_speech_with_repeat_for_send()
    ccMailID = ""
    if (isResponseYes(shouldAddCc)):
        st.markdown("**:blue[What is the mail id?]**")
        speakAndWrite("What is the mail id?")
        ccMailID = transcribe_speech_with_repeat_for_send()
        ccmailID = ccmailID.replace(" ", "").replace("attherate", "@").lower()
        while (not validateEmail(ccmailID)):
            st.error("This Email is Invalid! Can you please repeat...", icon="💀")
            speakAndWrite("This Email is Invalid!")
            speakAndWrite("Can you please repeat?")
            ccmailID = transcribe_speech_with_repeat_for_send()
            ccmailID = ccmailID.replace(" ", "").replace("attherate", "@").lower()

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()
        message.set_content(body)
        message['To'] = mailID
        if (len(ccMailID) > 0):
            message['cc'] = ccMailID.replace(
                " ", "").replace("attherate", "@").lower()
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
        st.markdown("**:green[Mail Sent Successfully!]**")
        speakAndWrite("Mail Sent Successfully!")
    except HttpError as error:
        print(F'An error occurred: {error}')
        st.text("Receiver's Email Id Incorrect!")
        speakAndWrite("Receiver's Email Id Incorrect!")
        send_message = None
