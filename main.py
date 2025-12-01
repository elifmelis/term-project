from tables import initialize_tables, add_table, assign_table, release_table, update_server
from menu import load_menu, save_menu
import os

DATA_DIR = "data"
TABLES_PATH = os.path.join(DATA_DIR, "tables.json")
MENU_PATH = os.path.join(DATA_DIR, "menu.json")

def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    tables = initialize_tables(TABLES_PATH)
    menu = load_menu(MENU_PATH)   # şimdilik bunu kullanmıyoruz ama lazım

    while True:
        print("\n=== Restaurant System ===")
        print("1) Host Menu")
        print("0) Exit")

        choice = input("Choice: ")

        if choice == "0":
            print("Goodbye.")
            break

        elif choice == "1":
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
                for t in tables:
                    print(t)

            elif host_choice == "2":
                number = int(input("Table number: "))
                capacity = int(input("Capacity: "))
                server = input("Server name: ")

                new_table = {
                    "number": number,
                    "capacity": capacity,
                    "server": server,
                    "status": "free"
                }

                tables = add_table(tables, new_table)
                print("Table added.")

            elif host_choice == "3":
                number = int(input("Table number: "))
                size = int(input("Party size: "))
                assign_table(tables, number, size)
                print("Table assigned.")

            elif host_choice == "4":
                number = int(input("Table number: "))
                release_table(tables, number)
                print("Table released.")

            elif host_choice == "5":
                number = int(input("Table number: "))
                new_server = input("New server name: ")
                update_server(tables, number, new_server)
                print("Server updated.")

if __name__ == "__main__":
    main()
