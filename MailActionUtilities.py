import constant
import streamlit as st
from test import speakText
from Utilities import isResponseYes, markEmailAsSpam, markEmailAsStarred, replyToThisMail, validateEmail, decodeMailBody, isResponseGoBack,  message_full_recursion, message_full_recursion_html
from test import transcribe_speech_with_repeat, transcribe_speech_with_repeat_for_send
import base64
from email.message import EmailMessage


def handleMailActions(service, senderEmail, messageID, message, subject, headerId, encodedMailContent):
    handleMarkAsSpam(service, messageID)
    handleMarkAsStarred(service, messageID)
    handleReplyToThisMail(messageID, service, message,
                          senderEmail, subject, headerId)
    handleForwardToThisMail(messageID, service, message,
                          senderEmail, subject, headerId, encodedMailContent)
    return


def handleMarkAsSpam(service, messageID):
    st.text("Do you want to mark this email as spam?")
    speakText("Do you want to mark this email as spam?")
    res = transcribe_speech_with_repeat()
    if (isResponseYes(res)):
        st.text("Marking as spam")
        speakText("Marking as spam")
        markEmailAsSpam(service, messageID)
        st.text("Email marked as spam successfully!")
        speakText("Email marked as spam successfully!")
    return


def handleMarkAsStarred(service, messageID):
    st.text("Do you want to mark this email as starred?")
    speakText("Do you want to mark this email as starred?")
    res = transcribe_speech_with_repeat()
    if (isResponseYes(res)):
        st.text("Marking as starred")
        speakText("Marking as starred")
        markEmailAsStarred(service, messageID)
        st.text("Email marked as starred successfully!")
        speakText("Email marked as starred successfully!")
    return


def handleReplyToThisMail(messageID, service, message, senderEmail, subject, headerId):
    st.text("Do you want to reply to this mail?")
    speakText("Do you want to reply to this mail?")
    res = transcribe_speech_with_repeat()
    if (isResponseYes(res)):
        st.text("Okay, What should be the reply")
        speakText("Okay, What should be the reply")
        userResponse = transcribe_speech_with_repeat_for_send()
        print(userResponse)
        replyToThisMail(messageID, userResponse, message,
                        service, senderEmail, subject, headerId)
        st.text("Reply Sent successfully!")
        speakText("Reply Sent successfully!!")

def handleForwardToThisMail(messageID, service, message, senderEmail, subject, headerId, encodedMailContent):
    st.text("Do you want to forward this email?")
    speakText("Do you want to forward this email?")
    res = transcribe_speech_with_repeat_for_send()
    if (isResponseYes(res)):
        st.markdown("**:blue[What is receivers's mail id?]**")
        speakText("What is receivers's  mail id")
        mailID = transcribe_speech_with_repeat_for_send()
        mailID = mailID.replace(" ", "").replace("attherate", "@").lower()
        while (not validateEmail(mailID)):
            st.error("This Email is Invalid! Can you please repeat...", icon="💀")
            speakText("This Email is Invalid! Can you please repeat?")
            mailID = transcribe_speech_with_repeat_for_send()
            mailID = mailID.replace(" ", "").replace("attherate", "@").lower()

        decodedMail = readMailForForwarding(encodedMailContent);


        message = EmailMessage()
        message.set_content(decodedMail)
        message['To'] = mailID
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



        st.text("Mail Forwarded successfully!!")
        speakText("Mail Forwarded successfully!!")

def readMailForForwarding(data):
    # Getting data in text format
    content = ""
    try:
        if "parts" in data["payload"]:
            content = message_full_recursion(data["payload"]["parts"])
            if (content == ""):
                content = message_full_recursion_html(data['payload']["parts"])
            if (content == ""):
                content = data['payload']["body"]["data"]
        else:
            content = data['payload']["body"]["data"]

    except:
        print("Unexpected error")
    content = decodeMailBody(content)
    return content
