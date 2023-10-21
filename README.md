# <img src="https://flagcdn.com/w40/ug.png"> UG MOBILE MONEY

UG Mobile Money is a python library for making mobile money transactions in Uganda. It currently supports MTN MOMO.

UG Mobile Money provides a simple interface for making mobile money transactions in a way that is similar to what the official MTN Mobile Money API provides but in a more pythonic and simple way. This makes it easy for beginners to get started and also for experienced developers who have been using the official API shift.

The library also handles other underlying functions like encryption, Authorization and regenerating access tokens. This makes it easy for developers to focus on the business logic of their applications and not worry about the underlying details.

The library utitlizes the Official MTN Mobile Money API. The API is documented [here](https://momodeveloper.mtn.com).


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install UG Mobile Money.

```sh
pip install ugmobilemoney
```

After installing it you can now import the package in your project.

```python
from mobile_money.momo import Collection, Disbursment
```

## Usage

This library is currently in development and only supports MTN MOMO. It supports the following operations:

- Collection
  - Request to pay
- Disbursment
  - Transfer

> **Note:** You need to have an account with MTN MOMO and have your API user ID and API key. You can get these from the [MTN MOMO Developer Portal](https://momodeveloper.mtn.com). If your in sandbox environment, we provide utils for creation of API user ID and API key.

### Collection

The UG Mobile Money library provides a `Collection` class that can be used to carry out operations or call the MOMO APIs provided under the collection Products.

You access it from the `mobile_money.momo` module.

```py
from mobile_money.momo import Collection


collection = Collection(
    subscription_key=SUBSCRIPTION_KEY,
    api_user=API_USER,
    api_key=API_KEY,
    callback_url="http://mydomain.com/webhooks/mtn/",
    production=False,
)
```

### Request to Pay

Request to pay is a service that allows a merchant to receive payments on from a customer. This is typically used when a customer is paying for goods or services. The `collect()` method is used to initiate a request to pay transaction.

```py
from mobile_money.momo import Collection
from mobile_money import generate_uuid

collection = Collection(
    subscription_key=SUBSCRIPTION_KEY,
    api_user=API_USER,
    api_key=API_KEY,
    callback_url="http://mydomain.com/webhooks/mtn/",
    production=False,
)

transaction_reference = generate_uuid()
# Request to pay
response = COLLECTION.collect(
    amount="100",
    phone_number="256772123456",
    currency="UGX",
    external_id="external id",
    reference_id=transaction_reference,
    payee_note="test",
    payer_message="test",
)

print(response)

# >>> <Response [202 Accepted]>
```

### Disbursment

The UG Mobile Money library provides a `Disbursment` class that can be used to carry out operations or call the MOMO APIs provided under the Disbursment Products.

You access it from the `mobile_money.momo` module.

```py
from mobile_money.momo import Disbursment

DISBURSEMENT = Disbursment(
    subscription_key=SUBSCRIPTION_KEY,
    api_user=API_USER,
    api_key=API_KEY,
    callback_url="http://mydomain.com/webhooks/mtn/",
    production=False,
)
```

### Transfer

Transfer is a service that allows a merchant to transfer money from their account to a customer's account. This is typically used when a customer is receiving money for goods or services. The `transfer()` method is used to initiate a transfer transaction.

```py
from mobile_money.momo import Disbursment
from mobile_money import generate_uuid

DISBURSEMENT = Disbursment(
    subscription_key=SUBSCRIPTION_KEY,
    api_user=API_USER,
    api_key=API_KEY,
    callback_url="http://mydomain.com/webhooks/mtn/",
    production=False,
)

transaction_reference = generate_uuid()

# Transfer
response = DISBURSEMENT.transfer(
    amount="100",
    phone_number="256772123456",
    currency="UGX",
    external_id="external id",
    reference_id=transaction_reference,
    payee_note="test",
    payer_message="test",
)

print(response)

# >>> <Response [202 Accepted]>
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License (MIT). Please see [License File](LICENSE) for more information.