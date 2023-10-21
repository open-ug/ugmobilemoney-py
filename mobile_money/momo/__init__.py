from .collections import get_access_token, request_to_pay
from .disbursments import get_access_token as get_access_token_disbursments, transfer
import datetime


SANDBOX_URL = "https://sandbox.momodeveloper.mtn.com/"
PRODUCTION_URL = "https://momodeveloper.mtn.com/"


class Collection:
    """
    Intializes a collection Instance.
    This can be used to carry out operations or call the MOMO APIs provided under the collection Product
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
        self.__token_expires_at = datetime.datetime.now() + datetime.timedelta(
            seconds=self.__token_expires_in - 60
        )

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
        payee_note: str = None,
        payer_message: str = None,
    ):
        """
        Collect funds from a client's mobile money account.

        Args:
            amount (str): Amount to be collected.
            phone_number (str): Mobile money account number.
            currency (str): Currency. Will always be EUR for Sandbox.
            external_id (str): External ID usually a unique identifier for the transaction in your system.
            reference_id (str): Reference ID.
            payee_note (str, optional): Message that will be displayed to the client. Defaults to None.
            payer_message (str, optional): Message that will be displayed to the client. Defaults to None.
        """

        # Check if the token has expired
        if self.__token_expires_at < datetime.datetime.now():
            resp = self.__get_access_token()
            data = resp.json()
            self.__access_token = data["access_token"]
            self.__token_expires_in = data["expires_in"]
            self.__token_expires_at = datetime.datetime.now() + datetime.timedelta(
                # Remove 60 seconds to minimize the risk of the token expiring before the request is made
                seconds=self.__token_expires_in - 60
            )

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
            payer_message,
            payee_note,
        )


class Disbursment:
    """
    Intializes a Disbursment Instance.
    This can pe used to carry out operations or call the MOMO APIs provided under the Disbursment Product
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
        self.__token_expires_at = datetime.datetime.now() + datetime.timedelta(
            seconds=self.__token_expires_in - 60
        )

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
        payer_message: str = None,
        payee_note: str = None,
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

        if self.__token_expires_at < datetime.datetime.now():
            resp = self.__get_access_token()
            data = resp.json()
            self.__access_token = data["access_token"]
            self.__token_expires_in = data["expires_in"]
            self.__token_expires_at = datetime.datetime.now() + datetime.timedelta(
                seconds=self.__token_expires_in - 60
            )
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
            payer_message,
            payee_note,
        )


__all__ = ["Collection", "Disbursment"]
