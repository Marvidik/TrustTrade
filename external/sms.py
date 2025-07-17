from twilio.rest import Client
from django.conf import settings
from dotenv import load_dotenv
import os



# Now use them
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_VERIFY_SID = os.getenv('TWILIO_VERIFY_SID')
client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)

def send_otp(phone_number):
    verification = client.verify \
        .services(TWILIO_VERIFY_SID) \
        .verifications \
        .create(to=phone_number, channel="sms")
    return verification.status  # usually "pending"

# send_otp("+2348132106194")

def verify_otp(phone_number, code):
    check = client.verify \
        .services(TWILIO_VERIFY_SID) \
        .verification_checks \
        .create(to=phone_number, code=code)
    return check.status  # "approved" if correct


# verify_otp("+2348132106194", "680787")  # Replace 123456 with the actual user input
