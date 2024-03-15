from httpx import Response
import httpx
# import xmltodict

SANDBOX_URL = "https://sandbox.yo.co.ug/services/yopaymentsdev/task.php"
PRODUCTION_URL = "https://paymentsapi1.yo.co.ug/ybs/task.php"


"""
Below is the format of the XML request: 
<?xml version="1.0" encoding="UTF-8"?> 
<AutoCreate> 
 <Request> 
 <APIUsername></APIUsername> 
 <APIPassword></APIPassword> 
 <Method>actransactioncheckstatus</Method> 
 <TransactionReference></TransactionReference> 
 <PrivateTransactionReference></PrivateTransactionReference> 
 <DepositTransactionType></DepositTransactionType> 
 </Request> 
</AutoCreate>
"""


def get_transaction_status(
    APIUsername: str,
    APIPassword: str,
    TransactionReference: str = None,
    PrivateTransactionReference: str = None,
    DepositTransactionType: str = None,
    sandbox: bool = True,
) -> Response:
    BASE_URL = SANDBOX_URL if sandbox else PRODUCTION_URL
    headers = {
        "Content-Type": "text/xml",
        "Content-transfer-encoding": "text",
    }

    mandatory_fields = {
        "APIUsername": APIUsername,
        "APIPassword": APIPassword,
        "Method": "actransactioncheckstatus",
    }

    optional_fields = {
        "TransactionReference": TransactionReference,
        "PrivateTransactionReference": PrivateTransactionReference,
        "DepositTransactionType": DepositTransactionType,
    }

    optional_fields = {k: v for k,
                       v in optional_fields.items() if v is not None}

    data = {**mandatory_fields, **optional_fields}

    data = """<?xml version="1.0" encoding="UTF-8"?>
    <AutoCreate>
        <Request>
        """
    for key, value in mandatory_fields.items():
        data += f"<{key}>{value}</{key}>"
    for key, value in optional_fields.items():
        data += f"<{key}>{value}</{key}>"
    data += """
        </Request>
    </AutoCreate>
    """

    response = httpx.post(BASE_URL, data=data, headers=headers)
    return response
