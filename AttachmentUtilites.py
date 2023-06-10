import constant
import base64
from tika import parser
import streamlit as st
from test import speakText
from Utilities import isResponseYes
from test import transcribe_speech_with_repeat


def handleAttachments(data, service, messageID):

    # Check for PDF Attachments
    attachmentList = getAttachmentIDs(data, constant.APPLICATION_PDF)

    if (len(attachmentList) == 0):
        st.text("This mail has no attachments")
        speakText("This mail has no attachments")
        return
    st.text("This mail has "+str(len(attachmentList))+" attachments")
    speakText("This mail has "+str(len(attachmentList))+" attachments")
    st.text("Do u want to read attachments?")
    speakText("Do u want to read attachments?")
    res = transcribe_speech_with_repeat()
    if (isResponseYes(res)):
        st.text("Getting attachments...")
        speakText("Getting attachments...")
        for attachment in attachmentList:
            st.text("Name of the file is "+attachment["fileName"])
            speakText("Name of the file is "+attachment["fileName"])
            st.text("Do u want to read it ?")
            speakText("Do u want to read it ?")
            res = transcribe_speech_with_repeat()
            if (isResponseYes(res)):
                readableText = getAttachments(
                    service, messageID, attachment["attachmentId"])
                st.text("Content of attachment is : ")
                speakText("Content of attachment is : ")
                st.write(readableText)
                speakText(readableText)
                st.text("Content of attachment is over...")
                speakText("Content of attachment is over...")
    return ""


def getAttachmentIDs(data, fileType):
    temp = []
    for i in data["payload"]["parts"]:
        if (i['mimeType']) in (fileType):
            temp.append(
                {"attachmentId": i['body']['attachmentId'], "fileName": i["filename"]})

    return temp


def getAttachments(service, messageID, attachmentID):
    mescontent = service.users().messages().attachments().get(
        userId='me', messageId=messageID, id=attachmentID).execute()
    decode = base64.urlsafe_b64decode(mescontent["data"])
    with open("attachment.pdf", "wb") as file:
        file.write(decode)
    raw = parser.from_file('attachment.pdf')
    return raw['content']
