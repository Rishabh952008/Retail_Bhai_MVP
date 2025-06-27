import streamlit as st
import sqlite3
from datetime import date

class BhaiyaApp:
    def __init__(self, db_path="db/Bhaiya.db"):
        # app start hote hi sabse pehle database se connection banate hain
        # currently using sqlite3, as it is lightweight and easy to set up , 
        # furthe we can switch to a more robust database like PostgreSQL or MySQL if needed
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def add_user(self, shop_name, owner_name, phone):
        self.cursor.execute(
            "INSERT INTO users (shop_name, owner_name, phone) VALUES (?, ?, ?)",
            (shop_name, owner_name, phone)
        )
        self.conn.commit()

    def get_user_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()

    def add_daily_sale(self, user_id, total_sale, stock_purchase, expenses, notes):
        today = date.today().isoformat()
        self.cursor.execute("""
            INSERT INTO daily_sales (user_id, date, total_sale, stock_purchase, expenses, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, today, total_sale, stock_purchase, expenses, notes))
        self.conn.commit()

    def get_summary(self, user_id):
        self.cursor.execute("""
            SELECT date, total_sale, stock_purchase, expenses, 
                   (total_sale - stock_purchase - expenses) AS profit
            FROM daily_sales
            WHERE user_id = ?
            ORDER BY date DESC
            LIMIT 7
        """, (user_id,))
        return self.cursor.fetchall()


# Streamlit App
app = BhaiyaApp()
st.title("Vyapari: Multi-Shop Business Tracker")

users = app.get_users()

if not users:
    st.header("Setup Your First Shop")
    shop_name = st.text_input("Shop Name")
    owner_name = st.text_input("Owner Name")
    phone = st.text_input("Phone Number")
    if st.button("Create Account"):
        app.add_user(shop_name, owner_name, phone)
        st.success("Shop created! Reload the page.")
else:
    user_options = {f"{u[1]} - {u[2]}": u[0] for u in users}
    selected_label = st.sidebar.selectbox("🔐 Select Shopkeeper", list(user_options.keys()))
    selected_user_id = user_options[selected_label]
    user_data = app.get_user_by_id(selected_user_id)
    user_id, shop_name, owner_name, phone = user_data

    st.sidebar.write(f"👋 Welcome, {owner_name} ({shop_name})")

    st.header("📋 Enter Today's Business")
    total_sale = st.number_input("Total Sale (₹)", min_value=0.0)
    stock_purchase = st.number_input("Stock Purchase (₹)", min_value=0.0)
    expenses = st.number_input("Expenses (₹)", min_value=0.0)
    notes = st.text_area("Notes (optional)")

    if st.button("💾 Save Today's Entry"):
        app.add_daily_sale(user_id, total_sale, stock_purchase, expenses, notes)
        st.success("Entry saved!")

    st.header("📊 Last 7 Days Summary")
    summary = app.get_summary(user_id)
    if summary:
        for entry in summary:
            st.markdown(f"""
**{entry[0]}**  
Sale: ₹{entry[1]} | Purchase: ₹{entry[2]} | Expenses: ₹{entry[3]}  
👉 Profit: ₹{entry[4]}
""")
    else:
        st.info("No entries yet. Start by adding today's sale.")
