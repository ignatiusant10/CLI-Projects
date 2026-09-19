from Service import (
    create_customer,
    list_all_customer,
    load_data,
    search,
    update,
    delete,
    ALLOWED_FIELDS,
)
from exceptions import CustomerNotFound, DuplicateCustomerError  

MENU = """
1. Add customer
2. List all customers
3. Search customer
4. Update customer
5. Delete customer
6. Exit
"""

HEADER = f"| {'ID':<6} | {'Name':<15} | {'Email':<25} | {'Phone':<12} |"
LINE = "-" * len(HEADER)


def ask(prompt):
    return input(prompt).strip()


def print_row(cid, customer):
    print(f"| {cid:<6} | {customer.name:<15} | {customer.email:<25} | {customer.phone:<12} |")


def print_table(rows):
    print(LINE)
    print(HEADER)
    print(LINE)
    for cid, customer in rows:
        print_row(cid, customer)
    print(LINE)


def add_customer():
    customer_id = ask("Enter customer id> ")
    if not customer_id:
        raise ValueError("Customer ID empty ah irukka koodadhu")
    name = ask("Enter customer name> ")
    email = ask("Enter customer email> ")
    phone = ask("Enter customer phone> ")
    create_customer(customer_id, name, email, phone)
    print(f"{name} added successfully!")


def show_all_customers():
    customers = list_all_customer()
    print_table(customers.items())


def search_customer():
    customer_id = ask("Enter customer id> ")
    customer = search(customer_id)
    print_table([(customer_id, customer)])


def update_customer():
    customer_id = ask("Enter customer id> ")
    print(f"Fields: {', '.join(sorted(ALLOWED_FIELDS))}")
    field_name = ask("Enter field name> ").lower()
    new_value = ask("Enter new value> ")
    update(customer_id, field_name, new_value)
    print(f"{field_name} updated successfully!")


def delete_customer():
    customer_id = ask("Enter customer id> ")
    if ask(f"Delete {customer_id}? (y/n)> ").lower() != "y":
        print("Cancelled.")
        return
    delete(customer_id)
    print(f"{customer_id} has been deleted!")


ACTIONS = {
    "1": add_customer,
    "2": show_all_customers,
    "3": search_customer,
    "4": update_customer,
    "5": delete_customer,
}


def main():
    try:
        load_data()
    except RuntimeError as e:
        print(f"Error: {e}")
        return

    while True:
        print(MENU)
        choice = ask("Enter 1-6> ")

        if choice == "6":
            break

        action = ACTIONS.get(choice)
        if action is None:
            print("Thappu choice! 1-6 mattum type pannunga.")
            continue

        try:
            action()
        except (CustomerNotFound, DuplicateCustomerError, ValueError) as e:
            print(f"Error: {e}")

    print("Bye have a great day!")


