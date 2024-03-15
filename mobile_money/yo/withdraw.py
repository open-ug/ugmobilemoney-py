from httpx import Response
import httpx
# import xmltodict

SANDBOX_URL = "https://sandbox.yo.co.ug/services/yopaymentsdev/task.php"
PRODUCTION_URL = "https://paymentsapi1.yo.co.ug/ybs/task.php"


def withdraw(
    APIUsername: str,
    APIPassword: str,
    NonBlocking: str,
    Amount: str,
    Account: str,
    Narrative: str,
    AccountProviderCode=None,
    TransactionLimitAccountIdentifier=None,
    NarrativeFileName=None,
    NarrativeFileBase64=None,
    InternalReference=None,
    ExternalReference=None,
    ProviderReferenceText=None,
    PublicKeyAuthenticationNonce=None,
    PublicKeyAuthenticationSignatureBase64=None,
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
        "Method": "acwithdrawfunds",
        "Amount": Amount,
        "Account": Account,
        "Narrative": Narrative,
    }

    optional_fields = {
        "NonBlocking": NonBlocking,
        "AccountProviderCode": AccountProviderCode,
        "NarrativeFileName": NarrativeFileName,
        "NarrativeFileBase64": NarrativeFileBase64,
        "InternalReference": InternalReference,
        "ExternalReference": ExternalReference,
        "ProviderReferenceText": ProviderReferenceText,
        "PublicKeyAuthenticationNonce": PublicKeyAuthenticationNonce,
        "PublicKeyAuthenticationSignatureBase64": PublicKeyAuthenticationSignatureBase64,
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

    respons = httpx.post(
        BASE_URL, headers=headers, content=data.encode("utf-8"), timeout=None
    )
    return respons
