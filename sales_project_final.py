import random
import pandas as pd
from datetime import datetime, timedelta
import sqlite3
import matplotlib.pyplot as plt
import os

# Always save output to Desktop
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# 1) Generate dataset
N = 300
start = datetime(2025, 1, 1)
products = ['Mixer', 'Juicer', 'Iron', 'Heater', 'Kettle']
price_map = {'Mixer': 2500, 'Juicer': 1800, 'Iron': 1200, 'Heater': 2200, 'Kettle': 900}
categories = {'Mixer': 'Kitchen', 'Juicer': 'Kitchen', 'Iron': 'Home', 'Heater': 'Home', 'Kettle': 'Kitchen'}
regions = ['North', 'South', 'East', 'West']

rows = []
for i in range(1, N+1):
    date = start + timedelta(days=random.randint(0, 210))
    product = random.choice(products)
    qty = random.randint(1, 5)
    price = price_map[product] + random.randint(-100, 300)
    revenue = qty * price
    rows.append({
        'order_id': f'ORD{i:04d}',
        'date': date.strftime('%Y-%m-%d'),
        'product': product,
        'category': categories[product],
        'quantity': qty,
        'price': price,
        'revenue': revenue,
        'region': random.choice(regions),
        'customer_id': f'CUST{random.randint(1,120):03d}'
    })

df = pd.DataFrame(rows)
csv_path = os.path.join(desktop, "sales_data.csv")
df.to_csv(csv_path, index=False)
print("✅ CSV created:", csv_path)

# 2) SQLite Database
db_path = os.path.join(desktop, "sales.db")
conn = sqlite3.connect(db_path)
df.to_sql('sales', conn, if_exists='replace', index=False)

# 3) Queries
q_top = """SELECT product, SUM(revenue) as total_revenue FROM sales GROUP BY product ORDER BY total_revenue DESC LIMIT 5;"""
top_products = pd.read_sql(q_top, conn)
print("\nTop Products:\n", top_products)

q_month = """SELECT strftime('%Y-%m', date) as month, SUM(revenue) as revenue FROM sales GROUP BY month ORDER BY month;"""
monthly = pd.read_sql(q_month, conn)

q_region = """SELECT region, SUM(revenue) as revenue FROM sales GROUP BY region ORDER BY revenue DESC;"""
region = pd.read_sql(q_region, conn)

# 4) Charts saved to Desktop
top_chart = os.path.join(desktop, "top_products.png")
top_products.plot.bar(x='product', y='total_revenue', legend=False, title="Top Products")
plt.savefig(top_chart); plt.clf()

month_chart = os.path.join(desktop, "monthly_revenue.png")
monthly.plot.line(x='month', y='revenue', marker='o', title="Monthly Revenue")
plt.xticks(rotation=45)
plt.savefig(month_chart); plt.clf()

region_chart = os.path.join(desktop, "region_revenue.png")
region.plot.bar(x='region', y='revenue', legend=False, title="Revenue by Region")
plt.savefig(region_chart); plt.clf()

print("✅ Plots saved to Desktop")

conn.close()
