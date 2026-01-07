# orders.py
# [ETİKET] Basic sipariş sistemi (öğrenci seviyesi)
# [ETİKET] İstenen fonksiyonlar: open_order, add_item_to_order, remove_item_from_order,
#         update_item_status, calculate_bill, split_bill

VALID_STATUSES = ["ordered", "preparing", "served", "voided"]


def open_order(table_number: int) -> dict:
    # [ETİKET] Yeni sipariş açar
    return {
        "table_number": int(table_number),
        "items": [],        # her eleman: {"item_id","name","price","qty","note","status"}
        "discount": 0.0     # TL bazında indirim (opsiyonel)
    }


def add_item_to_order(order: dict, menu_item: dict, quantity: int, note: str = "") -> dict:
    # [ETİKET] Siparişe ürün ekler
    if quantity <= 0:
        raise ValueError("Quantity must be > 0")

    if menu_item.get("available", True) is False:
        raise ValueError("This item is not available")

    order["items"].append({
        "item_id": str(menu_item["id"]),
        "name": str(menu_item["name"]),
        "price": float(menu_item["price"]),
        "qty": int(quantity),
        "note": str(note),
        "status": "ordered"
    })
    return order


def remove_item_from_order(order: dict, item_id: str) -> dict:
    # [ETİKET] Siparişten ürün siler (ilk bulduğunu)
    item_id = str(item_id)
    items = order.get("items", [])

    for i in range(len(items)):
        if str(items[i].get("item_id")) == item_id:
            items.pop(i)
            return order

    raise ValueError("Item not found")


def update_item_status(order: dict, item_id: str, status: str) -> dict:
    # [ETİKET] Ürün durumunu günceller
    status = str(status).strip().lower()
    if status not in VALID_STATUSES:
        raise ValueError("Invalid status")

    item_id = str(item_id)
    for it in order.get("items", []):
        if str(it.get("item_id")) == item_id:
            it["status"] = status
            return order

    raise ValueError("Item not found")


def calculate_bill(order: dict, tax_rate: float, tip_rate: float) -> dict:
    # [ETİKET] Hesap hesaplar (voided ürünleri saymaz)
    subtotal = 0.0
    for it in order.get("items", []):
        if it.get("status") == "voided":
            continue
        subtotal += float(it["price"]) * int(it["qty"])

    discount = float(order.get("discount", 0.0))
    if discount < 0:
        discount = 0.0
    if discount > subtotal:
        discount = subtotal

    after_discount = subtotal - discount
    tax = after_discount * float(tax_rate)
    tip = after_discount * float(tip_rate)
    total = after_discount + tax + tip

    return {
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "tax": round(tax, 2),
        "tip": round(tip, 2),
        "total": round(total, 2)
    }


def split_bill(order: dict, method: str, parties: int | list[int]) -> list[dict]:
    # [ETİKET] Hesabı böler (basic)
    # method: "even" veya "by_seat" (basic sürümde ikisi de eşit bölme gibi çalışır)

    method = str(method).strip().lower()
    if method not in ["even", "by_seat"]:
        raise ValueError("Invalid split method")

    # [ETİKET] Kural: served/voided olmayan varsa bölme yok
    for it in order.get("items", []):
        if it.get("status") not in ["served", "voided"]:
            raise ValueError("Cannot split: not all items served/voided")

    # [ETİKET] kaç kişi?
    if isinstance(parties, int):
        n = parties
    else:
        n = len(parties)

    if n <= 0:
        raise ValueError("Parties must be > 0")

    # [ETİKET] sadece subtotal-discount'u bölelim (tax/tip main'de ayrıca eklenebilir)
    bill = calculate_bill(order, tax_rate=0.0, tip_rate=0.0)
    total = bill["subtotal"] - bill["discount"]

    per = round(total / n, 2)

    result = []
    for i in range(n):
        result.append({"party_no": i + 1, "amount": per})

    # [ETİKET] yuvarlama farkı varsa ilk kişiye ekle
    current_sum = round(sum(x["amount"] for x in result), 2)
    diff = round(total - current_sum, 2)
    if diff != 0 and len(result) > 0:
        result[0]["amount"] = round(result[0]["amount"] + diff, 2)

    return result
