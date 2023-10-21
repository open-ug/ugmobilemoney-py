from httpx import Response
import httpx
import base64
import json


SANDBOX_URL = "https://sandbox.momodeveloper.mtn.com/"
PRODUCTION_URL = "https://momodeveloper.mtn.com/"


def get_access_token(
    subscription_key,
    X_Reference_id: str,
    apiKey: str,
    production: bool = True,
) -> Response:
    """
    Get an access token
    """
    BASE_URL = PRODUCTION_URL if production else SANDBOX_URL
    auth_str = X_Reference_id + ":" + apiKey
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        # Basic authentication header Where the username is the X-Reference-Id and the password is the APIKEY. It should be in base64 encoding.
        "Authorization": "Basic " + base64.b64encode(
            auth_str.encode("utf-8")
        ).decode("utf-8"),
    }
    response = httpx.post(
        BASE_URL + "disbursement/token/", headers=headers, json={"grant_type": "client_credentials"}
    )
    return response


def transfer(
    amount: str,
    MSISDN: str,
    currency: str,
    target_environment: str,
    subscription_key: str,
    access_token: str,
    external_id: str,
    reference_id: str,
    callback_url: str,
    payer_message: str = None,
    payee_note: str = None,
) -> Response:
    """
    Transfer funds from your account to client mobile money account.

    Args:
        amount (str): Amount to be transferred.
        MSISDN (str): Mobile money account number.
        currency (str): Currency. Will always be EUR for Sandbox.
        target_environment (str): Target environment. Either SANDBOX or PRODUCTION.
        Ocp_Apim_Subscription_Key (str): Subscription key.
        access_token (str): Access token.
        external_id (str): External ID usually a unique identifier for the transaction in your system.
        reference_id (str): Reference ID.
        callback_url (str): Callback URL.
    """
    BASE_URL = PRODUCTION_URL if target_environment == "production" else SANDBOX_URL
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Authorization": "Bearer " + access_token,
        "X-Callback-Url": callback_url,
        "X-Target-Environment": target_environment,
        "X-Reference-Id": reference_id,
        "Content-Type": "application/json"
    }
    data = {
        "amount": f"{amount}",
        "currency": "EUR" if target_environment == "production" else currency,
        "externalId": f"{external_id}",
        "payee": {
            "partyIdType": "MSISDN",
            "partyId": MSISDN
        },
        "payerMessage": payer_message,
        "payeeNote": payee_note
    }
    response = httpx.post(
        BASE_URL + "disbursement/v1_0/transfer", headers=headers, json=data
    )
    return response


__all__ = ["get_access_token", "transfer"]
