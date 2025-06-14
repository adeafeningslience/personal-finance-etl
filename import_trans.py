import pandas as pd
import psycopg2

# Load your CSV
df = pd.read_csv('transactions.csv')

print(df.columns)


# Define a list to hold incomplete records
incomplete_rows = []

# Clean and validate each row
valid_rows = []
for _, row in df.iterrows():
    # Basic field checks
    if pd.isna(row["date"]) or pd.isna(row["amount"]) or pd.isna(row["category_id"]) or pd.isna(row["vendor"]):
        incomplete_rows.append(row)
        continue
    
    # Check amount
    try:
        amt = float(row["amount"])
        if amt <= 0:
            incomplete_rows.append(row)
            continue
    except ValueError:
        incomplete_rows.append(row)
        continue

    # Save cleaned/validated row
    valid_rows.append((row["id"], row["category_id"], amt, row["date"], row.get("description", "")))



try:
    # Connect to your database
    conn = psycopg2.connect(
        dbname="postgres",
        user="claytonwells",
        password="K%$h3lle",  # consider using environment variables for security
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Insert into transactions table
    for _, row in df.iterrows():
        try:
            cursor.execute("""
            INSERT INTO transactions (id, date, amount, description, account_id, category_id, vendor)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
            row['id'],
            row['date'],
            row['amount'],
            row['description'],
            row['account_id'],
            row['category_id'],
            row['vendor']
            ))
        except Exception as row_error:
            print(f"Failed to insert row {row['id']}: {row_error}")

    conn.commit()

except psycopg2.Error as db_error:
    print("Database connection or execution error:", db_error)
    

finally:
    # Ensure cleanup happens even if an error occurs
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()

if incomplete_rows:
    df_bad = pd.DataFrame(incomplete_rows)
    df_bad.to_csv("incomplete_transactions.csv", index=False)
    print(f"Saved {len(incomplete_rows)} incomplete records to 'incomplete_transactions.csv'")

        
