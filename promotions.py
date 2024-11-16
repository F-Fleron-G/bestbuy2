from abc import ABC, abstractmethod


class Promotion(ABC):
    """
    A base class for all promotions. This sets up the general structure
    for any type of promotion we want to apply to products.
    """

    def __init__(self, name: str):
        """
        Initializes the promotion with a name.

        Args:
            name (str): The name of the promotion.
        """
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """
        Applies the promotion to a product and returns the discounted price.

        Args:
            product: The product being purchased.
            quantity: The quantity being purchased.

        Returns:
            float: The price after applying the promotion.
        """
        pass

    def __str__(self):
        """
        Returns the name of the promotion when converting the object to a string.

        Returns:
            str: The name of the promotion.
        """
        return self.name


class PercentDiscount(Promotion):
    """
    A promotion that applies a percentage discount to the product price.
    """

    def __init__(self, name: str, percent: float):
        """
        Initializes the percentage discount promotion.

        Args:
            name (str): The name of the promotion.
            percent (float): The discount percentage to apply.
        """
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        """
        Applies the percentage discount to the product price.

        Args:
            product: The product being purchased.
            quantity: The quantity being purchased.

        Returns:
            float: The total price after the discount is applied.
        """
        discount = (self.percent / 100) * product.price
        return (product.price - discount) * quantity


class SecondHalfPrice(Promotion):
    """
    A promotion where the second item is half price.
    """

    def __init__(self, name: str):
        """
        Initializes the second half price promotion.

        Args:
            name (str): The name of the promotion.
        """
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        """
        Calculates the total price with the second item at half price.

        Args:
            product: The product being purchased.
            quantity: The quantity being purchased.

        Returns:
            float: The total price with the discount applied.
        """
        full_price_count = quantity // 2 + quantity % 2
        half_price_count = quantity // 2
        return (full_price_count * product.price) + (half_price_count * product.price * 0.5)


class ThirdOneFree(Promotion):
    """
    A promotion where every third item is free.
    """

    def __init__(self, name: str):
        """
        Initializes the buy 2, get 1 free promotion.

        Args:
            name (str): The name of the promotion.
        """
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        """
        Calculates the total price with every third item being free.

        Args:
            product: The product being purchased.
            quantity: The quantity being purchased.

        Returns:
            float: The total price with the discount applied.
        """
        full_price_count = quantity - (quantity // 3)
        return full_price_count * product.price
