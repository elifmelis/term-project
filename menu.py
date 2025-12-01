import json

def load_menu(path):
    try:
        with open(path, "r") as file:
            menu = json.load(file)
            return menu
    except:
        return {
            "starters": [],
            "mains": [],
            "desserts": [],
            "beverages": []
        }

def save_menu(path, menu):
    with open(path, "w") as file:
        json.dump(menu, file)

