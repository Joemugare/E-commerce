import requests
import base64
import datetime
from django.conf import settings

def get_mpesa_access_token():
    """Generate M-Pesa OAuth access token."""
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    headers = {
        "Authorization": "Basic " + base64.b64encode(
            f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}".encode()
        ).decode()
    }
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()['access_token']

def generate_mpesa_password():
    """Generate password for STK Push (Base64 encoded Shortcode + Passkey + Timestamp)."""
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
    encoded = base64.b64encode(data.encode()).decode()
    return encoded, timestamp

def initiate_stk_push(phone_number, amount, order_id):
    """Initiate M-Pesa STK Push payment."""
    access_token = get_mpesa_access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    password, timestamp = generate_mpesa_password()
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerBuyGoodsOnline",  # Use CustomerPayBillOnline for Paybill
        "Amount": str(int(amount)),  # Amount in KSH (integer)
        "PartyA": phone_number,  # Customer's phone number (e.g., 2547xxxxxxxx)
        "PartyB": settings.MPESA_SHORTCODE,  # Your Till/Paybill Number
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": f"Order {order_id}",
        "TransactionDesc": "Payment for order"
    }
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()