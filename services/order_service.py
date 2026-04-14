from db.database import get_db
from services.product_service import get_product_by_name


def place_order(product_name, quantity):
    """Place an order: validate stock, create order, update stock."""
    product = get_product_by_name(product_name)
    if not product:
        return {"error": f"Product '{product_name}' not found."}

    if product["stock"] < quantity:
        return {"error": f"Not enough stock. Available: {product['stock']}, Requested: {quantity}"}

    total = product["price"] * quantity
    stock_after = product["stock"] - quantity

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (product_id, product_name, quantity, total_price) VALUES (?, ?, ?, ?)",
        (product["id"], product["name"], quantity, total),
    )
    order_id = cursor.lastrowid
    cursor.execute("UPDATE products SET stock = ? WHERE id = ?", (stock_after, product["id"]))
    conn.commit()
    conn.close()

    return {
        "order_id": order_id,
        "product_name": product["name"],
        "quantity": quantity,
        "total_price": total,
        "stock_remaining": stock_after,
    }


def get_all_orders():
    """Fetch all orders, most recent first."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM orders ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_order_by_id(order_id):
    """Fetch a single order."""
    conn = get_db()
    row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    conn.close()
    return dict(row) if row else None
