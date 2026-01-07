# menu.py
# [ETİKET] Menü yönetimi: JSON'dan yükle/kaydet + ürün ekle/güncelle + filtrele
# [ETİKET] Menü yapısı (dict):
# menu = {
#   "items": {
#       "I001": {"id":"I001","name":"Soup","category":"starters","price":60.0,"vegetarian":True,"available":True},
#       ...
#   }
# }

import json
import os


def _default_menu():
    # [ETİKET] Boş menü şablonu
    return {"items": {}}


def load_menu(path: str) -> dict:
    # [ETİKET] Menü dosyasını yükler (yoksa boş menü döndürür)
    if not os.path.exists(path):
        return _default_menu()

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # [ETİKET] Basit doğrulama: items yoksa ekle
        if not isinstance(data, dict):
            return _default_menu()
        if "items" not in data or not isinstance(data["items"], dict):
            data["items"] = {}

        return data
    except (json.JSONDecodeError, OSError):
        # [ETİKET] Dosya bozuksa program çökmesin
        return _default_menu()


def save_menu(path: str, menu: dict) -> None:
    # [ETİKET] Menü dosyasını kaydeder (klasör yoksa oluşturur)
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(menu, f, ensure_ascii=False, indent=4)


def add_menu_item(menu: dict, item: dict) -> dict:
    # [ETİKET] Menüye ürün ekler
    # item örnek:
    # {"id":"I001","name":"Pasta","category":"mains","price":120.0,"vegetarian":False,"available":True}

    if "items" not in menu or not isinstance(menu["items"], dict):
        menu["items"] = {}

    # [ETİKET] Zorunlu alan kontrolü
    required = ["id", "name", "category", "price"]
    for key in required:
        if key not in item:
            raise ValueError(f"Missing field: {key}")

    item_id = str(item["id"]).strip()
    if item_id == "":
        raise ValueError("Item id cannot be empty.")

    # [ETİKET] Tekrar id eklenmesin
    if item_id in menu["items"]:
        raise ValueError("Item id already exists.")

    # [ETİKET] Varsayılan alanlar
    normalized = {
        "id": item_id,
        "name": str(item["name"]).strip(),
        "category": str(item["category"]).strip().lower(),
        "price": float(item["price"]),
        "vegetarian": bool(item.get("vegetarian", False)),
        "available": bool(item.get("available", True)),
    }

    menu["items"][item_id] = normalized
    return menu


def update_menu_item(menu: dict, item_id: str, updates: dict) -> dict:
    # [ETİKET] Menü ürününü günceller (name/category/price/vegetarian/available)
    if "items" not in menu or item_id not in menu["items"]:
        raise ValueError("Item not found.")

    item = menu["items"][item_id]

    # [ETİKET] İzin verilen alanlar
    allowed = {"name", "category", "price", "vegetarian", "available"}
    for key in updates:
        if key not in allowed:
            raise ValueError(f"Invalid update field: {key}")

    if "name" in updates:
        item["name"] = str(updates["name"]).strip()

    if "category" in updates:
        item["category"] = str(updates["category"]).strip().lower()

    if "price" in updates:
        item["price"] = float(updates["price"])

    if "vegetarian" in updates:
        item["vegetarian"] = bool(updates["vegetarian"])

    if "available" in updates:
        item["available"] = bool(updates["available"])

    menu["items"][item_id] = item
    return menu


def filter_menu(menu: dict, category: str, vegetarian: bool | None = None) -> list:
    # [ETİKET] Kategoriye göre filtreler, istenirse vegetarian filtresi uygular
    # [ETİKET] Sadece available=True olanları listeler (deactive olan gelmez)
    if "items" not in menu:
        return []

    cat = str(category).strip().lower()
    result = []

    for item_id, item in menu["items"].items():
        if not item.get("available", True):
            continue

        if str(item.get("category", "")).lower() != cat:
            continue

        if vegetarian is not None and bool(item.get("vegetarian", False)) != vegetarian:
            continue

        result.append(item)

    return result


# (OPSİYONEL ama işe yarar) Menüde arama
def search_menu(menu: dict, text: str) -> list:
    # [ETİKET] İsim içinde arama yapar (available olanlarda)
    query = str(text).strip().lower()
    if query == "" or "items" not in menu:
        return []

    out = []
    for item in menu["items"].values():
        if not item.get("available", True):
            continue
        if query in str(item.get("name", "")).lower():
            out.append(item)
    return out
