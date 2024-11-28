import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()

# Fetch and print all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Query data from a specific table (replace <table_name>)
for table in tables:
    cursor.execute("SELECT * FROM resume_userprofile LIMIT 10;")
rows = cursor.fetchall()
print("Rows:", rows)

# Close the connection
connection.close()
