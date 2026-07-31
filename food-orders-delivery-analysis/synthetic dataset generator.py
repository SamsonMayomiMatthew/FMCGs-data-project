import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducible results
np.random.seed(42)
num_records = 1500

# 1. Generate Order IDs
order_ids = [f"ORD-2026-{1000 + i}" for i in range(num_records)]

# 2. Generate Timestamps (Simulating realistic peak hours)
start_date = datetime(2026, 5, 1)
timestamps = []
for _ in range(num_records):
    # Pick a random day over a 60-day period
    random_days = np.random.randint(0, 60)
    
    # Peak hours: Lunch (12 PM - 2 PM) & Dinner (6 PM - 9 PM)
    if np.random.rand() < 0.65:
        hour = np.random.choice([12, 13, 14, 18, 19, 20, 21])
    else:
        hour = np.random.choice([8, 9, 10, 11, 15, 16, 17, 22])
        
    minute = np.random.randint(0, 60)
    second = np.random.randint(0, 60)
    timestamps.append(start_date + timedelta(days=int(random_days), hours=int(hour), minutes=int(minute), seconds=int(second)))

# 3. Geo & Product Options
zones = ["Ikeja", "Lekki Phase 1", "Victoria Island", "Yaba", "Surulere", "Gbagada"]
zone_weights = [0.25, 0.25, 0.20, 0.12, 0.10, 0.08]

cuisine_items = {
    "Local Delicacies": ["Jollof Rice & Fried Chicken", "Pounded Yam & Egusi", "Amala & Abula", "Fried Plantain & Asun"],
    "Fast Food": ["Beef Burger & Fries", "Crispy Chicken Wings", "Shawarma Special"],
    "Grills & Suya": ["Spicy Beef Suya", "Grilled Catfish", "BBQ Chicken Quarters"],
    "Continental": ["Seafood Pasta", "Chicken Caesar Salad", "Club Sandwich"]
}

cuisines = list(cuisine_items.keys())
cuisine_weights = [0.45, 0.25, 0.20, 0.10]

# 4. Populate Detailed Rows
data = []
for i in range(num_records):
    ts = timestamps[i]
    zone = np.random.choice(zones, p=zone_weights)
    cuisine = np.random.choice(cuisines, p=cuisine_weights)
    item = np.random.choice(cuisine_items[cuisine])
    
    # Financial calculations
    base_price = np.random.choice([3500, 4500, 5000, 6500, 8000, 12000])
    delivery_fee = np.random.choice([800, 1000, 1200, 1500, 2000])
    discount = np.random.choice([0, 0, 0, 500, 1000], p=[0.6, 0.2, 0.1, 0.07, 0.03])
    total_amount = base_price + delivery_fee - discount
    
    # Operational metrics
    prep_time = int(np.random.normal(20, 5))
    prep_time = max(10, prep_time)  # Cap floor at 10 mins
    
    delivery_time = int(np.random.normal(35, 10))
    delivery_time = max(15, delivery_time)
    
    # Order Status & Rating
    status = np.random.choice(["Delivered", "Cancelled", "In Transit"], p=[0.90, 0.07, 0.03])
    
    if status == "Delivered":
        rating = round(np.random.uniform(3.5, 5.0), 1)
    else:
        rating = np.nan
        
    data.append({
        "Order_ID": order_ids[i],
        "Order_Timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "Delivery_Zone": zone,
        "Cuisine_Type": cuisine,
        "Item_Name": item,
        "Item_Price_NGN": base_price,
        "Delivery_Fee_NGN": delivery_fee,
        "Discount_NGN": discount,
        "Total_Amount_NGN": total_amount,
        "Prep_Time_Min": prep_time,
        "Delivery_Time_Min": delivery_time,
        "Order_Status": status,
        "Customer_Rating": rating
    })

# Convert to DataFrame
df_orders = pd.DataFrame(data)

# Export to CSV and Excel
df_orders.to_csv("Nigerian_Food_Delivery_Orders.csv", index=False)

with pd.ExcelWriter("Nigerian_Food_Delivery_Orders.xlsx", engine="openpyxl") as writer:
    df_orders.to_excel(writer, sheet_name="Orders_Data", index=False)

print("Dataset successfully generated: 1,500 records saved to CSV and Excel!")