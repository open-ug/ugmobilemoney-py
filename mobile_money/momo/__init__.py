from .collections import get_access_token, request_to_pay
from .disbursments import get_access_token as get_access_token_disbursments, transfer


SANDBOX_URL = "https://sandbox.momodeveloper.mtn.com/"
PRODUCTION_URL = "https://momodeveloper.mtn.com/"



class Collection:
    """
    Intializes a collection Instance.
    """

    def __init__(
            self, 
            subscription_key: str, 
            api_user: str, 
            api_key: str, 
            callback_url: str,
            production: bool = True,
        ):
        self.__subscription_key = subscription_key
        self.__api_user = api_user
        self.__api_key = api_key
        self.__production = production
        self.__callback_url = callback_url
        resp = self.__get_access_token()
        data = resp.json()
        self.__access_token = data["access_token"]
        self.__token_expires_in = data["expires_in"]


    def __get_access_token(self):
        """
        Get an access token
        """
        return get_access_token(
            self.__subscription_key, 
            self.__api_user, 
            self.__api_key,
            self.__production,
        )

    def collect(
            self,
            amount: str,
            phone_number: str,
            currency: str,
            external_id: str,
            reference_id: str,
        ):
        """
        Collect funds from a client's mobile money account.

        Args:
            amount (str): Amount to be collected.
            phone_number (str): Mobile money account number.
            currency (str): Currency. Will always be EUR for Sandbox.
            external_id (str): External ID usually a unique identifier for the transaction in your system.
            reference_id (str): Reference ID.
        """
        return request_to_pay(
            amount,
            phone_number,
            currency,
            "production" if self.__production else "sandbox",
            self.__subscription_key,
            self.__access_token,
            external_id,
            reference_id,
            self.__callback_url,
        )


class Disbursment:
    """
    Intializes a Disbursment Instance.
    """

    def __init__(
            self, 
            subscription_key: str, 
            api_user: str, 
            api_key: str, 
            callback_url: str,
            production: bool = True,
        ):
        self.__subscription_key = subscription_key
        self.__api_user = api_user
        self.__api_key = api_key
        self.__production = production
        self.__callback_url = callback_url
        resp = self.__get_access_token()
        data = resp.json()
        self.__access_token = data["access_token"]
        self.__token_expires_in = data["expires_in"]


    def __get_access_token(self):
        """
        Get an access token
        """
        return get_access_token_disbursments(
            self.__subscription_key, 
            self.__api_user, 
            self.__api_key,
            self.__production,
        )

    def transfer(
            self,
            amount: str,
            phone_number: str,
            currency: str,
            external_id: str,
            reference_id: str,
        ):
        """
        Transfer funds from your account to client mobile money account.

        Args:
            amount (str): Amount to be transferred.
            phone_number (str): Mobile money account number.
            currency (str): Currency. Will always be EUR for Sandbox.
            external_id (str): External ID usually a unique identifier for the transaction in your system.
            reference_id (str): Reference ID.
        """
        return transfer(
            amount,
            phone_number,
            currency,
            "production" if self.__production else "sandbox",
            self.__subscription_key,
            self.__access_token,
            external_id,
            reference_id,
            self.__callback_url,
        )


__all__ = ["Collection", "Disbursment"]