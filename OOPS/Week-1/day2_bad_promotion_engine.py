"""Week 1: Strategy pattern exercise.

Focus only on:
1. Replacing Checkout's if/elif chain with the Strategy pattern.
2. Implementing the strategy contract first with an ABC.
3. Replacing the ABC with a Protocol to compare the two approaches.

Money, currency rules, cart validation, BOGO, and other production concerns are
intentionally excluded. Prices are simple floats for this focused exercise.

Round 1 — ABC
-------------
1. Create DiscountStrategy(ABC) with an abstract calculate(subtotal) method.
2. Implement NoDiscount, TenPercentDiscount, and FlatDiscount strategies.
3. Give Checkout a strategy through its constructor.
4. Remove every discount-related if/elif from Checkout.
5. Make the assertions at the bottom pass without changing their expected values.

Target usage:

    checkout = Checkout(TenPercentDiscount())
    result = checkout.calculate(cart)

Round 2 — Protocol
------------------
1. Replace DiscountStrategy(ABC) with DiscountStrategy(Protocol).
2. Remove explicit inheritance from the concrete strategies.
3. Confirm that Checkout and the assertions still work.
4. Add LoyaltyDiscount without changing Checkout.

The lesson: Checkout should depend on a behavior contract, not on the names of
specific discount types.
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class Product:
    name: str
    price: float


@dataclass(frozen=True)
class CartItem:
    product: Product
    quantity: int


class ShoppingCart:
    def __init__(self) -> None:
        self._items: list[CartItem] = []

    def add(self, product: Product, quantity: int) -> None:
        self._items.append(CartItem(product, quantity))

    def subtotal(self) -> float:
        return sum(item.product.price * item.quantity for item in self._items)


@dataclass(frozen=True)
class CheckoutResult:
    subtotal: float
    discount: float
    total: float


class DiscountStrategy(ABC):

    @abstractmethod
    def calculate(self, subtotal : float) -> float:
        pass

class TenPercentDiscount(DiscountStrategy):

    def calculate(self, subtotal):
        return subtotal * 0.1

class FlatDiscount(DiscountStrategy):

    def __init__(self, amount : float):

        self.amount = amount

    def calculate(self, subtotal):
        return min(self.amount, subtotal)
        
class NoDiscount(DiscountStrategy):
    def calculate(self, subtotal: float) -> float:
        return 0.0

class Checkout:
    """This implementation works, but it must be refactored."""

    def __init__(self, discount_kind: DiscountStrategy) -> None:
        self._discount_kind = discount_kind

    def calculate(self, cart: ShoppingCart) -> CheckoutResult:
        subtotal = cart.subtotal()

        discount = self._discount_kind.calculate(subtotal)

        return CheckoutResult(
            subtotal=subtotal,
            discount=discount,
            total=subtotal - discount,
        )


def build_cart() -> ShoppingCart:
    cart = ShoppingCart()
    cart.add(Product("Keyboard", 80.0), 1)
    cart.add(Product("Mouse", 20.0), 2)
    return cart


if __name__ == "__main__":
    cart = build_cart()

    no_discount = Checkout(NoDiscount()).calculate(cart)
    percentage = Checkout(TenPercentDiscount()).calculate(cart)
    flat = Checkout(FlatDiscount(15.0)).calculate(cart)

    assert no_discount == CheckoutResult(120.0, 0.0, 120.0)
    assert percentage == CheckoutResult(120.0, 12.0, 108.0)
    assert flat == CheckoutResult(120.0, 15.0, 105.0)

    print("Starter behavior verified. Now replace the conditional with strategies.")
