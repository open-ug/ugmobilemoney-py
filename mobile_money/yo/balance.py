from httpx import Response
import httpx

SANDBOX_URL = "https://sandbox.yo.co.ug/services/yopaymentsdev/task.php"
PRODUCTION_URL = "https://paymentsapi1.yo.co.ug/ybs/task.php"


"""<?xml version="1.0" encoding="UTF-8"?> 
<AutoCreate> 
 <Request> 
 <APIUsername></APIUsername> 
 <APIPassword></APIPassword> 
 <Method>acacctbalance</Method> 
 </Request> 
</AutoCreate> """


def get_account_balance(
    APIUsername: str,
    APIPassword: str,
    sandbox: bool = True,
) -> Response:
    """
    Deposit funds to a mobile money account.

    Args:
        APIUsername (str): API Username.
        APIPassword (str): API Password.
    """

    BASE_URL = SANDBOX_URL if sandbox else PRODUCTION_URL

    headers = {
        "Content-Type": "text/xml",
        "Content-transfer-encoding": "text",
    }

    mandatory_fields = {
        "APIUsername": APIUsername,
        "APIPassword": APIPassword,
        "Method": "acacctbalance",
    }

    data = """<?xml version="1.0" encoding="UTF-8"?>
    <AutoCreate>
        <Request>
        """
    for key, value in mandatory_fields.items():
        data += f"<{key}>{value}</{key}>"
    data += """
        </Request>
    </AutoCreate>
    """

    response = httpx.post(
        BASE_URL, headers=headers, content=data.encode("utf-8"), timeout=None
    )
    return response
