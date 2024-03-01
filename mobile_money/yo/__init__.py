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

    def __init__(
        self,
        api_username: str,
        api_password: str,
        tx_ref: str = None,
        sandbox: bool = False,
    ):
        self.api_username = api_username
        self.api_password = api_password
        self.tx_ref = tx_ref
        self.sandbox = sandbox

    def get_status(self):
        """
        Get the status of a transaction.
        """
        if self.tx_ref is None:
            raise ValueError("Transaction reference is required.")

        return get_transaction_status(
            APIUsername=self.api_username,
            APIPassword=self.api_password,
            TransactionReference=self.tx_ref,
            sandbox=self.sandbox,
        )


class Yo:
    """
    Yo class for mobile money transactions.
    """
    tx_ref = None

    def __init__(self, api_username: str, api_password: str, sandbox: bool = False):
        self.api_username = api_username
        self.api_password = api_password
        self.sandbox = sandbox

    def deposit(self, amount: str, account: str, narrative: str, **kwargs) -> Response:
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
            **kwargs,
        )

    def withdraw(self, amount: str, account: str, narrative: str, **kwargs) -> Response:
        """
        Withdraw funds from a mobile money account.
        """
        return withdraw(
            APIUsername=self.api_username,
            APIPassword=self.api_password,
            Amount=amount,
            Account=account,
            Narrative=narrative,
            sandbox=self.sandbox,
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


yo = Yo(api_username="90003123107", api_password="4154388903", sandbox=True)

response = yo.deposit(
    amount="10000", account="256704203035", narrative="9858989489")

print(response.text)
