# tables.py
# [ETİKET] Masa yönetimi (basic): başlat, masa ekle, müşteri oturt, boşalt, garson güncelle

import json
import os


def initialize_tables(path: str) -> list:
    # [ETİKET] tables.json varsa yükler, yoksa boş liste döndürür
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except (OSError, json.JSONDecodeError):
        return []


def add_table(tables: list, table_data: dict) -> list:
    # [ETİKET] Yeni masa ekler
    # table_data örnek:
    # {"number":1, "capacity":4, "server":"-", "status":"free", "party_size":0}

    # [ETİKET] Basit kontrol: aynı numaralı masa eklenmesin
    new_no = int(table_data.get("number"))
    for t in tables:
        if int(t.get("number")) == new_no:
            raise ValueError("Table number already exists.")

    # [ETİKET] Default alanlar
    table_data["number"] = new_no
    table_data["capacity"] = int(table_data.get("capacity", 0))
    table_data["server"] = table_data.get("server", "-")
    table_data["status"] = table_data.get("status", "free")
    table_data["party_size"] = int(table_data.get("party_size", 0))

    tables.append(table_data)
    return tables


def assign_table(tables: list, table_number: int, party_size: int) -> dict | None:
    # [ETİKET] Masayı boşsa dolu yapar ve müşteri oturtur
    # [ETİKET] Kural: party_size kapasiteyi geçmesin (manager override yok, basic)
    table_number = int(table_number)
    party_size = int(party_size)

    for t in tables:
        if int(t.get("number")) == table_number:
            if t.get("status") != "free":
                return None
            if party_size > int(t.get("capacity", 0)):
                return None

            t["status"] = "occupied"
            t["party_size"] = party_size
            return t

    return None


def release_table(tables: list, table_number: int) -> bool:
    # [ETİKET] Masayı boş yapar
    table_number = int(table_number)
    for t in tables:
        if int(t.get("number")) == table_number:
            t["status"] = "free"
            t["party_size"] = 0
            return True
    return False


def update_server(tables: list, table_number: int, server_name: str) -> dict:
    # [ETİKET] Masanın garsonunu günceller
    table_number = int(table_number)
    for t in tables:
        if int(t.get("number")) == table_number:
            t["server"] = str(server_name).strip() if str(server_name).strip() else "-"
            return t

    return {}
