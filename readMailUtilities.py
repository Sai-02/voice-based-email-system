from __future__ import print_function
import re
from bs4 import BeautifulSoup
from Utilities import decodeMailBody, isResponseGoBack,  message_full_recursion, message_full_recursion_html
import demoji
import constant
from googleapiclient.discovery import build
import streamlit as st
from test import speakText, listen, transcribe_speech, transcribe_speech_with_repeat
from AttachmentUtilites import handleAttachments
from MailActionUtilities import handleMailActions
from Utilities import getLastTenMails, getMessageFromMessageID, decodeMailBody, isResponse1, isResponse2, isResponse3, isResponseRead, isResponseSend, isResponseStarred, isResponseUnread, isResponseFullInbox, listen, isResponseNext, isResponseSearchByName, markEmailAsRead, isResponseYes


def speakAndWrite(val):
    # st.write(val)
    speakText(val)

def readEmailInParts(content):
    arr = content.split()
    contentLen = len(arr)
    if(contentLen > 60):
        while(arr and len(arr)>0):
            toSpeak = " ".join(arr[0:60])
            st.text(toSpeak)
            speakText(toSpeak)
            arr = arr[60:]
            st.text("This mail has more content. Should I continue?")
            speakText("This mail has more content. Should I continue?")
            res = transcribe_speech_with_repeat()
            if(isResponseYes(res)):
                continue
            else:
                break
    else:
        speakText(content)


def handleReadMail(readMailCategory, creds):
    service = build('gmail', 'v1', credentials=creds)
    inbox = getLastTenMails(service, readMailCategory)
    for i in range(len(inbox)):
        dictionary = getMessageFromMessageID(
            service, inbox[i]["id"])
        # print("                                      ")
        # print("This was your "+str(i+1)+" mail")
        # speakAndWrite("Now next mail is        ")
        try:
            # जय श्री राम
            senderDetails = [sub['value'] for sub in dictionary['payload']
                             ['headers'] if sub['name'] == constant.FROM][0]
            subject = [sub['value'] for sub in dictionary['payload']
                       ['headers'] if sub['name'] == constant.SUBJECT][0]
            headerId = [sub['value'] for sub in dictionary['payload']
                        ['headers'] if sub['name'] == constant.MESSAGE_ID][0]
            senderarr = senderDetails.split(' ')
            senderarrlen = len(senderarr)
            senderEmail = senderarr[senderarrlen - 1]
            # Removing "<" & ">" from email
            senderEmail = re.sub("\<", " ", senderEmail)
            senderEmail = re.sub("\>", " ", senderEmail)
            senderName = " ".join(senderarr[0: (senderarrlen - 1)])

            st.text(senderName + " says " + subject +
                    "\n1. Read Emails \n2. Next Emails \n3.Go back")
            speakAndWrite(senderName + " says " + subject)
            speakAndWrite("Read email")
            speakAndWrite("Next mail")
            speakAndWrite("Go back")
            shouldGoBack = 0
            while (1):
                shouldReadNext = transcribe_speech()
                if (isResponseRead(shouldReadNext)):
                    speakAndWrite("Here is the mail: ")
                    mailBody = readmail(dictionary)
                    st.text("Here is the mail: \n")
                    readEmailInParts(mailBody)
                    speakAndWrite("                       ")
                    speakAndWrite("Over")
                    markEmailAsRead(service, inbox[i]["id"])
                    handleAttachments(
                        dictionary, service, inbox[i]["id"])
                    handleMailActions(service, senderEmail,
                                      inbox[i]["id"], inbox[i], subject, headerId)
                elif (isResponseGoBack(shouldReadNext)):
                    shouldGoBack = 1
                else:
                    speakText("Can you repeat again")
                    continue
                break
            if (shouldGoBack):
                break
        except Exception as e:
            print(e)


def readmail(data):
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
    content = content.replace('\\r', '')
    content = content.replace('\r', '')
    content = content.replace('\\n', '')
    content = content.replace('\n', '')
    content = re.sub(' +', ' ', content)
    content = replaceEmojiCharacter(content)
    content = removeUnicodeCharacters(content)
    content = removeTags(content)
    content = removeBrackets(content)
    return content


def replaceEmojiCharacter(content):
    emojiList = demoji.findall(content)
    for item in emojiList.keys():
        content = content.replace(item, emojiList[item] + ' emoji')
    return content


def removeUnicodeCharacters(content):
    unicoderemove = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               u"\U00002500-\U00002BEF"
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
    content = unicoderemove.sub(r'', content)
    anythingleft = content.encode("ascii", "ignore")
    content = anythingleft.decode()
    content = removeLinks(content)
    return content


def removeTags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script']):
        data.decompose()
    return ' '.join(soup.stripped_strings)


def removeBrackets(content):
    content = re.sub("\[.*?\]", " ", content)
    content = re.sub("\<.*?\>", " ", content)
    content = re.sub("\{.*?\}", " ", content)
    content = re.sub('=+', '=', content)
    return content


def removeLinks(content):
    content = re.sub(r'http\S+', ' ', content)
    content = re.sub(r'https\S+', ' ', content)
    return content
