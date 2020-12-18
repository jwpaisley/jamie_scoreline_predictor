import os
from dotenv import load_dotenv
import twilio.rest as Twilio
import json

load_dotenv()

class SMSClient:
    def __init__(self):
        self.authenticate()
        self.load_contacts()

    def authenticate(self):
        TWILIO_ACCT_SID = os.getenv("TWILIO_ACCT_SID")
        TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
        self.client = Twilio.Client(TWILIO_ACCT_SID, TWILIO_AUTH_TOKEN)

    def load_contacts(self):
        self.contacts = [i.strip() for i in os.environ.get("SMS_CONTACTS").split(",")] 

    def send_sms(self, recipient, msg):
        TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
        message = self.client.messages.create(to=recipient, from_=TWILIO_PHONE_NUMBER, body=msg)

    def broadcast_sms(self, msg):
        for contact in self.contacts:
            self.send_sms(contact, msg)