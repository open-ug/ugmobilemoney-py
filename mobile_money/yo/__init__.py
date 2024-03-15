"""
Yo! API for mobile money transactions.
"""
import xmltodict
from httpx import Response
from .deposit import deposit_funds
from .withdraw import withdraw
from .status import get_transaction_status


class Transaction:
    """
    Transaction class for mobile money transactions.
    """
    tx_ref = None
    sandbox = False
    private_transaction_reference = None

    def __init__(
        self,
        api_username: str,
        api_password: str,
        private_tx_ref: str = None,
        tx_ref: str = None,
        sandbox: bool = False,
    ):
        self.api_username = api_username
        self.api_password = api_password
        self.private_transaction_reference = private_tx_ref
        self.tx_ref = tx_ref
        self.sandbox = sandbox

    def get_status(self):
        """
        Get the status of a transaction.
        """

        return parse_response(get_transaction_status(
            APIUsername=self.api_username,
            APIPassword=self.api_password,
            TransactionReference=self.tx_ref,
            PrivateTransactionReference=self.private_transaction_reference,
            sandbox=self.sandbox,
        ))


class Yo:
    """
    Yo class for mobile money transactions.
    """
    tx_ref = None

    def __init__(self, api_username: str, api_password: str, sandbox: bool = False):
        self.api_username = api_username
        self.api_password = api_password
        self.sandbox = sandbox

    def deposit(self, amount: str, account: str, narrative: str, ExternalReference: str, **kwargs) -> Response:
        """
        Deposit funds into a mobile money account.
        """
        return deposit_funds(
            APIUsername=self.api_username,
            APIPassword=self.api_password,
            Amount=amount,
            Account=account,
            Narrative=narrative,
            sandbox=self.sandbox,
            ExternalReference=ExternalReference,
            **kwargs,
        )

    def withdraw(self, amount: str, account: str, narrative: str, ExternalReference: str, NonBlocking="FALSE", ** kwargs) -> Response:
        """
        Withdraw funds from a mobile money account.
        """
        return withdraw(
            APIUsername=self.api_username,
            APIPassword=self.api_password,
            NonBlocking=NonBlocking,
            Amount=amount,
            Account=account,
            Narrative=narrative,
            sandbox=self.sandbox,
            ExternalReference=ExternalReference,
            **kwargs,
        )

    def get_transaction_status(self, tx_ref: str) -> Response:
        """
        Get the status of a transaction.
        """
        return get_transaction_status(
            APIUsername=self.api_username,
            APIPassword=self.api_password,
            TransactionReference=tx_ref,
            sandbox=self.sandbox,
        )


def parse_response(resp: Response) -> dict:
    """
    Parse the XML response from Yo! API to a dictionary.
    """
    data = xmltodict.parse(resp.content)
    return data
