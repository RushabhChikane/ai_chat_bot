from db.database import get_db


def get_all_products(category=None):
    """Fetch all products, optionally filtered by category."""
    conn = get_db()
    if category:
        rows = conn.execute("SELECT * FROM products WHERE category = ? ORDER BY id", (category,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM products ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_product_by_name(name):
    """Find a product by exact or partial name match."""
    conn = get_db()
    row = conn.execute("SELECT * FROM products WHERE LOWER(name) = LOWER(?)", (name,)).fetchone()
    if not row:
        row = conn.execute("SELECT * FROM products WHERE LOWER(name) LIKE LOWER(?)", (f"%{name}%",)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_categories():
    """Get list of all product categories."""
    conn = get_db()
    rows = conn.execute("SELECT DISTINCT category FROM products ORDER BY category").fetchall()
    conn.close()
    return [r["category"] for r in rows]
