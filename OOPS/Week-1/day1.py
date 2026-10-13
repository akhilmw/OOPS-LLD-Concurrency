from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from functools import total_ordering
from types import NotImplementedType
from typing import Self


@total_ordering
@dataclass(frozen=True, init=False)
class Money:
    value: Decimal
    currency: str

    def __init__(
        self,
        value: Decimal | int | str,
        currency: str,
    ) -> None:
        if isinstance(value, (float, bool)):
            raise TypeError(
                "Money must be constructed from a Decimal, integer, or string"
            )

        try:
            normalized_value = Decimal(value)
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError("Invalid monetary value") from exc

        if not normalized_value.is_finite():
            raise ValueError("Money must have a finite value")

        if not isinstance(currency, str):
            raise TypeError("Currency must be a string")

        normalized_currency = currency.strip().upper()

        if (
            len(normalized_currency) != 3
            or not normalized_currency.isascii()
            or not normalized_currency.isalpha()
        ):
            raise ValueError(
                "Currency must contain exactly three ASCII letters"
            )

        object.__setattr__(self, "value", normalized_value)
        object.__setattr__(self, "currency", normalized_currency)

    def _ensure_same_currency(self, other: Self) -> None:
        if self.currency != other.currency:
            raise ValueError(
                f"Currency mismatch: {self.currency} and {other.currency}"
            )

    def __add__(
        self,
        other: object,
    ) -> Self | NotImplementedType:
        if not isinstance(other, Money):
            return NotImplemented

        self._ensure_same_currency(other)

        return type(self)(
            self.value + other.value,
            self.currency,
        )

    def __sub__(
        self,
        other: object,
    ) -> Self | NotImplementedType:
        if not isinstance(other, Money):
            return NotImplemented

        self._ensure_same_currency(other)

        return type(self)(
            self.value - other.value,
            self.currency,
        )

    def __mul__(
        self,
        scalar: object,
    ) -> Self | NotImplementedType:
        if isinstance(scalar, bool):
            return NotImplemented

        if not isinstance(scalar, (int, Decimal)):
            return NotImplemented

        return type(self)(
            self.value * Decimal(scalar),
            self.currency,
        )

    def __rmul__(
        self,
        scalar: object,
    ) -> Self | NotImplementedType:
        return self * scalar

    def __lt__(
        self,
        other: object,
    ) -> bool | NotImplementedType:
        if not isinstance(other, Money):
            return NotImplemented

        self._ensure_same_currency(other)

        return self.value < other.value

    def __str__(self) -> str:
        return f"{self.value} {self.currency}"

    def __repr__(self) -> str:
        return (
            f"Money(value={self.value!r}, "
            f"currency={self.currency!r})"
        )

class BankAccount:
    def __init__(
        self,
        account_id: str,
        owner: str,
        currency: str,
    ):

        self._account

    @property
    def balance(self) -> Money:
        ...

    @property
    def transactions(self) -> tuple:
        ...

    def deposit(self, amount: Money) -> None:
        ...

    def withdraw(self, amount: Money) -> None:
        ...

    def transfer_to(
        self,
        destination: "BankAccount",
        amount: Money,
    ) -> None:
        ...