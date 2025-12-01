import json

def initialize_tables(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tables(path, tables):
    with open(path, "w") as f:
        json.dump(tables, f)

def add_table(tables, table_data):
    tables.append(table_data)
    return tables

def assign_table(tables, table_number):
    for t in tables:
        if t["number"] == table_number:
            t["status"] = "occupied"
            return

def release_table(tables, table_number):
    for t in tables:
        if t["number"] == table_number:
            t["status"] = "free"
            return
