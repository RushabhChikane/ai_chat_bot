from db.database import get_db

PRODUCTS = [
    # Electronics
    ("iPhone 15", "electronics", 79999, "Apple iPhone 15 with A16 Bionic chip, 128GB storage, 48MP camera, Super Retina XDR display.", 10, 4.5),
    ("Samsung Galaxy S24", "electronics", 69999, "Samsung Galaxy S24 with Snapdragon 8 Gen 3, 128GB storage, 50MP triple camera, Dynamic AMOLED display.", 15, 4.4),
    ("Dell Inspiron 15 Laptop", "electronics", 45999, "Dell Inspiron 15 with Intel Core i5 13th Gen, 8GB RAM, 512GB SSD, 15.6 inch FHD display.", 8, 4.2),
    ("Sony WH-1000XM5 Headphones", "electronics", 24999, "Sony premium noise cancelling wireless headphones with 30-hour battery and exceptional sound quality.", 20, 4.7),
    ("Apple Watch Series 9", "electronics", 41999, "Apple Watch Series 9 with S9 chip, blood oxygen monitoring, ECG, always-on display, fitness tracking.", 12, 4.6),
    ("iPad Air", "electronics", 59999, "Apple iPad Air with M1 chip, 10.9 inch Liquid Retina display, 64GB storage.", 7, 4.5),
    # Clothing
    ("Levi's 511 Slim Fit Jeans", "clothing", 2499, "Levi's 511 slim fit jeans in classic blue denim. Comfortable stretch fabric.", 30, 4.3),
    ("Nike Air Max 270 Sneakers", "clothing", 8999, "Nike Air Max 270 with large Air unit in the heel. Mesh upper, lightweight and breathable.", 25, 4.4),
    ("Allen Solly Formal Shirt", "clothing", 1799, "Allen Solly men's slim fit formal shirt in white. Cotton fabric, button-down collar.", 40, 4.1),
    ("Adidas Originals Track Jacket", "clothing", 4999, "Adidas Originals track jacket with iconic three stripes. Recycled polyester, full zip.", 18, 4.3),
    ("Puma Essential Cotton T-Shirt", "clothing", 999, "Puma Essentials men's cotton t-shirt. Soft fabric, crew neck, Puma cat logo.", 50, 4.0),
    # Books
    ("Python Crash Course", "books", 599, "Best-selling Python programming book covering basics, data structures, web dev, and projects.", 35, 4.6),
    ("Hands-On Machine Learning", "books", 799, "Hands-On ML with Scikit-Learn, Keras, and TensorFlow. Covers neural networks and deep learning.", 20, 4.7),
    ("Clean Code by Robert Martin", "books", 699, "A handbook of agile software craftsmanship. Write clean, readable, and maintainable code.", 30, 4.5),
    # Home
    ("JBL Flip 6 Bluetooth Speaker", "home", 9999, "JBL Flip 6 portable Bluetooth speaker with powerful sound, 12-hour battery, IP67 waterproof.", 15, 4.5),
    ("Philips LED Desk Lamp", "home", 1299, "Philips LED desk lamp with adjustable brightness and color temperature. Eye-care technology.", 22, 4.3),
    # Accessories
    ("Logitech MX Master 3S Mouse", "accessories", 8999, "Logitech MX Master 3S wireless mouse with 8K DPI sensor, quiet clicks, MagSpeed scroll wheel.", 14, 4.8),
    ("Keychron K2 Mechanical Keyboard", "accessories", 6999, "Keychron K2 wireless mechanical keyboard with Gateron switches, RGB backlight, 75% layout.", 12, 4.6),
    ("Anker 7-in-1 USB-C Hub", "accessories", 2499, "Anker USB-C hub with HDMI 4K output, 2 USB-A ports, SD card reader, 100W power delivery.", 28, 4.4),
    ("Spigen iPhone 15 Case", "accessories", 1299, "Spigen Tough Armor case for iPhone 15. Military-grade drop protection, built-in kickstand.", 45, 4.3),
]


def seed_products():
    """Insert sample products if the table is empty."""
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if count > 0:
        conn.close()
        return

    conn.executemany(
        "INSERT INTO products (name, category, price, description, stock, rating) VALUES (?, ?, ?, ?, ?, ?)",
        PRODUCTS,
    )
    conn.commit()
    conn.close()
