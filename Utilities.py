from __future__ import print_function
import base64
import speech_recognition as sr
import constant
# If modifying these scopes, delete the file token.json.


def getAllMails(service):
    inbox = service.users().messages().list(userId='me').execute()
    return inbox


def getLastTenMails(service, query):
    inbox = service.users().messages().list(userId='me', q=query).execute()
    return inbox["messages"]


def isResponse1(resp):
    return resp == "one" or resp == "on" or resp == "vun" or resp == "One" or resp == "On" or resp == "Vun" or resp == "1" or resp == "man" or resp == "Man" or resp == "wall" or resp == "Read Email" or resp == "Read mail" or resp == "Read nail" or resp == "Read E mail" or resp == "read e mail" or resp == "reed mail"


def isResponse2(resp):
    return resp == "two" or resp == "tu" or resp == "too" or resp == "Two" or resp == "Tu" or resp == "Too" or resp == "2"


def isResponse3(resp):
    return resp == "three" or resp == "thri" or resp == "tree" or resp == "Three" or resp == "Thri" or resp == "Tree" or resp == "3" or resp == "free" or resp == "Free"


def isResponseRead(resp):
    for x in ["reed", "read", "re ead"]:
        if (resp and resp.lower().find(x) != -1):
            return 1
    return 0


def isResponseSend(resp):
    for x in ["send", "sent", "sed", "sad", "sand"]:
        if (resp and resp.lower().find(x) != -1):
            return 1
    return 0


def isResponseUnread(resp):
    for x in ["unread", "un read", "un red", "umread", "100", "hundred", "Android"]:
        if (resp and resp.lower().find(x) != -1):
            return 1
    return 0


def isResponseStarred(resp):
    for x in ["star", "sitar"]:
        if (resp and resp.lower().find(x) != -1):
            return 1
    return 0


def isResponseFullInbox(resp):
    for x in ["full", "inbox", "in box", "fool", "box"]:
        if (resp and resp.lower().find(x) != -1):
            return 1
    return 0


def isResponseNext(resp):
    for x in ["next", "ext", "text", "test", "axe", "ex", "nest"]:
        if (resp and resp.lower().find(x) != -1):
            return 1
    return 0


def isResponseSearchByName(resp):
    for x in ["name", "nem", "nam", "by", "buy", "search"]:
        if (resp and resp.lower().find(x) != -1):
            return 1
    return 0


def isResponseYes(resp):
    for x in ["Yes", "S", "yeah", "ya", "yo", "yess", "es"]:
        if (resp and resp.lower().find(x) != -1):
            return 1
    return 0


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
    return decodedMessage


def message_full_recursion(m):
    try:
        for i in m:
            mimeType = (i['mimeType'])

            if (i['mimeType']) in ('text/plain'):
                return i['body']['data']
            elif 'parts' in i:
                return message_full_recursion(i['parts'])
        return ""
    except Exception as e:
        return ""


def message_full_recursion_html(m):
    try:
        for i in m:
            mimeType = (i['mimeType'])

            if (i['mimeType']) in ('text/html'):
                return i['body']['data']
            elif 'parts' in i:
                return message_full_recursion_html(i['parts'])
        return ""
    except:
        return ""


def listen():
    r = sr.Recognizer()
    # print(sr.Microphone.list_microphone_names())
    print("listening...")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.1)
        # r.energy_threshold()
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
            return text
        except:
            print("sorry, could not recognise")
            # listen()


def markEmailAsRead(service, messageId):
    service.users().messages().modify(userId='me', id=messageId,
                                      body={'removeLabelIds': [constant.UNREAD]}).execute()


def markEmailAsSpam(service, messageId):
    service.users().messages().modify(userId='me', id=messageId,
                                      body={'addLabelIds': [constant.SPAM]}).execute()

def markEmailAsStarred(service, messageId):
    service.users().messages().modify(userId='me', id=messageId,
                                      body={'addLabelIds': [constant.STARRED]}).execute()
