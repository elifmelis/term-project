def daily_sales_report(orders):
    total = 0
    for order in orders:
        for item in order["items"]:
            total += item.get("price", 0)
    return {
        "total_sales": total,
        "order_count": len(orders)
    }


def top_selling_items(orders, limit=5):
    counts = {}

    for order in orders:
        for item in order["items"]:
            name = item.get("name")
            if name:
                counts[name] = counts.get(name, 0) + 1

    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_items[:limit]


def server_performance(orders):
    performance = {}

    for order in orders:
        server = order.get("server", "Unknown")
        performance[server] = performance.get(server, 0) + 1

    return performance


def export_report(report, filename):
    with open(filename, "w") as f:
        f.write(str(report))
    return filename
