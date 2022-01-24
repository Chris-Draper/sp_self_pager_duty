# Twilio Libraries
from twilio.rest import Client

# Local Libraries
import app_creds

def test_call():
    # Twilio phone number goes here. Grab one at https://twilio.com/try-twilio
    # and use the E.164 format, for example: "+12025551234"
    twilioNum = app_creds.twilNum

    # list of one or more phone numbers to dial, in "+19732644210" format
    callNum = [app_creds.number]

    # URL location of TwiML instructions for how to handle the phone call
    TWIML_INSTRUCTIONS_URL = "http://static.fullstackpython.com/phone-calls-python.xml"

    # connect to twilio account using credentials
    account = app_creds.twilAccSid
    token = app_creds.twilAuthToken
    client = Client(account, token)

    # set the method to "GET" from default POST because Amazon S3 only
    # serves GET requests on files. Typically POST would be used for apps
    client.calls.create(to=callNum, from_=twilioNum, url=TWIML_INSTRUCTIONS_URL, method="GET")

if __name__ == "__main__":
    test_call()