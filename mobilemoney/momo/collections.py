from httpx import Response
from . import PRODUCTION_URL, SANDBOX_URL

def get_access_token(
        subscription_key: str, 
        api_user: str, 
        api_key: str,
        production: bool = True,
    ) -> Response:
    """
    Get an access token

    Args:
        subscription_key (str): Subscription key
        api_user (str): API User, also known as X-Reference-Id.
        api_key (str): API Key
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
        BASE_URL + "collection/token/", headers=headers, json={"grant_type": "client_credentials"}
    )
    return response


def request_to_pay(
        amount: str,
        MSISDN: str,
        currency: str,
        target_environment: str,
        Ocp_Apim_Subscription_Key: str,
        access_token: str,
        external_id: str,
        reference_id: str,
        callback_url: str,
    ) -> Response:
    """
    Request to pay
    """
    BASE_URL = PRODUCTION_URL if target_environment == "production" else SANDBOX_URL

    headers = {
        "Ocp-Apim-Subscription-Key": Ocp_Apim_Subscription_Key,
        "Authorization": "Bearer " + access_token,
        "X-Callback-Url": callback_url,
        "X-Target-Environment": target_environment,
        "X-Reference-Id": reference_id,
    }
    data = {
        "amount": f"{amount}",
        "currency": "EUR" if target_environment == "production" else currency,
        "externalId": f"{external_id}",
        "payer": {
            "partyIdType": "MSISDN",
            "partyId": MSISDN
        },
        "payerMessage": "PAYMENT f for Miapose",
        "payeeNote": "Paying Loan"
    }
    response = httpx.post(
        BASE_URL + "collection/v1_0/requesttopay", headers=headers, json=data
    )
    return response