import httpx
import base64
import json
import uuid
from httpx import Response
from . import SANDBOX_URL


def create_api_key(
		subscription_key: str, 
		X_Reference_id: str, 
		providerCallbackHost: str,
	) -> Response:
    """
    Create API Key.

	Args:
		subscription_key (str): Subscription key
		X_Reference_id (str): Reference ID for Your API User. (UUID) 
		providerCallbackHost (str): Provider callback host. eg. google.com.
    """
    headers = {
        "X-Reference-Id": X_Reference_id,
        "Ocp-Apim-Subscription-Key": subscription_key,
    }
    data = {
        "providerCallbackHost": providerCallbackHost,
    }
    _response = httpx.post(
        SANDBOX_URL + "v1_0/apiuser", headers=headers, json=data
    )
    
    if _response.status_code == 201:
        pass
    else:
        return _response
    # Post to /v1_0/apiuser/{X-Reference-Id}/apikey to get an APIKEY for the user
    response = httpx.post(
        SANDBOX_URL + "v1_0/apiuser/" + X_Reference_id + "/apikey", 
        headers={
            "Ocp-Apim-Subscription-Key": subscription_key,
        }
    )
    return response

