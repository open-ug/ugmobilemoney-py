import httpx
import json
import base64
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad


CHARGE_CARD_ENDPOINT = "https://api.flutterwave.com/v3/charges?type=card"
MOBILE_MONEY_ENDPOINT = "https://api.flutterwave.com/v3/charges?type=mobile_money_"
MPESA_ENDPOINT = "https://api.flutterwave.com/v3/charges?type=mpesa"
TOKENISED_TRANSACTIONS = "https://api.flutterwave.com/v3/tokenized-charges"


# Function that charges a card using flutterwave api


def charge_card(
    card_number,
    cvv,
    expiry_month,
    expiry_year,
    transaction_id,
    amount,
    email,
    currency="USD",
    FLUTTERWAVE_SECRET=None,
    ENCRYPTION_KEY=None,
):
    """
    Charge a card
    :param card_number: Card number 
    :param cvv: Card CVV 
    :param expiry_month: Expiry month
    :param expiry_year: Expiry Year 
    :param transaction_id: Transaction ID
    :param amount: Amount
    :param email: Email
    :param currency: Currency Default USD
    """

    payload = {
        "amount": amount,
        "tx_ref": transaction_id,
        "currency": currency,
        "card_number": card_number,
        "cvv": cvv,
        "expiry_month": expiry_month,
        "expiry_year": expiry_year,
        "email": email,
    }

    headers = {
        "Authorization": "Bearer " + FLUTTERWAVE_SECRET,
        "Content-Type": "application/json",
    }

    # Encrypt the payload using  3DES algorithm
    payload = json.dumps(payload)
    payload = payload.encode("utf-8")
    encryption_key = ENCRYPTION_KEY.encode("utf-8")
    cipher = DES3.new(encryption_key, DES3.MODE_ECB)
    payload = cipher.encrypt(pad(payload, DES3.block_size))
    payload = base64.b64encode(payload)
    payload = payload.decode("utf-8")

    # Send the request to the api
    response = httpx.post(CHARGE_CARD_ENDPOINT, headers=headers, data={
        "client": payload
    })

    return response


def charge_mobile_money(
        phone_number, transaction_id, order_id, amount, email, country="uganda", currency="UGX", network="MTN",
        FLUTTERWAVE_SECRET=None
):
    """
    Charge Mobile Money
    """
    endpoint = MOBILE_MONEY_ENDPOINT + country

    if phone_number.startswith("+"):
        # change +2567 to 07
        phone_number = phone_number[4:]
        phone_number = "0" + phone_number

    payload = {
        "amount": amount,
        "tx_ref": transaction_id,
        "currency": currency,
        "email": email,
        "phone_number": phone_number,
        "order_id": order_id,
    }

    if country == "ghana":
        payload["network"] = network

    headers = {
        "Authorization": "Bearer " + FLUTTERWAVE_SECRET,
        "Content-Type": "application/json",
    }

    response = httpx.post(endpoint, headers=headers, data=json.dumps(payload))
    return response


def charge_mpesa(phone_number, transaction_id, order_id, amount, email, country="kenya",
                 FLUTTERWAVE_SECRET=None):
    """
    Charge Mpesa
    """
    currency = "KES"
    endpoint = MPESA_ENDPOINT + country
    if country == "kenya":
        currency = "KES"
    elif country == "tanzania":
        currency = "TZS"

    payload = {
        "amount": amount,
        "tx_ref": transaction_id,
        "currency": currency,
        "email": email,
        "phone_number": phone_number,
        "order_id": order_id,
    }

    headers = {
        "Authorization": "Bearer " + FLUTTERWAVE_SECRET,
        "Content-Type": "application/json",
    }

    response = httpx.post(endpoint, headers=headers, data=json.dumps(payload))
    return response


def verify_transaction(transaction_id,
                       flutterwave_secret=None):
    """
    Verify a transaction
    """
    endpoint = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {
        "Authorization": "Bearer " + flutterwave_secret,
        "Content-Type": "application/json",
    }

    response = httpx.get(endpoint, headers=headers)
    return response


def charge_card_token(card_token, transaction_id, amount, email, currency="USD",
                      FLUTTERWAVE_SECRET=None):
    """
    Charge a card using a token
    """
    payload = {
        "amount": amount,
        "tx_ref": transaction_id,
        "currency": currency,
        "email": email,
        "token": card_token,
    }

    headers = {
        "Authorization": "Bearer " + FLUTTERWAVE_SECRET,
        "Content-Type": "application/json",
    }

    response = httpx.post(TOKENISED_TRANSACTIONS,
                          headers=headers, data=json.dumps(payload))
    return response
