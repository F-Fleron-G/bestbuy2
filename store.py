RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


class Store:
    """
    A class representing a store that has multiple products.
    """

    def __init__(self, products):
        """
        Initializes the store with a list of products.

        Args:
            products: The list of products to initialize the store with.
        """
        self.products = []
        for product in products:
            self.products.append(product)

    def add_product(self, product):
        """
        Adds a product to the store.

        Args:
            product: The product to be added to the store.
        """
        self.products.append(product)

    def remove_product(self, product):
        """
        Removes a product from the store.

        Args:
            product: The product to be removed from the inventory.
        """
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        """
        Returns the total quantity of all products in the store.

        Returns:
            The total quantity of all products in the store.
        """
        total_quantity = sum(product.get_quantity() for product in self.products)
        return total_quantity

    def get_all_products(self):
        """
        Returns all active products in the store.

        Returns:
            A list of active products in the store.
        """
        return [product for product in self.products if product.is_active()]

    def order(self, shopping_list):
        """
        Processes an order of multiple products and returns the total cost.

        Args:
            shopping_list: A list of tuples, where each tuple contains a product
                           and the quantity to buy.

        Returns:
            The total cost of the order.
        """
        total_price = 0.0
        for product, quantity in shopping_list:
            if quantity <= 0:
                raise ValueError(f"{RED}ATTENTION! You have entered "
                                 f"an invalid quantity for {product.name}. "
                                 f"Quantity must be zero or higher.{RESET}")
            if not product.is_active():
                raise ValueError(f"{product.name} {RED}is not available.{RESET}")
            if quantity > product.get_quantity():
                raise ValueError(f"{RED}INSUFFICIENT STOCK!{RESET} {product.name}\n"
                                 f"{RED}We have{RESET} {product.quantity} {RED}units available.{RESET}")

            total_price += product.buy(quantity)

        return total_price
