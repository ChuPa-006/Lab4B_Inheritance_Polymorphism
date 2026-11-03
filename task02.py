"""Task 2 - Abstract notifier with shared notify logic."""


from abc import ABC, abstractmethod


class Notifier(ABC):
    max_length = 1000

    @abstractmethod
    def send(self, recipient: str, text: str) -> None:
        """Send a message through the concrete channel."""

    def notify(self, recipient: str, text: str) -> None:
        self.send(recipient, text[: self.max_length])


class TelegramNotifier(Notifier):
    max_length = 4096

    def send(self, recipient: str, text: str) -> None:
        print(f"telegram -> {recipient}: {text}")


class BrokenTelegramNotifier(Notifier):
    """Reproduces the original typo to show abstract-class protection."""

    def sned(self, recipient: str, text: str) -> None:
        print(f"telegram -> {recipient}: {text}")



class SmsNotifier(Notifier):
    max_length = 160

    def __init__(self) -> None:
        self.sent_messages: list[tuple[str, str]] = []

    def send(self, recipient: str, text: str) -> None:
        self.sent_messages.append((recipient, text))


def test_notifier_is_abstract():
    try:
        Notifier()
    except TypeError:
        pass
    else:
        raise AssertionError("Notifier must not be instantiated directly")


def test_typo_in_telegram_method_is_caught_at_instantiation():
    try:
        BrokenTelegramNotifier()
    except TypeError:
        pass
    else:
        raise AssertionError("The misspelled send method must leave the class abstract")


def test_telegram_notifier_sends_message(capsys):
    TelegramNotifier().notify("@ali", "Exam at 10:00")
    assert "telegram -> @ali: Exam at 10:00" in capsys.readouterr().out



def test_sms_notify_trims_to_its_own_limit():
    sms = SmsNotifier()
    sms.notify("+998901234567", "x" * 300)
    recipient, sent_text = sms.sent_messages[0]
    assert recipient == "+998901234567"
    assert len(sent_text) == 160


def test_telegram_uses_telegram_limit(capsys):
    text = "x" * 4200
    TelegramNotifier().notify("@ali", text)
    output = capsys.readouterr().out
    sent_text = output.split(": ", 1)[1].rstrip("\n")
    assert len(sent_text) == 4096


