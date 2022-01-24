# Gmail API Libraries
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Twilio Call Library
from twilio.rest import Client

# Python Libraries
import json
import pprint

# Local Library
import app_creds

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
# Setup pretty print to look through dict data
pp = pprint.PrettyPrinter(indent=4)

def pager_duty():

    # login to the gmail account
    service = handle_login()

    # get boolean for if first email is unread
    unreadFlag = get_unread_flag(service)

    if unreadFlag:
        call_user()
    else:
        print("All emails in critical alerts have been read. Shutting down.")

def handle_login():
    """
    Pulled from https://developers.google.com/gmail/api/quickstart/python?authuser=2
    Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service

def get_unread_flag(service):

    # set the user id to the userId of the current service
    userId = 'me'
    # get list of emails
    emailDict = service.users().messages().list(userId = userId).execute()
    emailList = emailDict['messages']

    # get the first message in the inbox
    firstEmail = emailList[0]
    emailId = firstEmail['id']
    emailFormat = 'metadata'
    firstMsg = service.users().messages().get(userId = userId, id = emailId, format=emailFormat).execute()

    # return true if first message is unread else false
    if 'UNREAD' in firstMsg['labelIds']:
        return True
    else:
        return False

def call_user():
    # Twilio phone number goes here. Grab one at https://twilio.com/try-twilio
    # and use the E.164 format, for example: "+12025551234"
    twilNum = app_creds.twilNum

    # list of one or more phone numbers to dial, in "+19732644210" format
    callNum = app_creds.number

    # URL location of TwiML instructions for how to handle the phone call
    TWIML_INSTRUCTIONS_URL = "http://static.fullstackpython.com/phone-calls-python.xml"

    # connect to twilio account using credentials
    # https://stackoverflow.com/questions/51878976/twiliorestclient-removed/52164107
    account = app_creds.twilAccSid
    token = app_creds.twilAuthToken
    client = Client(account, token)

    # set the method to "GET" from default POST because Amazon S3 only
    # serves GET requests on files. Typically POST would be used for apps
    client.calls.create(to=callNum, from_=twilNum, url=TWIML_INSTRUCTIONS_URL, method="GET")

if __name__ == '__main__':
    pager_duty()