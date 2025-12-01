import json

def open_order(table_number):
    return {
        "table_number": table_number,
        "items": []
    }

def add_item_to_order(order, item):
    order["items"].append(item)
    return order

def remove_item_from_order(order, item_id):
    for item in order["items"]:
        if item["id"] == item_id:
            order["items"].remove(item)
            return order
    return order

def update_item_in_order(order, item_id, new_name):
    for item in order["items"]:
        if item["id"] == item_id:
            item["name"] = new_name
            return order
    return order

def show_order(order):
    return order["items"]
