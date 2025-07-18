import requests
from dotenv import load_dotenv
import os



# Now use them
PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')

def initialize_payment(email, amount):
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "email": email,
        "amount": int(amount) * 100,  # in kobo
    }
    response = requests.post(
        "https://api.paystack.co/transaction/initialize",
        json=data,
        headers=headers
    )
    return response.json()


def verify_payment(reference):
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
    }
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    response = requests.get(url, headers=headers)
    return response.json()
