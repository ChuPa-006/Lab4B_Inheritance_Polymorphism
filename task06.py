"""Task 6 - Duck typing and a Writable Protocol."""

import io
from typing import Iterable, Protocol


class Writable(Protocol):
    def write(self, data: bytes) -> int:
        ...


def export_report(rows: Iterable[Iterable[object]], target: Writable) -> None:
    for row in rows:
        target.write((",".join(map(str, row)) + "\n").encode())


class S3Upload:
    def __init__(self, bucket: str, key: str) -> None:
        self.bucket = bucket
        self.key = key
        self.parts: list[bytes] = []

    def write(self, data: bytes) -> int: 
        self.parts.append(data)
        return len(data)


class FakeWriter:
    def __init__(self) -> None:
        self.data = bytearray()

    def write(self, data: bytes) -> int:
        self.data.extend(data)
        return len(data)


def test_export_to_bytesio():
    target = io.BytesIO()
    export_report([["Ali", 20], ["Sara", 21]], target)
    assert target.getvalue() == b"Ali,20\nSara,21\n"


def test_export_to_s3_upload():
    target = S3Upload("reports", "students.csv")
    export_report([["Ali", 20], ["Sara", 21]], target)
    assert b"".join(target.parts) == b"Ali,20\nSara,21\n"


def test_export_to_an_unrelated_fake_writer():
    target = FakeWriter()
    export_report([["course", "grade"]], target)
    assert bytes(target.data) == b"course,grade\n"


def test_export_accepts_an_empty_report():
    target = FakeWriter()
    export_report([], target)
    assert target.data == bytearray()

    