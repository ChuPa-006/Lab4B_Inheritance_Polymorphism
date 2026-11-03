"""Task 7 - Immutable Money value object with safe operators."""


from dataclasses import dataclass
from functools import total_ordering


class CurrencyMismatchError(ValueError):
    pass


@total_ordering
@dataclass(frozen=True, eq=False)
class Money:
    amount: int
    currency: str

    def __post_init__(self) -> None:
        if type(self.amount) is not int:
            raise TypeError("amount must be an integer in minor units")
        normalized = self.currency.upper()
        if len(normalized) != 3 or not normalized.isalpha():
            raise ValueError("currency must be a 3-letter code")
        object.__setattr__(self, "currency", normalized)

    def _require_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                f"Cannot combine {self.currency} with {other.currency}"
            )

    def __add__(self, other: object):
        if not isinstance(other, Money):
            return NotImplemented
        self._require_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __radd__(self, other: object):
        if type(other) is int and other == 0:
            return self
        return NotImplemented

    def __mul__(self, quantity: object):
        if type(quantity) is not int:
            return NotImplemented
        return Money(self.amount * quantity, self.currency)

    def __rmul__(self, quantity: object):
        return self.__mul__(quantity)

    def __eq__(self, other: object):
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other: object):
        if not isinstance(other, Money):
            return NotImplemented
        self._require_same_currency(other)
        return self.amount < other.amount

    def __hash__(self) -> int:
        return hash((self.amount, self.currency))


def test_addition_and_currency_mismatch():
    assert Money(500, "UZS") + Money(200, "UZS") == Money(700, "UZS")
    try:
        Money(100, "USD") + Money(1, "UZS")
    except CurrencyMismatchError:
        pass
    else:
        raise AssertionError("Different currencies must not be added")


def test_integer_multiplication_works_on_both_sides():
    price = Money(500, "UZS")
    assert price * 3 == Money(1500, "UZS")
    assert 3 * price == Money(1500, "UZS")


def test_sum_works_with_default_zero_start():
    assert sum([Money(100, "UZS"), Money(200, "UZS")]) == Money(300, "UZS")


def test_equality_ordering_and_hash():
    assert Money(500, "UZS") == Money(500, "UZS")
    assert (Money(500, "UZS") == 500) is False
    assert Money(100, "UZS") < Money(200, "UZS")
    assert Money(200, "UZS") > Money(100, "UZS")
    assert len({Money(500, "UZS"), Money(500, "UZS")}) == 1


def test_ordering_different_currencies_is_rejected():
    try:
        Money(100, "USD") > Money(1, "UZS")
    except CurrencyMismatchError:
        pass
    else:
        raise AssertionError("Different currencies are not order-comparable")


def test_money_is_immutable():
    price = Money(500, "UZS")
    try:
        price.amount = 1000
    except (AttributeError, TypeError):
        pass
    else:
        raise AssertionError("Money must be immutable")
