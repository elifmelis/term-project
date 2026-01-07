# storage.py
# [ETİKET] Basic persistence: data klasöründen yükle/kaydet + günlük yedek + kitchen ticket

import json
import os
import shutil
from datetime import datetime


def _safe_load_json(path, default):
    # [ETİKET] JSON dosyası varsa okur, yoksa default döndürür (çökmesin diye)
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default


def _safe_save_json(path, data):
    # [ETİKET] JSON kaydeder, klasör yoksa oluşturur
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_state(data_dir: str) -> tuple[list, dict, list]:
    # [ETİKET] data_dir içinden tables/menu/orders yükler
    # [ETİKET] Dönüş: (tables_list, menu_dict, orders_list)
    tables_path = os.path.join(data_dir, "tables.json")
    menu_path = os.path.join(data_dir, "menu.json")
    orders_path = os.path.join(data_dir, "orders.json")

    tables = _safe_load_json(tables_path, [])
    menu = _safe_load_json(menu_path, {"items": {}})
    orders = _safe_load_json(orders_path, [])

    # [ETİKET] Basit format düzeltme
    if not isinstance(tables, list):
        tables = []
    if not isinstance(menu, dict):
        menu = {"items": {}}
    if "items" not in menu or not isinstance(menu["items"], dict):
        menu["items"] = {}
    if not isinstance(orders, list):
        orders = []

    return tables, menu, orders


def save_state(data_dir: str, tables: list, menu: dict, orders: list) -> None:
    # [ETİKET] tables/menu/orders dosyalarını kaydeder
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    _safe_save_json(os.path.join(data_dir, "tables.json"), tables)
    _safe_save_json(os.path.join(data_dir, "menu.json"), menu)
    _safe_save_json(os.path.join(data_dir, "orders.json"), orders)


def backup_day(data_dir: str, archive_dir: str) -> str:
    # [ETİKET] Gün sonu yedeği alır: data_dir içeriğini archive_dir altına kopyalar
    # [ETİKET] Çıktı: oluşturulan backup klasör yolu

    if not os.path.exists(data_dir):
        raise ValueError("data_dir does not exist")

    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(archive_dir, f"backup_{stamp}")

    os.makedirs(backup_folder)

    # [ETİKET] data klasöründeki json dosyalarını kopyala
    for name in ["tables.json", "menu.json", "orders.json"]:
        src = os.path.join(data_dir, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(backup_folder, name))

    return backup_folder


def log_kitchen_ticket(order: dict, directory: str) -> str:
    # [ETİKET] Kitchen ticket text dosyası yazar (sipariş mutfak çıktısı)
    # [ETİKET] Çıktı: ticket dosyasının yolu

    if not os.path.exists(directory):
        os.makedirs(directory)

    table_no = order.get("table_number", "NA")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ticket_table{table_no}_{stamp}.txt"
    path = os.path.join(directory, filename)

    lines = []
    lines.append("=== KITCHEN TICKET ===")
    lines.append(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Table: {table_no}")
    lines.append("----------------------")

    for it in order.get("items", []):
        # [ETİKET] voided olanları mutfağa basmayalım
        if it.get("status") == "voided":
            continue
        qty = it.get("qty", 1)
        name = it.get("name", "Item")
        note = it.get("note", "")
        line = f"{qty}x {name}"
        lines.append(line)
        if str(note).strip() != "":
            lines.append(f"  note: {note}")

    lines.append("----------------------")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return path
