"""Task 1 - Payment methods and polymorphic Checkout."""


from abc import ABC, abstractmethod



class PaymentMethod(ABC):
    @abstractmethod
    def fee(self, amount: int) -> int:
        """Return the fee in sum."""

    @property
    @abstractmethod
    def refundable(self) -> bool:
        """Whether this payment can be refunded."""


class CardPayment(PaymentMethod):
    def fee(self, amount: int) -> int:
        return amount * 15 // 1000  # 1.5%

    @property
    def refundable(self) -> bool:
        return True


class ClickPayment(PaymentMethod):
    def fee(self, amount: int) -> int:
        return amount * 10 // 1000  # 1%

    @property
    def refundable(self) -> bool:
        return True


class PaymePayment(PaymentMethod):
    def fee(self, amount: int) -> int:
        return amount * 10 // 1000 

    @property
    def refundable(self) -> bool:
        return True


class CashPayment(PaymentMethod):
    def fee(self, amount: int) -> int:
        return 0

    @property
    def refundable(self) -> bool:
        return False


class BankTransfer(PaymentMethod):
    def fee(self, amount: int) -> int:
        return 5_000

    @property
    def refundable(self) -> bool:
        return True


class Checkout:
    def pay(self, method: PaymentMethod, amount: int) -> dict[str, int | bool]:
        return {
            "charged": amount + method.fee(amount),
            "refundable": method.refundable,
        }


def test_card_payment_fee_and_refundability():
    assert Checkout().pay(CardPayment(), 100_000) == {
        "charged": 101_500,
        "refundable": True,
    }


def test_click_and_payme_have_independent_classes_and_same_current_rule():
    checkout = Checkout()
    assert checkout.pay(ClickPayment(), 100_000) == {
        "charged": 101_000,
        "refundable": True,
    }
    assert checkout.pay(PaymePayment(), 100_000) == {
        "charged": 101_000,
        "refundable": True,
    }
    assert type(ClickPayment()) is not type(PaymePayment())


def test_cash_has_no_fee_and_is_not_refundable():
    assert Checkout().pay(CashPayment(), 100_000) == {
        "charged": 100_000,
        "refundable": False,
    }


def test_bank_transfer_uses_fixed_fee_without_checkout_changes():
    assert Checkout().pay(BankTransfer(), 100_000) == {
        "charged": 105_000,
        "refundable": True,
    }


