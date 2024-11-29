import sqlite3
import csv

# Connect to the SQLite database
connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()

# Fetch the table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Export the `auth_user` table data
try:
    table_name = "auth_user"  # Table you want to export
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    print(f"Fetched {len(rows)} rows from {table_name}.")
    
    # Get column names for the auth_user table
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [col[1] for col in cursor.fetchall()]
    print("Columns:", columns)

    # Write to CSV file
    with open(f"{table_name}.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # Write header row
        writer.writerows(rows)   # Write data rows

    print(f"Data successfully exported to {table_name}.csv")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the connection
    connection.close()
