RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


class Product:
    """
    Represents a product sold in the store.

    Attributes:
        name (str): The product name.
        price (float): The price per unit (must be positive).
        quantity (int): How many items are in stock (zero or higher).
        active (bool): Indicates if the product is still for sale.
    """
    def __init__(self, name: str, price: float, quantity: int):
        """
        Initializes a new product instance.

        Args:
            name (str): The product name.
            price (float): The price per unit (must be positive).
            quantity (int): How many items are in stock (zero or higher).

        Raises:
            ValueError: If name is empty or price or quantity is negative.
        """
        if not name or price < 0 or quantity < 0:
            raise ValueError(f"{RED}INVALID PRODUCT DETAILS! The name can't be empty, "
                             f"price must be positive, and quantity can't be negative.{RESET}")
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self) -> float:
        """Returns the number of items in stock."""
        return self.quantity

    def set_quantity(self, quantity: int):
        """
        Updates the stock quantity. If quantity hits zero, it deactivates the product.

        Args:
            quantity (int): The updated stock level (non-negative).

        Raises:
            ValueError: If quantity is negative.
        """
        if quantity < 0:
            raise ValueError(f"{RED}ATTENTION! Quantity can't be negative.{RESET}")
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """Returns True if the product is active (still for sale)."""
        return self.active

    def activate(self):
        """Marks the product as active."""
        self.active = True

    def deactivate(self):
        """Marks the product as inactive (out of stock or discontinued)."""
        self.active = False

    def show(self) -> str:
        """Returns a formatted string describing the product's details."""
        return (f"{YELLOW}{self.name}{RESET}: Price: {CYAN}{self.price}{RESET},"
                f" Quantity: {CYAN}{self.quantity}{RESET}")

    def buy(self, quantity: int) -> float:
        """
        Processes a purchase of a specific quantity.

        Args:
            quantity (int): The number of items to buy (must be positive
            and within stock).

        Returns:
            float: The total cost of the purchase.

        Raises:
            ValueError: If the quantity is invalid (negative, zero, or more than the
            available stock).
        """
        if quantity <= 0:
            raise ValueError(f"{RED}ERROR! Invalid quantity.{RESET}")
        if quantity > self.quantity:
            raise ValueError(f"{RED}ERROR! Insufficient stock.{RESET}")

        total_price = self.price * quantity
        self.set_quantity(self.quantity - quantity)
        return total_price


class NonStockedProduct(Product):
    def __init__(self, name: str, price: float):
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity: int):
        raise ValueError(f"{RED}Quantity modification is not allowed for non-stocked products.{RESET}")

    def show(self) -> str:
        return f"{YELLOW}{self.name}{RESET}: Price: {CYAN}{self.price}{RESET}, Quantity: Always 0 (Non-stocked)"


class LimitedProduct(Product):
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def buy(self, quantity: int) -> float:
        if quantity > self.maximum:
            raise ValueError(f"{RED}ERROR! Cannot purchase more than {self.maximum} units of {self.name} at once.{RESET}")
        return super().buy(quantity)

    def show(self) -> str:
        return (f"{YELLOW}{self.name}{RESET}: Price: {CYAN}{self.price}{RESET},"
                f" Quantity: {CYAN}{self.quantity}{RESET}, Max per Order: {CYAN}{self.maximum}{RESET}")
