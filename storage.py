import json
import os


def load_state(data_dir):
    tables = []
    menu = {}
    orders = []

    try:
        with open(os.path.join(data_dir, "tables.json"), "r") as f:
            tables = json.load(f)
    except:
        pass

    try:
        with open(os.path.join(data_dir, "menu.json"), "r") as f:
            menu = json.load(f)
    except:
        pass

    try:
        with open(os.path.join(data_dir, "orders.json"), "r") as f:
            orders = json.load(f)
    except:
        pass

    return tables, menu, orders


def save_state(data_dir, tables, menu, orders):
    with open(os.path.join(data_dir, "tables.json"), "w") as f:
        json.dump(tables, f)

    with open(os.path.join(data_dir, "menu.json"), "w") as f:
        json.dump(menu, f)

    with open(os.path.join(data_dir, "orders.json"), "w") as f:
        json.dump(orders, f)


def backup_day(data_dir, archive_dir):
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    backup_path = os.path.join(archive_dir, "backup.json")

    data = {}
    for file in ["tables.json", "menu.json", "orders.json"]:
        try:
            with open(os.path.join(data_dir, file), "r") as f:
                data[file] = json.load(f)
        except:
            data[file] = []

    with open(backup_path, "w") as f:
        json.dump(data, f)

    return backup_path


def log_kitchen_ticket(order, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = f"order_{order['table_number']}.txt"
    path = os.path.join(directory, filename)

    with open(path, "w") as f:
        f.write(f"Table: {order['table_number']}\n")
        for item in order["items"]:
            f.write(item.get("name", "") + "\n")

    return path
