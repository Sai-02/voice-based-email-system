from __future__ import print_function
import re
from bs4 import BeautifulSoup
from Services import decodeMailBody,  message_full_recursion, message_full_recursion_html
import demoji


def readmail(data):
    # Getting data in text format
    content = ""
    try:
        if "parts" in data["payload"]:
            content = message_full_recursion(data["payload"]["parts"])
            if (content == ""):
                content = message_full_recursion_html(data['payload']["parts"])
            if(content == ""):
                content = data['payload']["body"]["data"]
        else:
            content = data['payload']["body"]["data"]
            
    except:
        print("Unexpected error")
    content = decodeMailBody(content)
    content = content.replace('\r', '')
    content = content.replace('\n', '')
    content = re.sub(' +', ' ', content)
    content = replaceEmojiCharacter(content)
    content = removeUnicodeCharacters(content)
    content = removeTags(content)
    content = removeBrackets(content)
    return content


def replaceEmojiCharacter(content):
    bus = demoji.findall(content)
    for item in bus.keys():
        content = content.replace(item, bus[item] + ' emoji')
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
    content = re.sub(r'http\S+', ' Link ', content)
    content = re.sub(r'https\S+', ' Link ', content)
    return content
