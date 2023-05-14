import constant
import streamlit as st
from test import speakText
from Utilities import isResponseYes, markEmailAsSpam, markEmailAsStarred, replyToThisMail
from test import transcribe_speech


def handleMailActions(service, senderEmail, messageID, message, subject, headerId):
    handleMarkAsSpam(service, messageID)
    handleMarkAsStarred(service, messageID)
    handleReplyToThisMail(messageID, service, message,
                          senderEmail, subject, headerId)
    return


def handleMarkAsSpam(service, messageID):
    speakText("Do you want to mark this email as spam?")
    st.text("Do you want to mark this email as spam?")
    res = transcribe_speech()
    if (isResponseYes(res)):
        speakText("Marking as spam")
        st.text("Marking as spam")
        markEmailAsSpam(service, messageID)
        speakText("Email marked as spam successfully!")
        st.text("Email marked as spam successfully!")
    return


def handleMarkAsStarred(service, messageID):
    speakText("Do you want to mark this email as starred?")
    st.text("Do you want to mark this email as starred?")
    res = transcribe_speech()
    if (isResponseYes(res)):
        speakText("Marking as starred")
        st.text("Marking as starred")
        markEmailAsStarred(service, messageID)
        speakText("Email marked as starred successfully!")
        st.text("Email marked as starred successfully!")
    return


def handleReplyToThisMail(messageID, service, message, senderEmail, subject, headerId):
    st.text("Do you want to reply to this mail?")
    speakText("Do you want to reply to this mail?")
    res = transcribe_speech()
    if (isResponseYes(res)):
        st.text("Okay, What should be the reply")
        speakText("Okay, What should be the reply")
        userResponse = transcribe_speech()
        print(userResponse)
        replyToThisMail(messageID, userResponse, message,
                        service, senderEmail, subject, headerId)
        st.text("reply sent")
        speakText("Reply Sent successfully!!")
