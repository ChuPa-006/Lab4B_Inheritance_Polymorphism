"""Task 10 - One registry maps external strings to payment classes."""


from task01 import (
    BankTransfer,
    CardPayment,
    CashPayment,
    ClickPayment,
    PaymePayment,
    PaymentMethod,
)


class UnknownPaymentMethodError(ValueError):
    pass


PAYMENT_METHODS: dict[str, type[PaymentMethod]] = {
    "card": CardPayment,
    "click": ClickPayment,
    "payme": PaymePayment,
    "cash": CashPayment,
    "bank_transfer": BankTransfer,
}


def create_payment_method(name: str) -> PaymentMethod:
    normalized_name = name.strip().casefold()
    payment_class = PAYMENT_METHODS.get(normalized_name)
    if payment_class is None:
        supported = ", ".join(sorted(PAYMENT_METHODS))
        raise UnknownPaymentMethodError(
            f"Unknown payment method {name!r}. Supported methods: {supported}"
        )
    return payment_class()


def test_registry_creates_each_payment_type():
    assert isinstance(create_payment_method("card"), CardPayment)
    assert isinstance(create_payment_method("click"), ClickPayment)
    assert isinstance(create_payment_method("payme"), PaymePayment)
    assert isinstance(create_payment_method("cash"), CashPayment)
    assert isinstance(create_payment_method("bank_transfer"), BankTransfer)


def test_registry_normalises_whitespace_and_case():
    assert isinstance(create_payment_method(" Payme "), PaymePayment)
    assert isinstance(create_payment_method("PAYME"), PaymePayment)
    assert isinstance(create_payment_method("payme"), PaymePayment)


def test_unknown_name_lists_supported_names():
    try:
        create_payment_method("crypto")
    except UnknownPaymentMethodError as error:
        message = str(error)
        assert "card" in message
        assert "click" in message
        assert "payme" in message
        assert "bank_transfer" in message
    else:
        raise AssertionError("An unknown name must raise UnknownPaymentMethodError")
