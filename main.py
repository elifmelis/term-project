# main.py
# [ETİKET] Ana dosya: Terminal menülerini gösterir ve modülleri çağırır.

from tables import initialize_tables, add_table, assign_table, release_table, update_server
from menu import load_menu, save_menu
from orders import open_order, add_item_to_order, calculate_bill

import os

# [ETİKET] Data klasörü ve dosya yolları
DATA_DIR = "data"
TABLES_PATH = os.path.join(DATA_DIR, "tables.json")
MENU_PATH = os.path.join(DATA_DIR, "menu.json")


def ensure_data_dir():
    # [ETİKET] data/ yoksa oluşturur
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def print_tables(tables):
    # [ETİKET] Masaları ekrana basar
    if not tables:
        print("No tables yet.")
        return

    print("\n--- Tables ---")
    for t in tables:
        print(
            f"Table {t['number']} | cap={t['capacity']} | status={t['status']} | "
            f"server={t.get('server','-')} | party={t.get('party_size', 0)}"
        )


def host_menu(tables):
    # [ETİKET] Host menüsü (table management)
    while True:
        print("\n--- Host Menu ---")
        print("1) List Tables")
        print("2) Add Table")
        print("3) Assign Table (Seat Customers)")
        print("4) Release Table (Free Table)")
        print("5) Update Server")
        print("0) Back")

        choice = input("Choice: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            print_tables(tables)

        elif choice == "2":
            try:
                number = int(input("Table number: "))
                capacity = int(input("Capacity: "))
                server = input("Server name (optional): ").strip()

                table_data = {
                    "number": number,
                    "capacity": capacity,
                    "status": "free",
                    "server": server if server else "-",
                    "party_size": 0
                }
                tables = add_table(tables, table_data)
                print("Table added.")
            except ValueError:
                print("Invalid input. Please enter numbers for table/capacity.")

        elif choice == "3":
            try:
                number = int(input("Table number: "))
                party_size = int(input("Party size: "))

                result = assign_table(tables, number, party_size)
                if result is None:
                    print("Could not assign table (maybe full/occupied/not found).")
                else:
                    print(f"Assigned table {number} to party of {party_size}.")
            except ValueError:
                print("Invalid input. Please enter numbers.")

        elif choice == "4":
            try:
                number = int(input("Table number: "))
                ok = release_table(tables, number)
                print("Released." if ok else "Table not found.")
            except ValueError:
                print("Invalid input.")

        elif choice == "5":
            try:
                number = int(input("Table number: "))
                server_name = input("New server name: ").strip()
                updated = update_server(tables, number, server_name)
                if updated:
                    print("Server updated.")
                else:
                    print("Table not found.")
            except ValueError:
                print("Invalid input.")
        else:
            print("Invalid choice.")

    return tables


def main():
    # [ETİKET] Program başlangıcı
    ensure_data_dir()

    # [ETİKET] Başlangıç veri yükleme (şimdilik boş başlatıyoruz; sonraki adımda storage ekleyeceğiz)
    tables = initialize_tables(TABLES_PATH)
    menu = load_menu(MENU_PATH)  # şu an kullanmayacağız ama hazır dursun

    while True:
        print("\n=== Restaurant System ===")
        print("1) Host Menu")
        print("0) Exit")

        choice = input("Choice: ").strip()

        if choice == "0":
            print("Goodbye.")
            break

        elif choice == "1":
            tables = host_menu(tables)

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
