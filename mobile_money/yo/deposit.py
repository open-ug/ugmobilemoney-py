from httpx import Response
import httpx
import xmltodict

SANDBOX_URL = "https://sandbox.yo.co.ug/services/yopaymentsdev/task.php"
PRODUCTION_URL = "https://sandbox.yo.co.ug/services/yopaymentsdev/task.php"

""" 
<?xml version="1.0" encoding="UTF-8"?>
<AutoCreate>
 <Request>
 <APIUsername></APIUsername>
 <APIPassword></APIPassword>
 <Method>acdepositfunds</Method>
 <NonBlocking></NonBlocking>
 <Amount></Amount>
 <Account></Account>
 <AccountProviderCode></AccountProviderCode>
 <Narrative></Narrative>
 <NarrativeFileName></NarrativeFileName>
 <NarrativeFileBase64></NarrativeFileBase64>
 <InternalReference></InternalReference>
 <ExternalReference></ExternalReference>
 <ProviderReferenceText></ProviderReferenceText>
 <InstantNotificationUrl></InstantNotificationUrl>
 <FailureNotificationUrl></FailureNotificationUrl>
 <AuthenticationSignatureBase64></AuthenticationSignatureBase64>
 </Request>
</AutoCreate> 
 """


def deposit_funds(
    APIUsername: str,
    APIPassword: str,
    Amount: str,
    Account: str,
    Narrative: str,
    NonBlocking: bool | None = None,
    AccountProviderCode: str | None = None,
    NarrativeFileName: str | None = None,
    NarrativeFileBase64: str | None = None,
    InternalReference: str | None = None,
    ExternalReference: str | None = None,
    ProviderReferenceText: str | None = None,
    InstantNotificationUrl: str | None = None,
    FailureNotificationUrl: str | None = None,
    AuthenticationSignatureBase64: str | None = None,
    sandbox: bool = True,
) -> Response:
    """
    Deposit funds to a mobile money account.

    Args:
        APIUsername (str): API Username.
        APIPassword (str): API Password.
        Method (str): Method.
        NonBlocking (bool): NonBlocking.
        Amount (str): Amount to be transferred.
        Account (str): Mobile money account number.
        AccountProviderCode (str): Account provider code.
        Narrative (str): Narrative.
        NarrativeFileName (str): Narrative file name.
        NarrativeFileBase64 (str): Narrative file base64.
        InternalReference (str): Internal reference.
        ExternalReference (str): External reference.
        ProviderReferenceText (str): Provider reference text.
        InstantNotificationUrl (str): Instant notification URL.
        FailureNotificationUrl (str): Failure notification URL.
        AuthenticationSignatureBase64 (str): Authentication signature base64.
    """

    BASE_URL = SANDBOX_URL if sandbox else PRODUCTION_URL

    headers = {
        "Content-Type": "text/xml",
        "Content-transfer-encoding": "text",
    }

    mandatory_fields = {
        "APIUsername": APIUsername,
        "APIPassword": APIPassword,
        "Method": "acdepositfunds",
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
        "InstantNotificationUrl": InstantNotificationUrl,
        "FailureNotificationUrl": FailureNotificationUrl,
        "AuthenticationSignatureBase64": AuthenticationSignatureBase64,
    }

    # Remove None values from optional_fields
    optional_fields = {k: v for k,
                       v in optional_fields.items() if v is not None}

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

    response = httpx.post(
        BASE_URL, headers=headers, content=data.encode("utf-8"), timeout=None
    )
    return response
