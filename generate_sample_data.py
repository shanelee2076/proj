"""
Generates a realistic sample sales dataset (data/sample_sales_data.csv)
so the Streamlit app has something to display out of the box.
Run once: python generate_sample_data.py
"""

import numpy as np
import pandas as pd
import os

np.random.seed(42)

categories = {
    "Electronics": ["Wireless Earbuds", "Bluetooth Speaker", "Smartwatch", "Power Bank",
                    "USB-C Cable", "Laptop Stand", "Webcam", "Gaming Mouse"],
    "Home & Kitchen": ["Air Fryer", "Non-Stick Pan Set", "Electric Kettle", "Blender",
                       "Cutlery Set", "Storage Containers", "Coffee Maker"],
    "Fashion": ["Cotton T-Shirt", "Denim Jacket", "Running Shoes", "Leather Wallet",
                "Sunglasses", "Backpack", "Formal Shirt"],
    "Beauty & Personal Care": ["Face Moisturizer", "Shampoo", "Electric Trimmer",
                               "Perfume", "Lip Balm Set", "Hair Dryer"],
    "Sports & Fitness": ["Yoga Mat", "Dumbbell Set", "Resistance Bands", "Water Bottle",
                         "Cycling Helmet", "Skipping Rope"],
    "Stationery": ["Notebook Pack", "Gel Pens Set", "Sticky Notes", "Desk Organizer",
                   "Whiteboard Marker"],
}

rows = []
product_id = 1000

for category, products in categories.items():
    for product in products:
        # Base economics per product
        cost_price = np.round(np.random.uniform(100, 3000), 2)

        # Some products are intentionally loss-making (thin/negative margin)
        margin_type = np.random.choice(["healthy", "thin", "loss"], p=[0.6, 0.25, 0.15])
        if margin_type == "healthy":
            margin_pct = np.random.uniform(0.20, 0.55)
        elif margin_type == "thin":
            margin_pct = np.random.uniform(0.03, 0.10)
        else:
            margin_pct = np.random.uniform(-0.25, -0.02)

        selling_price = np.round(cost_price * (1 + margin_pct), 2)
        units_sold = int(np.random.gamma(shape=2.0, scale=60))  # skewed distribution
        units_sold = max(units_sold, 5)

        revenue = np.round(selling_price * units_sold, 2)
        total_cost = np.round(cost_price * units_sold, 2)
        profit = np.round(revenue - total_cost, 2)

        rows.append({
            "Product_ID": f"P{product_id}",
            "Product_Name": product,
            "Category": category,
            "Units_Sold": units_sold,
            "Cost_Price": cost_price,
            "Selling_Price": selling_price,
            "Revenue": revenue,
            "Total_Cost": total_cost,
            "Profit": profit,
        })
        product_id += 1

df = pd.DataFrame(rows)

os.makedirs("data", exist_ok=True)
df.to_csv("data/sample_sales_data.csv", index=False)
print(f"Generated {len(df)} product rows -> data/sample_sales_data.csv")
