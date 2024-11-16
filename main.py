from products import Product, NonStockedProduct, LimitedProduct
from promotions import SecondHalfPrice, ThirdOneFree, PercentDiscount
import store

RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
PURPLE = "\033[95m"
GREEN = "\033[92m"
RESET = "\033[0m"


def list_products(store):
    """Displays all active products in the store with a number for selection."""
    p_list_title = "AVAILABLE PRODUCTS"
    print(f"{p_list_title}")
    print(f"{YELLOW}‾{RESET}" * len(p_list_title))

    products = store.get_all_products()

    if not products:
        print(f"{YELLOW}WE ARE OUT OF STOCK!{RESET}")
    else:
        for p_num, product in enumerate(products, start=1):
            promotion_text = (
                f"{PURPLE}{product.promotion}{RESET}"
                if product.promotion
                else f"{RED}None{RESET}"
            )
            print(
                f"{YELLOW}{p_num}.{RESET} {YELLOW}{product.name}{RESET}, "
                f"Price: {CYAN}${product.price:.2f}{RESET}, "
                f"Quantity: {CYAN}{product.quantity if hasattr(product, 'quantity') else 'N/A'}{RESET}, "
                f"Promotion: {promotion_text}"
            )
    print()


def show_total_amount(store):
    """Shows the total quantity of all products in the store."""
    total_quantity = store.get_total_quantity()
    p_quantity_title = "TOTAL PRODUCTS"
    print(p_quantity_title)
    print(f"{CYAN}‾{RESET}" * len(p_quantity_title))
    print(f"We have {CYAN}{total_quantity}{RESET} products in stock.")


def make_order(store):
    """
    Allows the user to place an order by selecting products by number and
    specifying quantities.

    Displays products with promotions, handles invalid transactions gracefully,
    and provides a detailed order summary.
    """
    list_products(store)
    p_order_title = "PLACE YOUR ORDER"
    print(f"{p_order_title}")
    print(f"{YELLOW}‾{RESET}" * len(p_order_title))
    print(f"{YELLOW}(When done, type {RESET}'done'{YELLOW} to finish.){RESET}\n")

    shopping_list = {}

    while True:
        product_num = input(f"{GREEN}Please enter the product number:{RESET} ")

        if product_num.lower() == 'done':
            break

        try:
            product_index = int(product_num) - 1
            products = store.get_all_products()
            if product_index < 0 or product_index >= len(products):
                print(f"{RED}INVALID SELECTION! Please select a valid product number.{RESET}")
                continue
            product = products[product_index]
        except ValueError:
            print(f"{RED}INVALID INPUT! Please enter a number.{RESET}")
            continue

        quantity = input(f"{GREEN}How many {RESET}'{product.name}'"
                         f" {GREEN}would you like?{RESET} ")

        try:
            quantity = int(quantity)
            if quantity <= 0:
                print(f"{RED}ATTENTION! Quantity must be a positive number.{RESET}")
                continue

            try:
                total_cost = product.buy(quantity)
                if product.name in shopping_list:
                    shopping_list[product.name]['quantity'] += quantity
                    shopping_list[product.name]['total_cost'] += total_cost
                else:
                    shopping_list[product.name] = {'quantity': quantity, 'total_cost': total_cost}
                print(f"{CYAN}Added {quantity} x {product.name} to your order.{RESET}\n"
                      f"Continue ordering or type '{YELLOW}done{RESET}' to finish your order.")
            except ValueError as e:
                print(f"{RED}{e}{RESET}")

        except ValueError:
            print(f"{RED}INVALID INPUT! Please enter a valid number.{RESET}")
            continue

    if shopping_list:
        total_order_title = "YOUR ORDER SUMMARY"
        print(f"\n{total_order_title}")
        print(f"{CYAN}‾{RESET}" * len(total_order_title))

        total_price = 0
        for name, details in shopping_list.items():
            print(f"{YELLOW}{name}{RESET}: {CYAN}{details['quantity']}"
                  f" items{RESET}, Total: {CYAN}${details['total_cost']:.2f}{RESET}")
            total_price += details['total_cost']

        print(f"\nOrder Total: {CYAN}${total_price:.2f}{RESET}")
    else:
        print(f"{YELLOW}No items were added to your order.{RESET}")


def start(store):
    """
    Displays the store menu and lets the user choose what they'd like to do.

    Args:
        store (Store): The store where we get the products and inventory info.

    This function shows a simple menu where the user can:
        1. View all the products in the store.
        2. See the total quantity of products available.
        3. Place an order.
        4. Quit the app.
    """
    while True:
        menu_title = "STORE MENU"
        print(f"\n{menu_title}")
        print(f"{PURPLE}‾{RESET}" * len(menu_title))
        print(f"{PURPLE}1.{RESET} List all products in store")
        print(f"{PURPLE}2.{RESET} Show total products in store")
        print(f"{PURPLE}3.{RESET} Make an order")
        print(f"{PURPLE}4.{RESET} Quit")

        choice = input(f"\n{GREEN}Please choose a number:{RESET} ")
        print()

        if choice == '1':
            list_products(store)
        elif choice == '2':
            show_total_amount(store)
        elif choice == '3':
            make_order(store)
        elif choice == '4':
            print(f"{PURPLE}COME AGAIN!{RESET}")
            break
        else:
            print(f"{RED}INVALID CHOICE! Please select a valid option (1-4).{RESET}")


def main():
    """
    Sets up the store with some products and kicks off the user interface.

    This creates a list of products like the MacBook Air, Bose earbuds, and the
    Google Pixel, along with promotions.

    It then creates a store object with those products and hands it over to the
    `start()` function to run the menu.
    """
    second_half_price = SecondHalfPrice("Second Half price!")
    third_one_free = ThirdOneFree("Third One Free!")
    thirty_percent = PercentDiscount("30% off!", percent=30)

    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    ]

    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[3].set_promotion(thirty_percent)

    best_buy = store.Store(product_list)

    start(best_buy)


if __name__ == '__main__':
    main()
