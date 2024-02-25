from httpx import Response
import httpx
# import xmltodict

SANDBOX_URL = "https://sandbox.yo.co.ug/services/yopaymentsdev/task.php"
PRODUCTION_URL = "https://sandbox.yo.co.ug/services/yopaymentsdev/task.php"

""" 
<?xml version="1.0" encoding="UTF-8"?> 
<AutoCreate> 
 <Request> 
 <APIUsername></APIUsername> 
 <APIPassword></APIPassword> 
 <Method>acwithdrawfunds</Method> 
 <NonBlocking></NonBlocking> 
 <Amount></Amount> 
 <Account></Account> 
 <AccountProviderCode></AccountProviderCode> 
 <TransactionLimitAccountIdentifier></TransactionLimitAccountIdentifier> 
 <Narrative></Narrative> 
 <NarrativeFileName></NarrativeFileName> 
 <NarrativeFileBase64></NarrativeFileBase64> 
 <InternalReference></InternalReference> 
 <ExternalReference></ExternalReference> 
 <ProviderReferenceText></ProviderReferenceText> 
 <PublicKeyAuthenticationNonce></PublicKeyAuthenticationNonce> 
 <PublicKeyAuthenticationSignatureBase64></PublicKeyAuthenticationSignatureBase64> 
 </Request> 
</AutoCreate>
 """


def withdraw(
    APIUsername: str,
    APIPassword: str,
    NonBlocking: str,
    Amount: str,
    Account: str,
    AccountProviderCode: str,
    TransactionLimitAccountIdentifier: str,
    Narrative: str,
    NarrativeFileName: str,
    NarrativeFileBase64: str,
    InternalReference: str,
    ExternalReference: str,
    ProviderReferenceText: str,
    PublicKeyAuthenticationNonce: str,
    PublicKeyAuthenticationSignatureBase64: str,
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

    response = httpx.post(
        BASE_URL, headers=headers, content=data.encode("utf-8"), timeout=None
    )
    return response
