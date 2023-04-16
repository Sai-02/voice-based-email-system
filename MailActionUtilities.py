import constant
import streamlit as st
from test import speakText
from Utilities import isResponseYes, markEmailAsSpam, markEmailAsStarred
from test import transcribe_speech


def handleMailActions(service, messageID):
    handleMarkAsSpam(service, messageID)
    handleMarkAsStarred(service, messageID)
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