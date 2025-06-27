import sqlite3

conn = sqlite3.connect("bhaiya.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_name TEXT,
    owner_name TEXT,
    phone TEXT
);
""")

# Create daily_sales table
cursor.execute("""
CREATE TABLE IF NOT EXISTS daily_sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    total_sale REAL,
    stock_purchase REAL,
    expenses REAL,
    notes TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);
""")

conn.commit()
conn.close()
