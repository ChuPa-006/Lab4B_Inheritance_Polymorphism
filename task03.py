"""Task 3 - Subscription pricing with one VAT calculation."""



class Subscription:
    VAT_PERCENT = 12

    def __init__(self, user: str, months: int) -> None:
        self.user = user
        self.months = months
        self.base_monthly = 50_000

    def net(self) -> int:
        return self.base_monthly * self.months

    def price(self) -> int:
        net_price = self.net()
        return net_price * (100 + self.VAT_PERCENT) // 100


class StudentSubscription(Subscription):
    def net(self) -> int:
        return super().net() // 2


class FamilySubscription(Subscription):
    def __init__(self, user: str, months: int, members: int) -> None:
        super().__init__(user, months)
        if members < 1:
            raise ValueError("A family subscription must have at least one member")
        self.members = members

    def net(self) -> int:
        extra_members = self.members - 1
        extra_cost = 20_000 * extra_members * self.months
        return super().net() + extra_cost


def test_standard_subscription_for_three_months():
    assert Subscription("Ali", 3).price() == 168_000


def test_student_subscription_gets_half_off_net_price_then_vat():
    assert StudentSubscription("Ali", 3).price() == 84_000


def test_family_subscription_for_four_members_for_three_months():
    assert FamilySubscription("Ali", 3, 4).price() == 369_600


def test_vat_change_applies_to_all_subscription_types():
    original = Subscription.VAT_PERCENT
    try:
        Subscription.VAT_PERCENT = 15
        assert Subscription("Ali", 1).price() == 57_500
        assert StudentSubscription("Ali", 1).price() == 28_750
        assert FamilySubscription("Ali", 1, 2).price() == 80_500
    finally:
        Subscription.VAT_PERCENT = original

