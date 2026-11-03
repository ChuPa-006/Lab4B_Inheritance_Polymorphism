"""Task 5 - Employee role composition and role history."""


from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


class Role(ABC):
    @abstractmethod
    def monthly_pay(self) -> int:
        """Calculate monthly pay for this role."""


@dataclass(frozen=True)
class LecturerRole(Role):
    hours: int

    def monthly_pay(self) -> int:
        return self.hours * 120_000


@dataclass(frozen=True)
class HeadRole(Role):
    salary: int

    def monthly_pay(self) -> int:
        return self.salary + 3_000_000


class Employee:
    def __init__(
        self,
        emp_id: int,
        name: str,
        role: Role,
        start_date: date = date.min,
    ) -> None:
        self.emp_id = emp_id
        self.name = name
        self.role = role
        self.role_history: list[tuple[Role, date]] = [(role, start_date)]

    def change_role(self, new_role: Role, start_date: date) -> None:
        latest_start = self.role_history[-1][1]
        if start_date <= latest_start:
            raise ValueError("A new role must start after the current role's start date")
        self.role = new_role
        self.role_history.append((new_role, start_date))

    def monthly_pay(self, as_of: date | None = None) -> int:
        if as_of is None:
            return self.role.monthly_pay()

        applicable_roles = [
            role for role, start_date in self.role_history if start_date <= as_of
        ]
        if not applicable_roles:
            raise ValueError("No role was active on the requested date")
        return applicable_roles[-1].monthly_pay()


def test_promotion_keeps_same_employee_object_and_id():
    employee = Employee(77, "Ali", LecturerRole(hours=80), date(2026, 1, 1))
    original_id = employee.emp_id
    employee.change_role(HeadRole(salary=14_000_000), date(2026, 11, 1))
    assert employee.emp_id == original_id
    assert employee.name == "Ali"
    assert employee.monthly_pay() == 17_000_000
    assert len(employee.role_history) == 2


def test_historical_payroll_uses_role_active_on_that_date():
    employee = Employee(77, "Ali", LecturerRole(hours=80), date(2026, 1, 1))
    employee.change_role(HeadRole(salary=14_000_000), date(2026, 11, 1))
    assert employee.monthly_pay(as_of=date(2026, 10, 1)) == 9_600_000
    assert employee.monthly_pay(as_of=date(2026, 11, 1)) == 17_000_000


def test_monthly_pay_delegates_to_role_without_role_type_branches():
    lecturer = Employee(1, "Sara", LecturerRole(hours=10))
    head = Employee(2, "Omar", HeadRole(salary=10_000_000))
    assert lecturer.monthly_pay() == 1_200_000
    assert head.monthly_pay() == 13_000_000


def test_role_change_requires_a_later_start_date():
    employee = Employee(77, "Ali", LecturerRole(hours=80), date(2026, 1, 1))
    try:
        employee.change_role(HeadRole(salary=14_000_000), date(2025, 12, 31))
    except ValueError:
        pass
    else:
        raise AssertionError("Role history dates must be chronological")
