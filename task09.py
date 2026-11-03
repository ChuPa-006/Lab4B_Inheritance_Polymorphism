"""Task 9 - Cooperative multiple inheritance and method resolution order."""



class Model:
    def save(self) -> None:
        print("Model.save: INSERT/UPDATE")


class TimestampMixin:
    def save(self) -> None:
        print("TimestampMixin: set updated_at")
        super().save()


class ValidateMixin:
    def save(self) -> None:
        print("ValidateMixin: validate fields")
        if not getattr(self, "valid", True):
            raise ValueError("Invoice data is invalid")
        super().save()  


class AuditMixin:
    def save(self) -> None:
        super().save()
        print("AuditMixin: write audit entry")


class OriginalValidateMixin:
    """The initial broken mixin: validation silently stops the save chain."""

    def save(self) -> None:
        print("ValidateMixin: validate fields")


class OriginalInvoice(TimestampMixin, OriginalValidateMixin, AuditMixin, Model):
    valid = True


class Invoice(TimestampMixin, ValidateMixin, AuditMixin, Model):
    valid = True


class ReorderedInvoice(TimestampMixin, AuditMixin, Model, ValidateMixin):
    valid = True


def test_original_save_chain_stops_at_validate(capsys):
    assert OriginalInvoice.__mro__ == (
        OriginalInvoice,
        TimestampMixin,
        OriginalValidateMixin,
        AuditMixin,
        Model,
        object,
    )
    OriginalInvoice().save()
    assert capsys.readouterr().out.splitlines() == [
        "TimestampMixin: set updated_at",
        "ValidateMixin: validate fields",
    ]


def test_mro_order_and_all_four_save_steps(capsys):
    assert Invoice.__mro__ == (
        Invoice,
        TimestampMixin,
        ValidateMixin,
        AuditMixin,
        Model,
        object,
    )
    Invoice().save()
    assert capsys.readouterr().out.splitlines() == [
        "TimestampMixin: set updated_at",
        "ValidateMixin: validate fields",
        "Model.save: INSERT/UPDATE",
        "AuditMixin: write audit entry",
    ]


def test_invalid_invoice_stops_before_database_and_audit(capsys):
    invoice = Invoice()
    invoice.valid = False
    try:
        invoice.save()
    except ValueError as error:
        assert str(error) == "Invoice data is invalid"
    else:
        raise AssertionError("Invalid invoice must raise ValueError")
    assert capsys.readouterr().out.splitlines() == [
        "TimestampMixin: set updated_at",
        "ValidateMixin: validate fields",
    ]


def test_reordered_bases_put_model_before_validate(capsys):
    assert ReorderedInvoice.__mro__ == (
        ReorderedInvoice,
        TimestampMixin,
        AuditMixin,
        Model,
        ValidateMixin,
        object,
    )
    ReorderedInvoice().save()
    assert capsys.readouterr().out.splitlines() == [
        "TimestampMixin: set updated_at",
        "Model.save: INSERT/UPDATE",
        "AuditMixin: write audit entry",
    ]
