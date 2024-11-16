import pytest
import products
import promotions
from products import Product  # Import Product directly


def test_create_product_success():
    """Tests creating a valid product works."""
    macbook = Product("MacBook Air M2", price=1450, quantity=100)
    assert macbook.name == "MacBook Air M2"
    assert macbook.price == 1450
    assert macbook.quantity == 100
    assert macbook.is_active()


def test_create_product_invalid_name():
    """Tests creating a product without a name raises a ValueError."""
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)


def test_create_product_negative_price():
    """Tests creating a product with a negative price raises a ValueError."""
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_product_becomes_inactive_when_quantity_zero():
    """Tests a product becomes inactive when its quantity reaches zero."""
    macbook = Product("MacBook Air M2", price=1450, quantity=1)
    macbook.set_quantity(0)
    assert macbook.get_quantity() == 0
    assert not macbook.is_active()


def test_product_purchase_modifies_quantity_and_returns_total_price():
    """
    Tests purchasing a valid quantity reduces stock and returns the
    correct total price.
    """
    macbook = Product("MacBook Air M2", price=1450, quantity=10)
    total_price = macbook.buy(2)
    assert total_price == 1450 * 2
    assert macbook.get_quantity() == 8


def test_product_purchase_larger_quantity_than_exists():
    """Tests buying a larger quantity than in stock raises a ValueError."""
    macbook = Product("MacBook Air M2", price=1450, quantity=5)
    with pytest.raises(ValueError):
        macbook.buy(10)


def test_promotions_apply_correctly():
    """Tests that promotions are applied correctly to products."""
    macbook = Product("MacBook Air M2", price=1450, quantity=100)
    earbuds = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    windows_license = products.NonStockedProduct("Windows License", price=125)
    shipping = products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)

    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    macbook.set_promotion(second_half_price)
    earbuds.set_promotion(third_one_free)
    windows_license.set_promotion(thirty_percent)

    assert macbook.buy(2) == 1450 + (1450 * 0.5)
    assert earbuds.buy(3) == 250 * 2
    assert windows_license.buy(1) == 125 * 0.7
    with pytest.raises(ValueError):
        shipping.buy(2)


product_list = [
    Product("MacBook Air M2", price=1450, quantity=100),
    Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    Product("Google Pixel 7", price=500, quantity=250),
    products.NonStockedProduct("Windows License", price=125),
    products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
]

for product in product_list:
    print(product.show())
