import pytest
from products import Product


def test_create_product_success():
    """Tests creating a valid product works."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    assert product.is_active()


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
    product = Product("MacBook Air M2", price=1450, quantity=1)
    product.set_quantity(0)
    assert product.get_quantity() == 0
    assert not product.is_active()


def test_product_purchase_modifies_quantity_and_returns_total_price():
    """Tests purchasing a valid quantity reduces stock and returns the correct total price."""
    product = Product("MacBook Air M2", price=1450, quantity=10)
    total_price = product.buy(2)
    assert total_price == 1450 * 2
    assert product.get_quantity() == 8


def test_product_purchase_larger_quantity_than_exists():
    """Tests buying a larger quantity than in stock raises a ValueError."""
    product = Product("MacBook Air M2", price=1450, quantity=5)
    with pytest.raises(ValueError):
        product.buy(10)
