from products import Product
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
            print(f"{p_num}. {product.show()}")
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

    This function shows the list of products once at the start, lets the
    user select products by their list number, and enter the desired quantity.

    Products can be selected multiple times, and their quantities will be
    aggregated in the final order.

    After each successful addition to the order,it confirms and prompts the
    user to continue or finish the order.
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

        quantity = input(f"{GREEN}How many {RESET}"
                         f"'{product.name}' {GREEN}would you like?{RESET} ")

        try:
            quantity = int(quantity)
            if quantity <= 0:
                print(f"{RED}ATTENTION! Quantity must be a positive number.{RESET}")
                continue
            if product.name in shopping_list:
                shopping_list[product.name]['quantity'] += quantity
            else:
                shopping_list[product.name] = {'product': product, 'quantity': quantity}

            print(f"{CYAN}Added {quantity} x {product.name} to your order.{RESET}\n"
                  f"Continue ordering or type '{YELLOW}done{RESET}' to finish your order.")
        except ValueError:
            print(f"{RED}INVALID INPUT! Please enter a valid number.{RESET}")
            continue

    if shopping_list:
        try:
            order_list = [(item['product'], item['quantity']) for item
                          in shopping_list.values()]
            total_price = store.order(order_list)
            total_order_title = "YOUR ORDER SUMMARY"
            print(f"\n{total_order_title}")
            print(f"{CYAN}‾{RESET}" * len(total_order_title))

            for item in shopping_list.values():
                product = item['product']
                quantity = item['quantity']
                item_total = quantity * product.price
                print(f"{YELLOW}{product.name}{RESET} x {CYAN}{quantity}{RESET} @"
                      f" {CYAN}{product.price}{RESET} each\n"
                      f"Item Total: {CYAN}{item_total}{RESET}")
                print()

            print(f"Order Total: {CYAN}{total_price}{RESET}")

        except ValueError as e:
            print(e)


def start(store):
    """
    Displays the store menu and lets the user choose what they'd like to do.

    Args:
        store (Store): The store where we get the products and inventory info.

    This function shows a simple menu where the user can:
        1. View all the products in the store.
        2. See the total quantity of products available.
        3. Place an order (a placeholder for now).
        4. Quit the app.

    It keeps asking the user for input until they choose to quit or make a
    valid choice.
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
    Google Pixel.

    It then creates a store object with those products and hands it over to the
    `start()` function to run the menu.

    It's basically the entry point of the program where everything starts.
    """
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250)
    ]

    best_buy = store.Store(product_list)

    start(best_buy)


if __name__ == '__main__':
    main()
