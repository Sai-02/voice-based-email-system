REPLY_TO="Reply-To"
SUBJECT="Subject"
DELIVERED_TO="Delivered-To"
MIME_TYPE_TEXT_PLAIN="text/plain"
FROM="From"
GET_PRIMARY = "category:primary is:unread"
GET_STARRED = "category:primary is:starred"
GET_FULL_INBOX = 'category:primary'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          "https://mail.google.com/",
          "https://www.googleapis.com/auth/gmail.modify",
          "https://www.googleapis.com/auth/gmail.compose",
          "https://www.googleapis.com/auth/gmail.send"]

getStarred = 'is:starred'
getUnread = 'is:unread'
