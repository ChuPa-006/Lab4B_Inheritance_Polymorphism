"""Task 4 - Append-only audit log using composition."""



from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class AuditEntry:
    user: str
    action: str


class AuditLog:
    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def record(self, user: str, action: str) -> None:
        self._entries.append(AuditEntry(user, action))

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self) -> Iterator[AuditEntry]:
        return iter(tuple(self._entries))

    def last(self, n: int) -> tuple[AuditEntry, ...]:
        if n < 0:
            raise ValueError("n must be non-negative")
        if n == 0:
            return ()
        return tuple(self._entries[-n:])


def test_audit_log_records_and_supports_len_and_iteration():
    log = AuditLog()
    log.record("admin", "approve_loan#77")
    log.record("ali", "login")
    assert len(log) == 2
    assert [(entry.user, entry.action) for entry in log] == [
        ("admin", "approve_loan#77"),
        ("ali", "login"),
    ]


def test_last_returns_the_requested_number_of_entries():
    log = AuditLog()
    log.record("a", "one")
    log.record("b", "two")
    log.record("c", "three")
    assert [entry.action for entry in log.last(2)] == ["two", "three"]
    assert log.last(0) == ()


def test_audit_entries_are_immutable():
    log = AuditLog()
    log.record("admin", "approve")
    entry = log.last(1)[0]
    try:
        entry.action = "erase" 
    except (AttributeError, TypeError):
        pass
    else:
        raise AssertionError("AuditEntry must be immutable")


def test_audit_log_does_not_expose_list_mutators():
    log = AuditLog()
    assert not hasattr(log, "clear")
    assert not hasattr(log, "sort")
    assert not hasattr(log, "pop")
