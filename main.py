from tables import initialize_tables, add_table, assign_table, release_table, update_server
from menu import load_menu, save_menu, add_menu_item, update_menu_item, filter_menu
import os

DATA_DIR = "data"
TABLES_PATH = os.path.join(DATA_DIR, "tables.json")
MENU_PATH = os.path.join(DATA_DIR, "menu.json")


def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    tables = initialize_tables(TABLES_PATH)
    menu = load_menu(MENU_PATH)

    while True:
        print("\n=== Restaurant System ===")
        print("1) Host Menu")
        print("2) Manager Menu")
        print("0) Exit")

        main_choice = input("Choice: ")

        if main_choice == "0":
            save_menu(MENU_PATH, menu)
            print("Goodbye.")
            break

        elif main_choice == "1":
            print("\n--- Host Menu ---")
            print("1) List Tables")
            print("2) Add Table")
            print("3) Assign Table")
            print("4) Release Table")
            print("5) Update Server")
            print("0) Back")

            host_choice = input("Choice: ")

            if host_choice == "0":
                pass

            elif host_choice == "1":
                for table in tables:
                    print(table)

            elif host_choice == "2":
                table_number = int(input("Table number: "))
                capacity = int(input("How many people can sit at this table?: "))
                server_name = input("Server name (can be empty): ")

                new_table = {
                    "number": table_number,
                    "capacity": capacity,
                    "server": server_name,
                    "status": "free"
                }

                tables = add_table(tables, new_table)
                print("Table added.")

            elif host_choice == "3":
                table_number = int(input("Table number: "))
                party_size = int(input("Party size: "))
                assign_table(tables, table_number, party_size)
                print("Table assigned.")

            elif host_choice == "4":
                table_number = int(input("Table number: "))
                release_table(tables, table_number)
                print("Table released.")

            elif host_choice == "5":
                table_number = int(input("Table number: "))
                new_server = input("New server name: ")
                update_server(tables, table_number, new_server)
                print("Server updated.")

        elif main_choice == "2":
            print("\n--- Manager Menu ---")
            print("1) List Menu Items")
            print("2) Add Menu Item")
            print("3) Update Menu Item")
            print("0) Back")

            manager_choice = input("Choice: ")

            if manager_choice == "0":
                pass

            elif manager_choice == "1":
                category = input("Category (starters/mains/desserts/beverages): ")
                items = filter_menu(menu, category)
                for item in items:
                    print(item)

            elif manager_choice == "2":
                category = input("Category: ")
                item_id = input("ID: ")
                name = input("Name: ")
                price = float(input("Price: "))

                new_item = {
                    "id": item_id,
                    "name": name,
                    "price": price,
                    "category": category
                }

                add_menu_item(menu, new_item)
                print("Item added.")

            elif manager_choice == "3":
                item_id = input("ID to update: ")
                new_price = float(input("New price: "))
                update_menu_item(menu, item_id, {"price": new_price})
                print("Item updated.")

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
