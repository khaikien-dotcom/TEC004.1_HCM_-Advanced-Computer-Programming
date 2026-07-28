
# import sqlite3

# # # 10.1
# # def setup_database():
# #     conn = sqlite3.connect("housing_market.db")
# #     cursor = conn.cursor()

# #     cursor.execute("""
# #     CREATE TABLE IF NOT EXISTS database (
# #         prop_id INTEGER PRIMARY KEY,
# #         address TEXT,
# #         price_bil_vnd REAL,
# #         sqm REAL,
# #         unit_price_mil REAL,
# #         market_segment TEXT
# #     )
# #     """)

# #     conn.commit()
# #     conn.close()

# # setup_database()


# import json
# # # 10.2
# # def migrate_data(filepath):
# #     with open(filepath, "r", encoding="utf-8") as f:
# #         data = json.load(f)

# #     conn = sqlite3.connect("housing_market.db")
# #     cursor = conn.cursor()

# #     for item in data:
# #         cursor.execute("""
# #             INSERT OR IGNORE INTO database
# #             (prop_id, address, price_bil_vnd, sqm, unit_price_mil, market_segment)
# #             VALUES (?, ?, ?, ?, ?, ?)
# #         """, (
# #             item["prop_id"],
# #             item["address"],
# #             item["price_bil_vnd"],
# #             item["sqm"],
# #             item["unit_price_mil"],
# #             item["market_segment"]
# #         ))

# #     conn.commit()
# #     conn.close()

# # # migrate_data("scraped_data.json")

# # #10.3
# # def verify_migration():
# #     conn = sqlite3.connect("housing_market.db")
# #     cursor = conn.cursor()

# #     cursor.execute("SELECT COUNT(*) FROM database")
# #     count = cursor.fetchone()[0]

# #     cursor.execute("SELECT * FROM database LIMIT 5")
# #     records = cursor.fetchall()

# #     print("Total rows:", count)
# #     print("First 5 records:")
# #     for record in records:
# #         print(record)
    
# #     conn.commit()
# #     conn.close()
# # verify_migration()

# import pandas as pd
# import csv

# conn = sqlite3.connect("housing_market.db")
# cursor = conn.cursor()
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS properties (
#         prop_id INTEGER PRIMARY KEY,
#         address TEXT,
#         price REAL,
#         sqm REAL,
#         type TEXT
#     )
#     """)
# conn.commit()
# with open("market_report.csv", "r", encoding="utf-8") as f:
#     data = csv.DictReader(f)

#     for item in data:
#         cursor.execute("""
#             INSERT OR IGNORE INTO properties
#             (prop_id, address, price, sqm, type)
#             VALUES (?, ?, ?, ?, ?)
#         """, (
#             item["id"],
#             item["address"],
#             item["price"],
#             item["sqm"],
#             item["type"]
#         ))
# conn.commit()
# df_villas = pd.read_sql_query("""
#     SELECT * FROM properties
#     WHERE type = 'Villa'
#     AND price > 10
#     """, conn)
# print(df_villas.head())
# conn.commit()
# conn.close()

import sqlite3
from ai_engine import predict_market_price

DB_NAME = "housing_market.db"

# 1. ALTER TABLE Task: Add column for AI predictions
def add_prediction_column():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Adds the new column 'ai_predicted_price' to 'properties' table
        cursor.execute("ALTER TABLE properties ADD COLUMN ai_predicted_price REAL;")
        conn.commit()
        print("Successfully added column 'ai_predicted_price'.")
    except sqlite3.OperationalError as e:
        # Safety check: SQLite throws an error if column already exists
        if "duplicate column name" in str(e):
            print("Column 'ai_predicted_price' already exists. Skipping ALTER TABLE.")
        else:
            raise e
    finally:
        conn.close()

# 2. UPDATE Task: Fetch properties, run Gemini AI, and save back to DB
def populate_ai_predictions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Query all properties needing predictions
    cursor.execute("SELECT prop_id, sqm, type, price FROM properties")
    rows = cursor.fetchall()

    print(f"\nProcessing AI predictions for {len(rows)} properties...")

    for row in rows:
        prop_id, sqm, prop_type, price = row

        try:
            # Predict price using Gemini AI engine
            predicted_price = predict_market_price(
                sqm=sqm, 
                property_type=prop_type, 
                current_price=price
            )

            # Update the prediction back into the database
            cursor.execute("""
                UPDATE properties 
                SET ai_predicted_price = ? 
                WHERE prop_id = ?
            """, (predicted_price, prop_id))

            print(f"Prop ID {prop_id} ({prop_type}): Listed {price}B -> Predicted {predicted_price}B VND")

        except Exception as e:
            print(f"Error predicting price for Prop ID {prop_id}: {e}")

# Save all changes to database
    conn.commit()
    conn.close()
    print("\nAll database predictions successfully updated!")


if __name__ == "__main__":
    # Step A: Run ALTER TABLE once
    add_prediction_column()

    # Step B: Populate AI predictions
    populate_ai_predictions()